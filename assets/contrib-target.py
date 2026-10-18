#!/usr/bin/env python3
"""Contribution grid as target practice — no snake. Writes dist/*.svg

Uses GitHub GraphQL when GITHUB_TOKEN is set (CI). Locally uses empty grid.
Run from repo root: python3 assets/contrib-target.py
"""
import json
import os
import sys
import urllib.request

USER = os.environ.get("GITHUB_USER", "Rahul-ramakrishnan06")
OUT = os.environ.get("CONTRIB_OUT", os.path.join(os.path.dirname(__file__), "..", "dist"))

COLORS = ["#161616", "#3d1515", "#6b1f1f", "#9e2828", "#C41E3A"]
W, H = 900, 220
CELL, GAP = 11, 3


def fetch_calendar():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        return None, 0
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { contributionCount } }
          }
        }
      }
    }
    """
    body = json.dumps({"query": query, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "contrib-target-builder",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    grid = []
    for w in weeks:
        for d in w["contributionDays"]:
            grid.append(d["contributionCount"])
    return grid, cal["totalContributions"]


def color_for(n):
    if n <= 0:
        return COLORS[0]
    if n == 1:
        return COLORS[1]
    if n <= 3:
        return COLORS[2]
    if n <= 6:
        return COLORS[3]
    return COLORS[4]


def render(grid, total, variant):
    bg = "#080808" if variant == "dark" else "#0F0F0F"
    ink = "#E8E8E8"
    accent = "#C41E3A"
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Contribution target practice">',
        "<style>.p{animation:pulse 2s ease-in-out infinite}@keyframes pulse{50%{opacity:.55}}</style>",
        f'<rect width="{W}" height="{H}" fill="{bg}"/>',
        f'<text x="28" y="32" font-family="monospace" font-size="11" letter-spacing="2" fill="{accent}">TARGET PRACTICE — CONTRIBUTIONS</text>',
        f'<text x="28" y="54" font-family="sans-serif" font-size="13" fill="{ink}">Each hit is a day you shipped. Total: {total}</text>',
    ]
    ox, oy = 28, 72
    cols = 53
    rows = 7
    counts = grid if grid and len(grid) >= cols * rows else [0] * (cols * rows)
    if len(counts) > cols * rows:
        counts = counts[-cols * rows :]
    idx = 0
    for col in range(cols):
        for row in range(rows):
            n = counts[idx] if idx < len(counts) else 0
            idx += 1
            x = ox + col * (CELL + GAP)
            y = oy + row * (CELL + GAP)
            cls = ' class="p"' if n > 3 else ""
            o.append(f'<rect{cls} x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color_for(n)}"/>')
    cx, cy = W - 120, H / 2 + 20
    o.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{accent}" stroke-width="1" opacity="0.5"/>')
    o.append(f'<line x1="{cx-60}" y1="{cy}" x2="{cx+60}" y2="{cy}" stroke="{ink}" stroke-width="0.6" opacity="0.4"/>')
    o.append(f'<line x1="{cx}" y1="{cy-60}" x2="{cx}" y2="{cy+60}" stroke="{ink}" stroke-width="0.6" opacity="0.4"/>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    grid, total = fetch_calendar()
    if grid is None:
        grid, total = [], 0
        print("note: no GITHUB_TOKEN — wrote placeholder grid", file=sys.stderr)
    os.makedirs(OUT, exist_ok=True)
    for variant, fn in (("light", "contrib-target.svg"), ("dark", "contrib-target-dark.svg")):
        path = os.path.join(OUT, fn)
        with open(path, "w") as f:
            f.write(render(grid, total, variant))
        print("wrote", path)


if __name__ == "__main__":
    main()
