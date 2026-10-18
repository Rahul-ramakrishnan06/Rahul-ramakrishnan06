#!/usr/bin/env python3
"""Section header for war journal / contribution stats."""
import os
from punisher_theme import PUNISHER as P, skull, crosshair

W, H = 680, 72


def render(t):
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="War journal">',
        f'<rect width="{W}" height="{H}" fill="{t["BG"]}"/>',
        crosshair(W / 2, H / 2, 30, t["ACCENT"], t["INK"]),
        skull(42, 38, 0.9, t["ACCENT"], t["BG"]),
        skull(W - 42, 38, 0.9, t["ACCENT"], t["BG"]),
        f'<text x="{W/2}" y="42" text-anchor="middle" font-family="ui-monospace, Menlo, monospace" '
        f'font-size="14" letter-spacing="3" fill="{t["INK"]}">WAR JOURNAL</text>',
        '</svg>',
    ])


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in ("war-journal-header.svg", "war-journal-header-dark.svg"):
        with open(os.path.join(here, fn), "w") as f:
            f.write(render(P))
        print("wrote", fn)
