#!/usr/bin/env python3
"""Operator character card — animated loadout (Punisher noir).

Run: python3 character-card.py
Inventory items link to repos when viewed as raw SVG on GitHub.
"""
import os
from punisher_theme import PUNISHER as P, skull

NAME_1, NAME_2 = "RAHUL", "R"
CLASS = "DEVSECOPS INFRA LEAD"
METHOD = "zero trust · GitOps"
EMPLOYER = "stealth-startup"

LOADOUT = [
    ("Multi-cloud",    5, 5),
    ("Data center",    4, 5),
    ("IaC",            5, 5),
    ("CI/CD",          5, 5),
    ("Security",       5, 5),
    ("Open source",    3, 5),
]
VITALS = [
    ("employer",     EMPLOYER),
    ("public repos", "7"),
    ("certs",        "AWS SAA · TF Associate"),
    ("stack",        "Python · Bash · HCL"),
]
BASE = "https://github.com/Rahul-ramakrishnan06"
ITEMS = [
    ("multicloud-karmada-gitops", f"{BASE}/multicloud-karmada-gitops"),
    ("multicloud-karmada-setup", f"{BASE}/multicloud-karmada-setup"),
    ("supabase-selfhosted-k8s", f"{BASE}/supabase-selfhosted-k8s"),
    ("gcp-cloudrun-iac-rest-api", f"{BASE}/gcp-cloudrun-iac-rest-api"),
    ("DevOps_Projects", f"{BASE}/DevOps_Projects"),
    ("devops-ai-playbook", f"{BASE}/devops-ai-playbook"),
]

W, H = 860, 620
THEMES = {"light": {**P, "SLOT": "#1A1A1A"}, "dark": {**P, "SLOT": "#1A1A1A"}}
SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'
SERIF = 'Georgia, "Times New Roman", serif'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(t):
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="ct cd">')
    o.append('<title id="ct">Rahul R operator character card</title>')
    loadout = "; ".join(f"{d} {b} of {tot}" for d, b, tot in LOADOUT)
    o.append(f'<desc id="cd">Character card. {NAME_1} {NAME_2}, {esc(CLASS)}. Loadout: {esc(loadout)}.</desc>')
    o.append('<style>')
    o.append('.blink{animation:bl 1.1s steps(1) infinite}@keyframes bl{50%{opacity:0}}')
    o.append('.fillin{animation:fi .5s ease-out both}@keyframes fi{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}')
    o.append('a.inv text{fill:#FF4D5A}a.inv:hover text{fill:#E8E8E8}')
    o.append('@media (prefers-reduced-motion:reduce){.blink,.fillin{animation:none}}')
    o.append('</style>')
    o.append(f'<rect width="{W}" height="{H}" fill="{t["BG"]}"/>')
    o.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{t["RULE"]}"/>')
    for x, y in ((26, 26), (W-26, 26), (26, H-26), (W-26, H-26)):
        o.append(f'<path d="M{x-7} {y}H{x+7}M{x} {y-7}V{y+7}" stroke="{t["ACCENT"]}" stroke-width="1.2"/>')
    o.append(skull(W - 70, 58, 1.0, t["ACCENT2"], t["BG"]))
    o.append(f'<rect x="40" y="42" width="8" height="8" fill="{t["ACCENT"]}"/>')
    o.append(f'<text x="56" y="50" font-family=\'{MONO}\' font-size="11" letter-spacing="2.4" fill="{t["ACCENT"]}">OPERATOR CARD</text>')
    o.append(f'<text x="38" y="100" font-family=\'{SERIF}\' font-size="42" fill="{t["INK"]}">{NAME_1}</text>')
    o.append(f'<text x="38" y="140" font-family=\'{SERIF}\' font-size="42" fill="{t["INK"]}">{NAME_2}</text>')
    o.append(f'<text x="42" y="168" font-family=\'{MONO}\' font-size="11.5" fill="{t["MUTED"]}">CLASS   <tspan fill="{t["INK"]}">{esc(CLASS)}</tspan></text>')
    o.append(f'<text x="42" y="186" font-family=\'{MONO}\' font-size="11.5" fill="{t["MUTED"]}">METHOD  <tspan fill="{t["INK"]}">{METHOD}</tspan><tspan class="blink" fill="{t["ACCENT"]}">_</tspan></text>')
    o.append(f'<line x1="38" y1="206" x2="{W-38}" y2="206" stroke="{t["INK"]}" stroke-width="1.3"/>')
    lx, ly = 40, 244
    o.append(f'<text x="{lx}" y="{ly}" font-family=\'{MONO}\' font-size="11" letter-spacing="2" fill="{t["ACCENT"]}">LOADOUT</text>')
    y = ly + 28
    for d, b, tot in LOADOUT:
        o.append(f'<text x="{lx}" y="{y}" font-family=\'{SANS}\' font-size="15" fill="{t["INK"]}">{esc(d)}</text>')
        bx = lx + 190
        for i in range(tot):
            fill = t["ACCENT"] if i < b else t["BG"]
            stroke = "" if i < b else f' stroke="{t["SLOT"]}" stroke-width="1.4"'
            cls = ' class="fillin"' if i < b else ''
            dly = f' style="transform-box:fill-box;transform-origin:center;animation-delay:{0.2 + (y-ly)*0.004 + i*0.08:.2f}s"' if i < b else ''
            o.append(f'<rect{cls}{dly} x="{bx + i*22}" y="{y-13}" width="15" height="15" fill="{fill}"{stroke}/>')
        o.append(f'<text x="{bx + tot*22 + 10}" y="{y}" font-family=\'{MONO}\' font-size="11" fill="{t["MUTED"]}">{b}/{tot}</text>')
        y += 30
    o.append(f'<text x="{lx}" y="{y+4}" font-family=\'{MONO}\' font-size="10" fill="{t["MUTED"]}">bars = public work, not skill rating</text>')
    vx = 560
    o.append(f'<line x1="{vx-24}" y1="228" x2="{vx-24}" y2="470" stroke="{t["RULE"]}"/>')
    o.append(f'<text x="{vx}" y="{ly}" font-family=\'{MONO}\' font-size="11" letter-spacing="2" fill="{t["ACCENT"]}">VITALS</text>')
    vy = ly + 28
    for k, v in VITALS:
        o.append(f'<text x="{vx}" y="{vy}" font-family=\'{MONO}\' font-size="11.5" fill="{t["MUTED"]}">{k}</text>')
        o.append(f'<text x="{vx}" y="{vy+17}" font-family=\'{SANS}\' font-size="14" fill="{t["INK"]}">{esc(v)}</text>')
        vy += 46
    iy = 508
    o.append(f'<line x1="38" y1="{iy-24}" x2="{W-38}" y2="{iy-24}" stroke="{t["RULE"]}"/>')
    o.append(f'<text x="40" y="{iy}" font-family=\'{MONO}\' font-size="11" letter-spacing="2" fill="{t["ACCENT"]}">INVENTORY — CLICK IN FULL SVG</text>')
    cx, cyy = 40, iy + 22
    for name, url in ITEMS:
        wch = 14 + len(name) * 7.2
        if cx + wch > W - 40:
            cx = 40
            cyy += 32
        o.append(f'<a class="inv" xlink:href="{esc(url)}">')
        o.append(f'<rect x="{cx}" y="{cyy-15}" width="{wch:.0f}" height="22" fill="{t["BG2"]}" stroke="{t["RULE"]}"/>')
        o.append(f'<rect x="{cx}" y="{cyy-15}" width="3" height="22" fill="{t["ACCENT"]}"/>')
        o.append(f'<text x="{cx+11}" y="{cyy}" font-family=\'{MONO}\' font-size="11" fill="{t["LINK"]}">{esc(name)}</text>')
        o.append('</a>')
        cx += wch + 10
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, fn in (("light", "character-card.svg"), ("dark", "character-card-dark.svg")):
        with open(os.path.join(here, fn), "w") as f:
            f.write(card(THEMES[name]))
        print("wrote", fn)
