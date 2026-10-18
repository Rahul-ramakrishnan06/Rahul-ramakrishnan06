#!/usr/bin/env python3
"""Mission log + active missions — black/red board.

Run: python3 missions-board.py
"""
import os
from punisher_theme import PUNISHER as P, skull

W = 1000
BASE = "https://github.com/Rahul-ramakrishnan06"

MISSION_LOG = [
    ("stealth-startup · now", "DevSecOps Infra Lead — DC + GCP + AWS + Cloudflare."),
    ("iCliniq · through Sep 2026", "WIF on 15+ pipelines; Chainguard + Trivy; GenAI on Cloud Run."),
    ("Sony / Soneium", "99.99% mainnet uptime; GitOps; deploy time −40%."),
    ("Netgear / VVDN", "ECS production — deploy ~30% faster; cost ~25% lower."),
]

ACTIVE = [
    ("ACTIVE", "multicloud-karmada-gitops", "Cluster drift across federated fleets"),
    ("ACTIVE", "multicloud-karmada-setup", "IaC sprawl and control-plane skew"),
    ("BUILDING", "supabase-selfhosted-k8s", "Self-hosted data plane on Kubernetes"),
    ("ACTIVE", "gcp-cloudrun-iac-rest-api", "Serverless and API config drift"),
    ("LAB", "DevOps_Projects", "Pipeline experiments and automation"),
    ("REF", "devops-ai-playbook", "AI-assisted ops patterns (fork)"),
]

MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'
SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif'
ROW = 34
PAD = 24


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def status_color(status, t):
    if status == "ACTIVE":
        return t["ACCENT"]
    if status == "BUILDING":
        return "#D4A574"
    return t["MUTED"]


def render(t):
    log_h = PAD + 56 + len(MISSION_LOG) * ROW + 40
    active_h = 56 + len(ACTIVE) * ROW + PAD
    H = log_h + active_h
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="mbt mbd">',
        '<title id="mbt">Mission log and active missions</title>',
        '<desc id="mbd">Black and red tactical board with operation history and repository missions.</desc>',
        '<style>a.repo:hover text{fill:#E8E8E8}</style>',
        f'<rect width="{W}" height="{H}" fill="{t["BG"]}"/>',
        f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{t["RULE"]}"/>',
        skull(W - 58, 42, 0.85, t["ACCENT2"], t["BG"]),
    ]

    y = PAD + 20
    o.append(f'<text x="{PAD}" y="{y}" font-family=\'{MONO}\' font-size="11" letter-spacing="2.5" fill="{t["ACCENT"]}">MISSION LOG</text>')
    y += 10
    o.append(f'<line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="{t["ACCENT"]}" stroke-width="0.8"/>')
    y += 22
    o.append(f'<text x="{PAD}" y="{y}" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">OPERATION</text>')
    o.append(f'<text x="280" y="{y}" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">OUTCOME</text>')
    y += 18
    for op, out in MISSION_LOG:
        o.append(f'<rect x="{PAD}" y="{y-14}" width="{W-2*PAD}" height="{ROW-4}" fill="{t["BG2"]}" stroke="{t["RULE"]}"/>')
        o.append(f'<rect x="{PAD}" y="{y-14}" width="3" height="{ROW-4}" fill="{t["ACCENT"]}"/>')
        o.append(f'<text x="{PAD+14}" y="{y+4}" font-family=\'{SANS}\' font-size="13" font-weight="600" fill="{t["INK"]}">{esc(op)}</text>')
        o.append(f'<text x="280" y="{y+4}" font-family=\'{SANS}\' font-size="12.5" fill="{t["MUTED"]}">{esc(out)}</text>')
        y += ROW

    y += 24
    o.append(f'<text x="{PAD}" y="{y}" font-family=\'{MONO}\' font-size="11" letter-spacing="2.5" fill="{t["ACCENT"]}">ACTIVE MISSIONS</text>')
    y += 10
    o.append(f'<line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="{t["ACCENT"]}" stroke-width="0.8"/>')
    y += 22
    o.append(f'<text x="{PAD}" y="{y}" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">STATUS</text>')
    o.append(f'<text x="130" y="{y}" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">REPO</text>')
    o.append(f'<text x="420" y="{y}" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">THREAT MODEL</text>')
    y += 18
    for status, repo, threat in ACTIVE:
        o.append(f'<rect x="{PAD}" y="{y-14}" width="{W-2*PAD}" height="{ROW-4}" fill="{t["BG2"]}" stroke="{t["RULE"]}"/>')
        o.append(f'<rect x="{PAD}" y="{y-14}" width="3" height="{ROW-4}" fill="{status_color(status, t)}"/>')
        o.append(f'<text x="{PAD+14}" y="{y+4}" font-family=\'{MONO}\' font-size="10.5" font-weight="700" fill="{status_color(status, t)}">{esc(status)}</text>')
        url = f"{BASE}/{repo}"
        o.append(f'<a class="repo" xlink:href="{esc(url)}">')
        o.append(f'<text x="130" y="{y+4}" font-family=\'{MONO}\' font-size="11.5" fill="{t["LINK"]}">{esc(repo)}</text>')
        o.append("</a>")
        o.append(f'<text x="420" y="{y+4}" font-family=\'{SANS}\' font-size="12" fill="{t["INK"]}">{esc(threat)}</text>')
        y += ROW

    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in ("missions-board.svg", "missions-board-dark.svg"):
        with open(os.path.join(here, fn), "w") as f:
            f.write(render(P))
        print("wrote", fn)
