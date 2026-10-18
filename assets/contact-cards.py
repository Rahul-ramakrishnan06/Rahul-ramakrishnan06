#!/usr/bin/env python3
"""Contact cards — black + red Punisher style."""
import os
from punisher_theme import PUNISHER as P, skull

CARDS = [
    ("github",   "GitHub",   "Rahul-ramakrishnan06"),
    ("linkedin", "LinkedIn", "rahul-r-a9b564211"),
    ("x",        "X",        "@R_Rahul_06"),
    ("reddit",   "Reddit",   "u/R_ahul_R"),
    ("email",    "Email",    "rahulkarthi06@gmail.com"),
]

W, H = 240, 76
SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(label, handle):
    t = P
    size = 15 if len(handle) <= 22 else 12
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label)}: {esc(handle)}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="{t["BG"]}" stroke="{t["RULE"]}"/>',
        f'<rect x="0.5" y="0.5" width="3" height="{H-1}" fill="{t["ACCENT"]}"/>',
        skull(210, 38, 0.45, t["MUTED"], t["BG"]),
        f'<text x="18" y="27" font-family=\'{MONO}\' font-size="10.5" letter-spacing="1.8" fill="{t["ACCENT"]}">{esc(label.upper())}</text>',
        f'<text x="18" y="54" font-family=\'{SANS}\' font-size="{size}" fill="{t["INK"]}">{esc(handle)}</text>',
        '</svg>',
    ])


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "cards"), exist_ok=True)
    for cid, label, handle in CARDS:
        path = os.path.join(here, "cards", f"{cid}.svg")
        with open(path, "w") as f:
            f.write(card(label, handle) + "\n")
        print("wrote", path)
