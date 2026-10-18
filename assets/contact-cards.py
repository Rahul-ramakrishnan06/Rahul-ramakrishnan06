#!/usr/bin/env python3
"""Build contact cards for README.md footer."""
import os

CARDS = [
    ("github",   "GitHub",   "Rahul-ramakrishnan06"),
    ("linkedin", "LinkedIn", "rahul-r-a9b564211"),
    ("email",    "Email",    "rahulkarthi06@gmail.com"),
]

W, H = 240, 76
INK, MUTED, ACCENT, RULE, BG = "#191B19", "#6B6D71", "#C41E3A", "#E4E2DC", "#FAF9F6"
SANS = '"Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif'
MONO = 'ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(label, handle):
    size = 15 if len(handle) <= 22 else 12
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label)}: {esc(handle)}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="{BG}" stroke="{RULE}"/>',
        f'<rect x="0.5" y="0.5" width="3" height="{H-1}" fill="{ACCENT}"/>',
        f'<rect x="18" y="20" width="7" height="7" fill="{ACCENT}"/>',
        f'<text x="32" y="27" font-family=\'{MONO}\' font-size="10.5" letter-spacing="1.8" fill="{ACCENT}">{esc(label.upper())}</text>',
        f'<text x="18" y="54" font-family=\'{SANS}\' font-size="{size}" fill="{INK}">{esc(handle)}</text>',
        f'<path d="M{W-26} 18H{W-16}V28M{W-16} 18L{W-27} 29" fill="none" stroke="{MUTED}" stroke-width="1.4"/>',
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
