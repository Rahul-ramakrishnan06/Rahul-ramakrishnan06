"""Shared Punisher-inspired visuals (original art — not Marvel IP)."""

PUNISHER = dict(
    BG="#080808",
    BG2="#111111",
    INK="#E8E8E8",
    MUTED="#8A8A8A",
    ACCENT="#C41E3A",
    ACCENT2="#8B0000",
    RULE="#2A2A2A",
    GLOW="#C41E3A44",
    LINK="#FF4D5A",
)

# Generic skull silhouette (scaled group)
SKULL = """
<g id="skull" transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="-2" rx="14" ry="16" fill="{fill}" opacity="0.92"/>
  <rect x="-10" y="8" width="20" height="10" rx="3" fill="{fill}" opacity="0.92"/>
  <ellipse cx="-5" cy="0" rx="4.5" ry="5.5" fill="{bg}"/>
  <ellipse cx="5" cy="0" rx="4.5" ry="5.5" fill="{bg}"/>
  <rect x="-3" y="10" width="2.5" height="5" fill="{bg}"/>
  <rect x="0.5" y="10" width="2.5" height="5" fill="{bg}"/>
  <rect x="-6" y="10" width="2" height="4" fill="{bg}"/>
  <rect x="4" y="10" width="2" height="4" fill="{bg}"/>
</g>
"""


def skull(x, y, s, fill, bg):
    return SKULL.format(x=x, y=y, s=s, fill=fill, bg=bg)


def crosshair(cx, cy, r, accent, ink):
    return f"""
<g opacity="0.35">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" stroke-width="1"/>
  <line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{ink}" stroke-width="0.8"/>
  <line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}" stroke="{ink}" stroke-width="0.8"/>
</g>"""
