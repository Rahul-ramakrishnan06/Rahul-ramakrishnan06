#!/usr/bin/env python3
"""Build the mission timeline: career stages, self-playing walk."""
import os

STAGES = [
    ("Student · B.E. CSE",           "2018 – 2022"),
    ("DevOps · VVDN / Netgear",      "2022 – 2023"),
    ("DevOps · Sustainability",      "2024"),
    ("Blockchain · Sony Soneium",    "2024 – 2025"),
    ("Healthcare · iCliniq",         "2025 – 2026"),
    ("DevSecOps Infra Lead",         "2026 – present"),
]
W, H = 900, 210
LOOP = 14
THEMES = {
    "light": dict(INK="#191B19", MUTED="#6B6D71", ACCENT="#C41E3A", RULE="#E4E2DC", BG="#FAF9F6", GROUND="#C9B8B8"),
    "dark":  dict(INK="#E6EDF3", MUTED="#9BA5AF", ACCENT="#E63946", RULE="#30363D", BG="#0D1117", GROUND="#4A3035"),
}
MONO = 'ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
SANS = '"Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif'
SERIF = 'Georgia, "Times New Roman", "Liberation Serif", serif'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def run(t):
    gy = 150
    x0, x1 = 60, W - 40
    n = len(STAGES)
    seg = (x1 - x0) / n
    starts = [x0 + i * seg for i in range(n)]
    mids = [s + seg / 2 for s in starts]
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="jt jd">')
    o.append('<title id="jt">Rahul R mission timeline</title>')
    o.append(f'<desc id="jd">A self-playing walk along a career line through six stages: '
             f'{"; ".join(f"{r} {s}" for r,s in STAGES)}. Stages are evenly spaced, not to scale.</desc>')
    o.append('<style>')
    o.append(f'.runner{{animation:runx {LOOP}s linear infinite}}')
    o.append(f'@keyframes runx{{from{{transform:translateX({starts[0]-20:.0f}px)}}to{{transform:translateX({x1-6:.0f}px)}}}}')
    o.append('.legA{animation:legA .28s steps(1) infinite}.legB{animation:legB .28s steps(1) infinite}')
    o.append('@keyframes legA{50%{opacity:0}}@keyframes legB{0%,50%{opacity:0}50.01%{opacity:1}}')
    o.append('.bob{animation:bob .28s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-3px)}}')
    span = x1 - 6 - (starts[0] - 20)
    for i in range(n):
        frac = (starts[i] - (starts[0] - 20)) / span
        pct = max(0.1, frac * 100)
        o.append(f'.lit{i}{{animation:lit{i} {LOOP}s linear infinite}}'
                 f'@keyframes lit{i}{{0%,{max(0,pct-0.1):.1f}%{{opacity:.3}}{pct:.1f}%,100%{{opacity:1}}}}')
    o.append('@media (prefers-reduced-motion:reduce){.runner,.legA,.legB,.bob,'
             + ",".join(f".lit{i}" for i in range(n)) + '{animation:none}}')
    o.append('</style>')
    o.append(f'<rect width="{W}" height="{H}" fill="{t["BG"]}"/>')
    o.append(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{t["RULE"]}"/>')
    o.append(f'<text x="34" y="44" font-family=\'{MONO}\' font-size="11" letter-spacing="2.2" fill="{t["ACCENT"]}">MISSION TIMELINE</text>')
    o.append(f'<text x="34" y="70" font-family=\'{SERIF}\' font-size="18" fill="{t["INK"]}">From campus to data center and multi-cloud.</text>')
    o.append(f'<line x1="{x0-16}" y1="{gy}" x2="{x1}" y2="{gy}" stroke="{t["GROUND"]}" stroke-width="2"/>')
    for i, (role, spanlab) in enumerate(STAGES):
        sx, mx = starts[i], mids[i]
        o.append(f'<g class="lit{i}">')
        o.append(f'<line x1="{sx:.0f}" y1="{gy}" x2="{sx:.0f}" y2="{gy-28}" stroke="{t["ACCENT"]}" stroke-width="1.4"/>')
        o.append(f'<rect x="{sx:.0f}" y="{gy-34}" width="13" height="10" fill="{t["ACCENT"]}"/>')
        fs = 12 if len(role) > 22 else 14
        o.append(f'<text x="{mx:.0f}" y="{gy-44}" text-anchor="middle" font-family=\'{SANS}\' font-size="{fs}" font-weight="600" fill="{t["INK"]}">{esc(role)}</text>')
        o.append(f'<text x="{mx:.0f}" y="{gy+22}" text-anchor="middle" font-family=\'{MONO}\' font-size="10.5" fill="{t["MUTED"]}">{esc(spanlab)}</text>')
        o.append('</g>')
    o.append(f'<line x1="{x1:.0f}" y1="{gy}" x2="{x1:.0f}" y2="{gy-6}" stroke="{t["GROUND"]}" stroke-width="2"/>')
    o.append('<g class="runner"><g class="bob">')
    c = t["INK"]
    o.append(f'<rect x="-4" y="{gy-30}" width="9" height="9" fill="{c}"/>')
    o.append(f'<rect x="-3" y="{gy-20}" width="7" height="13" fill="{c}"/>')
    o.append(f'<line class="legA" x1="0" y1="{gy-8}" x2="-5" y2="{gy}" stroke="{c}" stroke-width="2.4"/>')
    o.append(f'<line class="legA" x1="1" y1="{gy-8}" x2="7" y2="{gy}" stroke="{c}" stroke-width="2.4"/>')
    o.append(f'<line class="legB" x1="0" y1="{gy-8}" x2="1" y2="{gy}" stroke="{c}" stroke-width="2.4"/>')
    o.append(f'<line class="legB" x1="1" y1="{gy-8}" x2="2" y2="{gy}" stroke="{c}" stroke-width="2.4"/>')
    o.append(f'<line x1="2" y1="{gy-18}" x2="9" y2="{gy-14}" stroke="{c}" stroke-width="2.2"/>')
    o.append('</g></g>')
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, fn in (("light", "journey.svg"), ("dark", "journey-dark.svg")):
        with open(os.path.join(here, fn), "w") as f:
            f.write(run(THEMES[name]))
        print("wrote", fn)
