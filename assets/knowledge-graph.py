#!/usr/bin/env python3
"""Build knowledge-graph.svg from the model below.

Standard library only. Run:  python3 knowledge-graph.py
The layout is a seeded force simulation, so the same model always gives the
same picture. Change the model, re-run, look at the result.
"""
import math, random, os, sys

# ---------------------------------------------------------------- model ----
# Domains orbit the identity node. "angle" is a starting hint in degrees
# (0 = right, 90 = down); the simulation moves them from there. The order
# round the ring keeps domains that share labelled links next to each other.
DOMAINS = [
    # id         label              angle
    ("cloud",   "Multi-cloud",      -100),
    ("dc",      "Data center",       -36),
    ("iac",     "IaC",                22),
    ("cicd",    "CI/CD & GitOps",     88),
    ("sec",     "Security",          148),
    ("platform","Platform",          210),
]

# state: built (shown in public work), explore (started, early),
#        interest (no public work yet).
CONCEPTS = [
    # id            label                      domain      state
    ("gcp",       "GCP & Cloud Run",          "cloud",     "built"),
    ("aws",       "AWS & edge cases",         "cloud",     "built"),
    ("cf",        "Cloudflare WAF & edge",    "cloud",     "built"),
    ("hybrid",    "Hybrid connectivity",      "cloud",     "built"),
    ("rack",      "Rack & power",             "dc",        "built"),
    ("netops",    "Network operations",       "dc",        "built"),
    ("bare",      "Bare-metal lifecycle",     "dc",        "built"),
    ("dr",        "DR & failover",            "dc",        "explore"),
    ("tf",        "Terraform modules",        "iac",       "built"),
    ("tg",        "Terragrunt stacks",        "iac",       "built"),
    ("drift",     "Drift & policy",           "iac",       "built"),
    ("gha",       "GitHub Actions",           "cicd",      "built"),
    ("argo",      "ArgoCD & Helm",            "cicd",      "built"),
    ("gitops",    "GitOps workflows",         "cicd",      "built"),
    ("wif",       "Workload Identity Fed.",   "sec",       "built"),
    ("scan",      "Trivy & Chainguard",       "sec",       "built"),
    ("posture",   "Cloud posture",            "sec",       "built"),
    ("k8s",       "Kubernetes",               "platform",  "built"),
    ("genai",     "LiteLLM & RAG",            "platform",  "built"),
    ("chain",     "Blockchain nodes",         "platform",  "built"),
    ("karmada",   "Multi-cluster Karmada",    "platform",  "explore"),
    ("supa",      "Self-hosted data plane",   "platform",  "explore"),
]

RELATIONS = [
    # from        to           label                kind
    ("wif",      "gha",       "secures",           "flow"),
    ("tf",       "gitops",    "defines",           "flow"),
    ("rack",     "hybrid",    "extends",           "flow"),
    ("scan",     "argo",      "gates",             "flow"),
    ("tf",       "argo",      "feeds",             "loop"),
]

# Optional fixed positions, applied after the simulation: {"id": (x, y)}
PINS = {}

# --------------------------------------------------------------- canvas ----
W, H = 1000, 1300
GX0, GY0, GX1, GY1 = 48, 214, 952, 1004     # graph area
CX, CY = 500, 606                            # identity node
SEED = 7

# Two palettes. Light is the default; dark matches GitHub's dark canvas so the
# plate does not glare. set_theme() picks one; render() reads these globals.
THEMES = {
    "light": dict(INK="#191B19", GREY="#55575C", MUTED="#6B6D71", ACCENT="#C41E3A",
                  EDGE="#9A6B6B", EDGE_LABEL="#5C3030", SAGE="#F0E0E0", RULE="#E4E2DC",
                  BG="#FAF9F6", DOT="#E8E4E4", MEMBER="#B89090", INTEREST="#868A84"),
    "dark":  dict(INK="#E6EDF3", GREY="#AEB7C0", MUTED="#9BA5AF", ACCENT="#E63946",
                  EDGE="#8B4A52", EDGE_LABEL="#C98A8A", SAGE="#2A1218", RULE="#30363D",
                  BG="#0D1117", DOT="#1C181A", MEMBER="#6B4548", INTEREST="#6E7681"),
}
INK = GREY = MUTED = ACCENT = EDGE = EDGE_LABEL = SAGE = RULE = BG = DOT = MEMBER = INTEREST = ""


def set_theme(name):
    globals().update(THEMES[name])

SANS = '"Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif'
MONO = 'ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
SERIF = 'Georgia, "Times New Roman", "Liberation Serif", serif'


def text_w(s, size, mono=False, bold=False):
    if mono:
        return len(s) * size * 0.6
    w = 0.0
    for ch in s:
        if ch in "il.,'|!:;": w += 0.26
        elif ch in "fjrt-() ": w += 0.32
        elif ch in "mwMW": w += 0.82
        elif ch.isupper(): w += 0.66
        else: w += 0.53
    return w * size * (1.06 if bold else 1.0)


# --------------------------------------------------------------- nodes -----
class Node:
    def __init__(self, nid, kind, label, x, y):
        self.id, self.kind, self.label = nid, kind, label
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.pinned = False
        self.state = "built"
        self.domain = None
        self.r = 4

    def box(self):
        """Box around dot and its label, used to keep labels apart."""
        if self.kind == "self":
            return (self.x - 96, self.y - 96, self.x + 96, self.y + 96)
        if self.kind == "domain":
            w = text_w(self.label, 22, bold=True)
            return (self.x - w / 2 - 8, self.y - self.r - 6, self.x + w / 2 + 8, self.y + self.r + 30)
        w = text_w(self.label, 15.5)
        return (self.x - w / 2 - 6, self.y - self.r - 3, self.x + w / 2 + 6, self.y + self.r + 23)


def build():
    rnd = random.Random(SEED)
    nodes = {}
    me = Node("self", "self", "Rahul R", CX, CY)
    me.pinned = True
    nodes["self"] = me
    for did, label, ang in DOMAINS:
        a = math.radians(ang)
        n = Node(did, "domain", label, CX + R_DOMAIN * math.cos(a), CY + R_DOMAIN / SQUASH * math.sin(a))
        nodes[did] = n
    for cid, label, dom, state in CONCEPTS:
        d = nodes[dom]
        a = math.atan2((d.y - CY) * SQUASH, d.x - CX) + rnd.uniform(-0.45, 0.45)
        n = Node(cid, "concept", label, CX + R_CONCEPT * math.cos(a), CY + R_CONCEPT / SQUASH * math.sin(a))
        n.state, n.domain = state, dom
        n.r = {"built": 6, "explore": 6, "interest": 3.6}[state]
        nodes[cid] = n
    for d in DOMAINS:
        nodes[d[0]].r = 11
    return nodes


def edges_of(nodes):
    e = []
    for d in DOMAINS:
        e.append(("self", d[0], "spoke"))
    for c in CONCEPTS:
        e.append((c[2], c[0], "member"))
    for a, b, lab, kind in RELATIONS:
        e.append((a, b, kind))
    return e


SPRING = {"spoke": (190, 0.010), "member": (110, 0.085),
          "flow": (170, 0.002), "loop": (240, 0.001)}
R_DOMAIN, R_CONCEPT, SQUASH = 205, 360, 1.12
RADIAL = {"domain": (R_DOMAIN, 0.06), "concept": (R_CONCEPT, 0.018)}


def simulate(nodes, edges, steps=900):
    ns = list(nodes.values())
    for step in range(steps):
        t = 1.0 - step / steps
        fx = {n.id: 0.0 for n in ns}
        fy = {n.id: 0.0 for n in ns}
        # charge
        for i, a in enumerate(ns):
            for b in ns[i + 1:]:
                dx, dy = a.x - b.x, a.y - b.y
                d2 = dx * dx + dy * dy + 0.01
                d = math.sqrt(d2)
                f = 2600.0 / d2
                fx[a.id] += f * dx / d; fy[a.id] += f * dy / d
                fx[b.id] -= f * dx / d; fy[b.id] -= f * dy / d
        # springs
        for a, b, kind in edges:
            A, B = nodes[a], nodes[b]
            L, k = SPRING[kind]
            dx, dy = B.x - A.x, B.y - A.y
            d = math.hypot(dx, dy) + 0.01
            f = k * (d - L)
            fx[A.id] += f * dx / d; fy[A.id] += f * dy / d
            fx[B.id] -= f * dx / d; fy[B.id] -= f * dy / d
        # each kind keeps to its own ring
        for n in ns:
            if n.kind in RADIAL:
                R, k = RADIAL[n.kind]
                dx, dy = n.x - CX, (n.y - CY) * SQUASH
                d = math.hypot(dx, dy) + 0.01
                f = k * (R - d)
                fx[n.id] += f * dx / d; fy[n.id] += f * dy / d / SQUASH
        # label boxes must not overlap
        for i, a in enumerate(ns):
            ax0, ay0, ax1, ay1 = a.box()
            for b in ns[i + 1:]:
                bx0, by0, bx1, by1 = b.box()
                ox = min(ax1, bx1) - max(ax0, bx0) + 8
                oy = min(ay1, by1) - max(ay0, by0) + 6
                if ox > 0 and oy > 0:
                    if ox < oy:
                        s = 0.5 * ox * (1 if a.x >= b.x else -1)
                        fx[a.id] += s; fx[b.id] -= s
                    else:
                        s = 0.5 * oy * (1 if a.y >= b.y else -1)
                        fy[a.id] += s; fy[b.id] -= s
        # move
        for n in ns:
            if n.pinned:
                continue
            m = math.hypot(fx[n.id], fy[n.id])
            cap = 2 + 14 * t
            if m > cap:
                fx[n.id] *= cap / m; fy[n.id] *= cap / m
            n.x += fx[n.id]; n.y += fy[n.id]
            x0, y0, x1, y1 = n.box()
            if x0 < GX0: n.x += GX0 - x0
            if x1 > GX1: n.x -= x1 - GX1
            if y0 < GY0: n.y += GY0 - y0
            if y1 > GY1: n.y -= y1 - GY1
    for k, (x, y) in PINS.items():
        nodes[k].x, nodes[k].y = x, y


# -------------------------------------------------------------- render -----
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sweep(n):
    """0..1 by angle round the identity node, clockwise from the top. Used to
    stagger the load animation so the graph builds in one sweep."""
    a = math.atan2(n.y - CY, n.x - CX) + math.pi / 2
    return (a % (2 * math.pi)) / (2 * math.pi) * 0.6


def render(nodes, edges):
    out = []
    labels = []
    o = out.append
    o(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    o('<title id="t">Intel graph: how Rahul R connects data center and cloud operations</title>')
    o(f'<desc id="d">{esc(describe())}</desc>')
    o('<defs>')
    o(f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="{DOT}"/></pattern>')
    o(f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L9 5L0 9z" fill="{EDGE}"/></marker>')
    o(f'<marker id="aa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L9 5L0 9z" fill="{ACCENT}"/></marker>')
    o('<style>')
    o(f'.s{{font-family:{SANS}}} .m{{font-family:{MONO}}} .f{{font-family:{SERIF}}}')
    o(f'.halo{{paint-order:stroke;stroke:{BG};stroke-width:4px;stroke-linejoin:round}}')
    o('.draw{stroke-dasharray:1;animation:draw .7s ease-out both}')
    o('.fade{animation:fade .5s ease-out both}')
    o('.pop{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.2,.9,.3,1.25) both}')
    o('@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}')
    o('@keyframes fade{from{opacity:0}to{opacity:1}}')
    o('@keyframes pop{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:scale(1)}}')
    o('@media (prefers-reduced-motion:reduce){.draw,.fade,.pop{animation:none}}')
    o('</style></defs>')
    o(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    o(f'<rect x="{GX0-24}" y="{GY0-24}" width="{GX1-GX0+48}" height="{GY1-GY0+40}" fill="url(#dots)"/>')
    o(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="{RULE}"/>')
    for x, y in ((34, 34), (W - 34, 34), (34, H - 34), (W - 34, H - 34)):
        o(f'<path d="M{x-7} {y}H{x+7}M{x} {y-7}V{y+7}" stroke="{ACCENT}" stroke-width="1.2"/>')
    masthead(o)

    # membership lines first, then spokes, then labelled links
    for a, b, kind in edges:
        A, B = nodes[a], nodes[b]
        if kind == "member":
            o(f'<line class="draw" pathLength="1" style="animation-delay:{1.0 + sweep(B):.2f}s" x1="{A.x:.1f}" y1="{A.y:.1f}" x2="{B.x:.1f}" y2="{B.y:.1f}" stroke="{MEMBER}" stroke-width="1.1"/>')
    for d in DOMAINS:
        D = nodes[d[0]]
        o(f'<line class="draw" pathLength="1" style="animation-delay:{0.35 + sweep(D) * 0.5:.2f}s" x1="{CX}" y1="{CY}" x2="{D.x:.1f}" y2="{D.y:.1f}" stroke="{INK}" stroke-width="2.4"/>')
    placed = []
    for a, b, lab, kind in RELATIONS:
        A, B = nodes[a], nodes[b]
        dx, dy = B.x - A.x, B.y - A.y
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        sx, sy = A.x + ux * (A.r + 3), A.y + uy * (A.r + 3)
        ex, ey = B.x - ux * (B.r + 5), B.y - uy * (B.r + 5)
        mx_, my_ = (sx + ex) / 2, (sy + ey) / 2
        # try both sides and several bends; keep curves that clear the
        # identity node, then pick the one crossing the fewest node labels
        boxes = [n.box() for n in nodes.values() if n.id not in (a, b, "self")]
        best = None
        for f in (0.18, 0.3, 0.42, 0.55, 0.7, 0.85):
            for side in (1, -1):
                bend = f * d * side
                cx_, cy_ = mx_ - uy * bend, my_ + ux * bend
                pts = [((1-t)**2*sx + 2*(1-t)*t*cx_ + t*t*ex, (1-t)**2*sy + 2*(1-t)*t*cy_ + t*t*ey)
                       for t in [i/40 for i in range(41)]]
                if min(math.hypot(x - CX, y - CY) for x, y in pts) <= 118:
                    continue
                hits = sum(1 for bx in boxes if any(bx[0] <= x <= bx[2] and bx[1] <= y <= bx[3] for x, y in pts))
                outward = math.hypot(cx_ - CX, cy_ - CY) >= math.hypot(mx_ - CX, my_ - CY)
                score = (hits, f, 0 if outward else 1)
                if best is None or score < best[0]:
                    best = (score, cx_, cy_)
        qx, qy = best[1], best[2]
        col, mk, dash = (ACCENT, "aa", ' stroke-dasharray="5 4"') if kind == "loop" else (EDGE, "ah", "")
        anim = 'class="fade"' if kind == "loop" else 'class="draw" pathLength="1"'
        o(f'<g class="fade" style="animation-delay:{2.0 + sweep(A) * 0.4:.2f}s"><path {anim} style="animation-delay:{2.0 + sweep(A) * 0.4:.2f}s" d="M{sx:.1f} {sy:.1f}Q{qx:.1f} {qy:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="{col}" stroke-width="1.3"{dash} marker-end="url(#{mk})"/></g>')
        # put the label at the first point along the curve that is clear of
        # every node, its label, and labels already placed
        lw = text_w(lab, 11, True) + 8
        def bez(t):
            return ((1-t)**2*sx + 2*(1-t)*t*qx + t*t*ex, (1-t)**2*sy + 2*(1-t)*t*qy + t*t*ey)
        best = None
        for t in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.2, 0.8):
            px, py = bez(t)
            bx = (px - lw/2, py - 8, px + lw/2, py + 8)
            hit = any(not (bx[2] < b[0] or bx[0] > b[2] or bx[3] < b[1] or bx[1] > b[3])
                      for b in [n.box() for n in nodes.values()] + placed)
            if not hit:
                best = (px, py, bx); break
        if best is None:
            px, py = bez(0.5); best = (px, py, (px - lw/2, py - 8, px + lw/2, py + 8))
        lx, ly, bx = best
        placed.append(bx)
        labels.append(f'<text class="m halo fade" style="animation-delay:{2.5 + sweep(A) * 0.4:.2f}s" x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" font-size="11" fill="{ACCENT if kind == "loop" else EDGE_LABEL}">{esc(lab)}</text>')

    # nodes
    for n in nodes.values():
        if n.kind == "concept":
            o(f'<g class="pop" style="animation-delay:{1.2 + sweep(n):.2f}s">')
            q = n.r * 0.9
            if n.state == "built":
                o(f'<rect x="{n.x-q:.1f}" y="{n.y-q:.1f}" width="{2*q:.1f}" height="{2*q:.1f}" fill="{ACCENT}"/>')
                fill = INK
            elif n.state == "explore":
                o(f'<rect x="{n.x-q:.1f}" y="{n.y-q:.1f}" width="{2*q:.1f}" height="{2*q:.1f}" fill="{BG}" stroke="{ACCENT}" stroke-width="1.8"/>')
                fill = INK
            else:
                o(f'<rect x="{n.x-q:.1f}" y="{n.y-q:.1f}" width="{2*q:.1f}" height="{2*q:.1f}" fill="{BG}" stroke="{INTEREST}" stroke-width="1.3"/>')
                fill = GREY
            o('</g>')
            o(f'<text class="s halo fade" style="animation-delay:{1.35 + sweep(n):.2f}s" x="{n.x:.1f}" y="{n.y + n.r + 16:.1f}" text-anchor="middle" font-size="15.5" fill="{fill}">{esc(n.label)}</text>')
        elif n.kind == "domain":
            q = n.r + 2
            dl = 0.85 + sweep(n) * 0.5
            o(f'<g class="pop" style="animation-delay:{dl:.2f}s">')
            o(f'<rect x="{n.x-q-4:.1f}" y="{n.y-q-4:.1f}" width="{2*q+8:.1f}" height="{2*q+8:.1f}" fill="{BG}" stroke="{INK}" stroke-width="0.9"/>')
            o(f'<rect x="{n.x-q:.1f}" y="{n.y-q:.1f}" width="{2*q:.1f}" height="{2*q:.1f}" fill="{INK}"/>')
            o('</g>')
            serial = "%02d" % ([d[0] for d in DOMAINS].index(n.id) + 1)
            lw_ = text_w(n.label, 22, bold=True)
            o(f'<text class="m halo fade" style="animation-delay:{dl + 0.15:.2f}s" x="{n.x - lw_/2 - 6:.1f}" y="{n.y + n.r + 29:.1f}" text-anchor="end" font-size="11" fill="{ACCENT}">{serial}</text>')
            o(f'<text class="s halo fade" style="animation-delay:{dl + 0.15:.2f}s" x="{n.x:.1f}" y="{n.y + n.r + 29:.1f}" text-anchor="middle" font-size="22" font-weight="700" fill="{INK}">{esc(n.label)}</text>')
    out.extend(labels)
    o('<g class="fade" style="animation-delay:2.9s">')
    callouts(o, nodes)
    o('</g>')
    # identity: crosshair and serif name, no box
    o('<g class="fade">')
    o(f'<circle cx="{CX}" cy="{CY}" r="74" fill="{BG}" stroke="{ACCENT}" stroke-width="1" stroke-dasharray="2 4"/>')
    o(f'<path d="M{CX-94} {CY}H{CX-78}M{CX+78} {CY}H{CX+94}M{CX} {CY-94}V{CY-78}M{CX} {CY+78}V{CY+94}" stroke="{ACCENT}" stroke-width="1.4"/>')
    o(f'<text class="f halo" x="{CX}" y="{CY+8}" text-anchor="middle" font-size="34" fill="{INK}">Rahul R</text>')
    o(f'<text class="m" x="{CX}" y="{CY+42}" text-anchor="middle" font-size="9.5" letter-spacing="1.4" fill="{ACCENT}">DEVSECOPS INFRA LEAD</text>')
    o('</g>')
    panel(o)
    o('</svg>')
    return "\n".join(out)


# Annotations: node, box top-left, lines. Placed in the empty corners.
CALLOUTS = [
    ("wif",     (48, 214),  ["zero trust", "no long-lived keys in CI;", "identity federation everywhere"]),
    ("rack",    (736, 214), ["data center first", "what runs on metal still", "has to meet cloud bar for security"]),
    ("gitops",  (690, 930), ["gitops", "desired state in the repo,", "not on someone's laptop"]),
]


def callouts(o, nodes):
    for nid, (bx, by), lines in CALLOUTS:
        n = nodes[nid]
        w = max(text_w(l, 11, True) for l in lines) + 20
        h = 16 * len(lines) + 12
        # elbow leader from the node to the nearest side of the box
        ex = bx if n.x < bx else bx + w
        ey = by + h / 2
        o(f'<path d="M{n.x:.1f} {n.y:.1f}V{ey:.1f}H{ex:.1f}" fill="none" stroke="{INK}" stroke-width="0.8" stroke-dasharray="2 2"/>')
        o(f'<circle cx="{n.x:.1f}" cy="{n.y:.1f}" r="{n.r + 5:.1f}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
        o(f'<rect x="{bx}" y="{by}" width="{w:.1f}" height="{h}" fill="{BG}" stroke="{INK}" stroke-width="0.9"/>')
        o(f'<rect x="{bx}" y="{by}" width="3" height="{h}" fill="{ACCENT}"/>')
        for i, l in enumerate(lines):
            wt, col = ("600", INK) if i == 0 else ("400", MUTED)
            o(f'<text class="m" x="{bx + 12}" y="{by + 20 + 16 * i}" font-size="11" font-weight="{wt}" fill="{col}">{esc(l)}</text>')


def masthead(o):
    o(f'<rect x="48" y="58" width="8" height="8" fill="{ACCENT}"/>')
    o(f'<text class="m" x="64" y="66" font-size="11" letter-spacing="2" fill="{ACCENT}">CLASSIFIED INTEL GRAPH</text>')
    o(f'<text class="f" x="46" y="112" font-size="34" fill="{INK}">Data center to multi-cloud.</text>')
    o(f'<text class="f" x="46" y="150" font-size="34" fill="{INK}">Hardened. Automated. Measured.</text>')
    rows = [("name", "Rahul R"), ("role", "DevSecOps infrastructure lead"),
            ("focus", "DC, GCP, AWS, Cloudflare"), ("method", "zero trust & GitOps"),
            ("checks", "scan, posture, uptime"), ("profile", "github.com/Rahul-ramakrishnan06")]
    y = 64
    for k, v in rows:
        dots = "." * (17 - len(k))
        o(f'<text class="m" x="600" y="{y}" font-size="11.5"><tspan fill="{MUTED}">{k} {dots}</tspan><tspan fill="{INK}"> {esc(v)}</tspan></text>')
        y += 19
    o(f'<line x1="48" y1="184" x2="952" y2="184" stroke="{INK}" stroke-width="1.4"/>')
    o(f'<line x1="48" y1="188.5" x2="952" y2="188.5" stroke="{RULE}"/>')


def panel(o):
    y0 = 1036
    o(f'<line x1="48" y1="{y0}" x2="952" y2="{y0}" stroke="{INK}" stroke-width="1.4"/>')
    o(f'<line x1="48" y1="{y0+4.5}" x2="952" y2="{y0+4.5}" stroke="{RULE}"/>')
    ly = y0 + 34
    # node states
    lx = 48
    o(f'<text class="m" x="{lx}" y="{ly}" font-size="11" letter-spacing="1.6" fill="{ACCENT}">READING THE GRAPH</text>')
    items = [("built", "shown in public work"), ("explore", "started, early"), ("interest", "interest, nothing public yet")]
    yy = ly + 26
    for kind, lab in items:
        if kind == "built": o(f'<rect x="{lx+2}" y="{yy-10}" width="11" height="11" fill="{ACCENT}"/>')
        if kind == "explore": o(f'<rect x="{lx+2}" y="{yy-10}" width="11" height="11" fill="{BG}" stroke="{ACCENT}" stroke-width="1.8"/>')
        if kind == "interest": o(f'<rect x="{lx+4}" y="{yy-8}" width="7" height="7" fill="{BG}" stroke="{INTEREST}" stroke-width="1.3"/>')
        o(f'<text class="s" x="{lx+24}" y="{yy}" font-size="13.5" fill="{INK}">{lab}</text>')
        yy += 24
    # link types
    o(f'<text class="m" x="{lx}" y="{yy+14}" font-size="11" letter-spacing="1.6" fill="{ACCENT}">LINKS</text>')
    yy += 40
    o(f'<line x1="{lx}" y1="{yy-4}" x2="{lx+30}" y2="{yy-4}" stroke="{EDGE}" stroke-width="1.3" marker-end="url(#ah)"/>')
    o(f'<text class="s" x="{lx+42}" y="{yy}" font-size="13.5" fill="{INK}">one idea feeds another</text>')
    yy += 24
    o(f'<line x1="{lx}" y1="{yy-4}" x2="{lx+30}" y2="{yy-4}" stroke="{ACCENT}" stroke-width="1.3" stroke-dasharray="5 4" marker-end="url(#aa)"/>')
    o(f'<text class="s" x="{lx+42}" y="{yy}" font-size="13.5" fill="{INK}">feedback loop</text>')
    # how I decide
    tx = 372
    o(f'<line x1="{tx-20}" y1="{y0+18}" x2="{tx-20}" y2="{y0+186}" stroke="{RULE}"/>')
    o(f'<text class="m" x="{tx}" y="{ly}" font-size="11" letter-spacing="1.6" fill="{ACCENT}">HOW I DECIDE</text>')
    rules = [("mechanism", "understand network, identity, and state"),
             ("least privilege", "no standing credentials in pipelines"),
             ("gitops", "declarative desired state in version control"),
             ("supply chain", "harden images; scan in every build"),
             ("observability", "measure uptime, cost, and recovery time"),
             ("outcomes", "blast radius and SLA over tool fashion")]
    yy = ly + 26
    for i, (k, v) in enumerate(rules, 1):
        o(f'<text class="m" x="{tx}" y="{yy}" font-size="11" fill="{ACCENT}">{i:02d}</text>')
        o(f'<text class="s" x="{tx+26}" y="{yy}" font-size="13.5" fill="{INK}"><tspan font-weight="700">{k}</tspan><tspan fill="{GREY}">  {v}</tspan></text>')
        yy += 23
    # footnote
    o(f'<text class="s" x="48" y="{H-38}" font-size="11.5" fill="{GREY}">Squares show public evidence, not skill level.</text>')


def describe():
    parts = ["An intel graph with Rahul R at the centre, joined to six domains."]
    for did, label, _ in DOMAINS:
        items = []
        for c in CONCEPTS:
            if c[2] != did:
                continue
            s = c[1]
            if c[3] == "explore": s += ", started"
            if c[3] == "interest": s += ", interest with nothing public yet"
            items.append(s)
        parts.append(f"{label}: " + "; ".join(items) + ".")
    lab = {c[0]: c[1] for c in CONCEPTS}
    lab.update({d[0]: d[1] for d in DOMAINS})
    parts.append("Labelled links: " + "; ".join(f"{lab[a]} to {lab[b]}, {l}" for a, b, l, k in RELATIONS) + ".")
    parts.append("Callouts: " + "; ".join(" ".join(c[2]) for c in CALLOUTS) + ".")
    parts.append("A footer lists how decisions are made: mechanism, least privilege, GitOps, supply chain, "
                 "observability, and outcomes.")
    return " ".join(parts)


if __name__ == "__main__":
    nodes = build()
    edges = edges_of(nodes)
    simulate(nodes, edges)
    here = os.path.dirname(os.path.abspath(__file__))
    for name, fname in (("light", "knowledge-graph.svg"), ("dark", "knowledge-graph-dark.svg")):
        set_theme(name)
        out = os.path.join(here, fname)
        with open(out, "w") as f:
            f.write(render(nodes, edges))
        print("wrote", out)
