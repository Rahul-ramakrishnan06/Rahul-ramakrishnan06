#!/usr/bin/env python3
"""Judgment runbook tabs — Punisher noir."""
import os
from punisher_theme import PUNISHER as P, skull

TABS = [
    ("01", "WIF", "No standing keys"),
    ("02", "SCAN", "Harden + Trivy"),
    ("03", "GITOPS", "Truth in git"),
    ("04", "DR", "Know RTO/RPO"),
    ("05", "SLO", "Measure or guess"),
    ("06", "BLAST", "Shrink radius"),
]

W, H = 1000, 124
THEMES = {"light": P, "dark": P}
MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'
SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(t):
    n = len(TABS)
    margin, gap = 24, 8
    tab_w = (W - 2 * margin - gap * (n - 1)) / n
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rt rd">',
        '<title id="rt">Judgment runbook</title>',
        '<desc id="rd">Six Punisher-style operating tabs for hybrid infra.</desc>',
        f'<rect width="{W}" height="{H}" fill="{t["BG"]}"/>',
        skull(968, 28, 0.75, t["ACCENT"], t["BG"]),
        f'<text x="{margin}" y="28" font-family=\'{MONO}\' font-size="10" letter-spacing="2" fill="{t["ACCENT"]}">JUDGMENT RUNBOOK</text>',
    ]
    y0 = 44
    th = H - y0 - 12
    for i, (num, title, sub) in enumerate(TABS):
        x = margin + i * (tab_w + gap)
        o.append(f'<rect x="{x:.1f}" y="{y0}" width="{tab_w:.1f}" height="{th}" fill="{t["BG2"]}" stroke="{t["RULE"]}"/>')
        o.append(f'<rect x="{x:.1f}" y="{y0}" width="4" height="{th}" fill="{t["ACCENT"]}"/>')
        o.append(f'<text x="{x+14:.1f}" y="{y0+20}" font-family=\'{MONO}\' font-size="9" fill="{t["MUTED"]}">{num}</text>')
        o.append(f'<text x="{x+14:.1f}" y="{y0+40}" font-family=\'{MONO}\' font-size="11" font-weight="700" fill="{t["INK"]}">{esc(title)}</text>')
        fs = 10 if len(sub) > 18 else 11
        o.append(f'<text x="{x+14:.1f}" y="{y0+58}" font-family=\'{SANS}\' font-size="{fs}" fill="{t["MUTED"]}">{esc(sub)}</text>')
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, fn in (("light", "runbook-strip.svg"), ("dark", "runbook-strip-dark.svg")):
        path = os.path.join(here, fn)
        with open(path, "w") as f:
            f.write(render(THEMES[name]))
        print("wrote", path)
