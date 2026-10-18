#!/usr/bin/env python3
"""Cross-section map: DC ↔ WAN ↔ cloud. Punisher noir styling.

Run: python3 hybrid-perimeter.py
"""
import os
from punisher_theme import PUNISHER as P, skull, crosshair

W, H = 1000, 580
BASE = "https://github.com/Rahul-ramakrishnan06"
EMPLOYER = "stealth-startup"

THEMES = {
    "light": {**P, "ZONE_DC": "#0F0F0F", "ZONE_WAN": "#121010", "ZONE_CL": "#0D1014", "LINE": "#444"},
    "dark":  {**P, "ZONE_DC": "#0A0A0A", "ZONE_WAN": "#100C0C", "ZONE_CL": "#080C10", "LINE": "#3A3A3A"},
}
MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'
SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def link(url, inner):
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{inner}</a>'


def rack(x, y, h, t, label, href=None):
    w = 52
    body = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t["ZONE_DC"]}" stroke="{t["ACCENT"]}" stroke-width="1"/>',
        f'<line x1="{x+8}" y1="{y+12}" x2="{x+w-8}" y2="{y+12}" stroke="{t["RULE"]}"/>',
        f'<line x1="{x+8}" y1="{y+28}" x2="{x+w-8}" y2="{y+28}" stroke="{t["RULE"]}"/>',
        f'<line x1="{x+8}" y1="{y+44}" x2="{x+w-8}" y2="{y+44}" stroke="{t["RULE"]}"/>',
        f'<circle cx="{x+w/2}" cy="{y+h-18}" r="4" fill="{t["ACCENT"]}"/>',
        f'<text x="{x+w/2}" y="{y+h+16}" text-anchor="middle" font-family=\'{MONO}\' font-size="9" fill="{t["MUTED"]}">{esc(label)}</text>',
    ]
    inner = "\n".join(body)
    if href:
        return link(href, f'<g class="hotspot">{inner}<rect x="{x}" y="{y}" width="{w}" height="{h+20}" fill="transparent"/></g>')
    return f"<g>{inner}</g>"


def cloud_block(x, y, w, h, t, title, lines, href):
    inner = "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{t["ZONE_CL"]}" stroke="{t["ACCENT"]}" stroke-width="1.2"/>',
        f'<text x="{x+12}" y="{y+22}" font-family=\'{MONO}\' font-size="10" letter-spacing="1.5" fill="{t["ACCENT"]}">{esc(title)}</text>',
    ])
    ly = y + 40
    for line in lines:
        inner += f'\n<text x="{x+12}" y="{ly}" font-family=\'{SANS}\' font-size="11" fill="{t["INK"]}">{esc(line)}</text>'
        ly += 16
    return link(href, f'<g>{inner}<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="transparent"/></g>')


def render(t):
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="pt pd">')
    o.append('<title id="pt">Hybrid perimeter map — Punisher ops theme</title>')
    o.append('<desc id="pd">Black tactical map from data center through WAN to multi-cloud. '
             'Current employer stealth-startup. Click zones for repositories.</desc>')
    o.append('<style>.hotspot rect[fill=transparent]{cursor:pointer}.hotspot:hover rect[fill=transparent]{fill:' + t["GLOW"] + '}</style>')
    o.append(f'<rect width="{W}" height="{H}" fill="{t["BG"]}"/>')
    o.append(crosshair(500, 300, 220, t["ACCENT"], t["INK"]))
    o.append(skull(920, 52, 1.1, t["MUTED"], t["BG"]))
    o.append(skull(48, 520, 0.85, t["ACCENT2"], t["BG"]))

    o.append(f'<text x="32" y="36" font-family=\'{MONO}\' font-size="10" letter-spacing="3" fill="{t["ACCENT"]}">CLASSIFIED — HYBRID PERIMETER</text>')
    o.append(f'<text x="32" y="72" font-family=\'{SANS}\' font-size="26" font-weight="700" fill="{t["INK"]}">Rack to region — one perimeter.</text>')
    o.append(f'<text x="32" y="98" font-family=\'{SANS}\' font-size="13" fill="{t["MUTED"]}">DevSecOps Infra Lead · {EMPLOYER} · DC + GCP + AWS + Cloudflare</text>')

    o.append(f'<rect x="24" y="118" width="290" height="400" fill="{t["ZONE_DC"]}" stroke="{t["RULE"]}"/>')
    o.append(f'<rect x="314" y="118" width="372" height="400" fill="{t["ZONE_WAN"]}" stroke="{t["RULE"]}"/>')
    o.append(f'<rect x="686" y="118" width="290" height="400" fill="{t["ZONE_CL"]}" stroke="{t["RULE"]}"/>')

    o.append(f'<text x="44" y="142" font-family=\'{MONO}\' font-size="10" letter-spacing="2" fill="{t["ACCENT"]}">DATA CENTER</text>')
    o.append(f'<text x="334" y="142" font-family=\'{MONO}\' font-size="10" letter-spacing="2" fill="{t["ACCENT"]}">WAN · ZERO TRUST</text>')
    o.append(f'<text x="706" y="142" font-family=\'{MONO}\' font-size="10" letter-spacing="2" fill="{t["ACCENT"]}">MULTI-CLOUD</text>')

    o.append(rack(48, 168, 120, t, "COMPUTE", f"{BASE}/DevOps_Projects"))
    o.append(rack(118, 168, 120, t, "K8s / PLATFORM", f"{BASE}/supabase-selfhosted-k8s"))
    o.append(rack(188, 168, 120, t, "NETWORK", None))
    o.append(f'<text x="44" y="330" font-family=\'{SANS}\' font-size="12" fill="{t["INK"]}">Bare metal · TOR · PDU discipline</text>')
    o.append(f'<text x="44" y="350" font-family=\'{SANS}\' font-size="12" fill="{t["MUTED"]}">Custody and latency still win here</text>')

    cx, cy = 500, 280
    o.append(f'<line x1="314" y1="{cy}" x2="686" y2="{cy}" stroke="{t["LINE"]}" stroke-width="3" stroke-dasharray="8 6"/>')
    o.append(f'<line x1="260" y1="{cy}" x2="314" y2="{cy}" stroke="{t["ACCENT"]}" stroke-width="2"/>')
    o.append(f'<line x1="686" y1="{cy}" x2="740" y2="{cy}" stroke="{t["ACCENT"]}" stroke-width="2"/>')
    o.append(f'<polygon points="{cx},{cy-36} {cx+40},{cy} {cx},{cy+36} {cx-40},{cy}" fill="{t["BG"]}" stroke="{t["ACCENT"]}" stroke-width="1.8"/>')
    o.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family=\'{MONO}\' font-size="9" fill="{t["INK"]}">WIF</text>')
    o.append(f'<text x="334" y="200" font-family=\'{MONO}\' font-size="10" fill="{t["INK"]}">IAP · mTLS · secret rotation</text>')
    o.append(f'<text x="334" y="220" font-family=\'{MONO}\' font-size="10" fill="{t["MUTED"]}">No long-lived keys in CI</text>')
    o.append(link(f"{BASE}/multicloud-karmada-setup",
                  f'<text x="334" y="380" font-family=\'{MONO}\' font-size="11" fill="{t["LINK"]}">↗ IaC: multicloud-karmada-setup</text>'))
    o.append(link(f"{BASE}/multicloud-karmada-gitops",
                  f'<text x="334" y="400" font-family=\'{MONO}\' font-size="11" fill="{t["LINK"]}">↗ GitOps: multicloud-karmada-gitops</text>'))
    o.append(f'<circle cx="400" cy="{cy}" r="5" fill="{t["ACCENT"]}"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></circle>')

    o.append(cloud_block(706, 168, 250, 100, t, "GCP", ["Cloud Run · WIF · Firestore"], f"{BASE}/gcp-cloudrun-iac-rest-api"))
    o.append(cloud_block(706, 282, 250, 100, t, "AWS", ["ECS · EKS · SES/S3"], f"{BASE}/DevOps_Projects"))
    o.append(cloud_block(706, 396, 250, 100, t, "CLOUDFLARE", ["WAF · Pages · R2"], f"{BASE}/DevOps_Projects"))

    o.append(f'<line x1="32" y1="528" x2="968" y2="528" stroke="{t["ACCENT"]}" stroke-width="0.6"/>')
    o.append(f'<text x="32" y="548" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">CLICK ZONES → REPOS</text>')
    o.append(f'<text x="250" y="548" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">CURRENT · {EMPLOYER}</text>')
    o.append(f'<text x="500" y="548" font-family=\'{MONO}\' font-size="9.5" fill="{t["MUTED"]}">PAST · iCliniq · Soneium · Netgear</text>')
    o.append(link(f"{BASE}/devops-ai-playbook",
                  f'<text x="780" y="548" font-family=\'{MONO}\' font-size="9.5" fill="{t["LINK"]}">playbook ↗</text>'))
    o.append(f'<text x="32" y="568" font-family=\'{MONO}\' font-size="8" fill="{t["ACCENT2"]}">INSPIRED OPS AESTHETIC — NOT AFFILIATED WITH MARVEL</text>')
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, fn in (("light", "hybrid-perimeter.svg"), ("dark", "hybrid-perimeter-dark.svg")):
        path = os.path.join(here, fn)
        with open(path, "w") as f:
            f.write(render(THEMES[name]))
        print("wrote", path)
