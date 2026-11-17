"""Generates the profile README SVGs in the oondraa-web visual language.

Fonts and images are embedded as data URIs so the SVGs render inside GitHub's <img>.
Usage: python -I build.py <oondraa-web dir> <output assets dir>
"""
import base64
import os
import sys
from html import escape

WEB, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def data_uri(path):
    ext = path.rsplit(".", 1)[1].lower()
    mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg", "woff2": "font/woff2"}[ext]
    return f"data:{mime};base64,{b64(path)}"


FONT_CSS = f"""
@font-face {{ font-family: G; font-weight: 100 900; src: url({data_uri(os.path.join(WEB, 'fonts/geist-latin-ext-wght-normal.woff2'))}) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
@font-face {{ font-family: G; font-weight: 100 900; src: url({data_uri(os.path.join(WEB, 'fonts/geist-latin-wght-normal.woff2'))}) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
text {{ font-family: G, 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif; }}
"""

ACCENT, ACCENT_DARK = "#1760f0", "#5b93ff"
THEMES = {
    "light": dict(bg="#e9e9ec", bg2="#dfdfe4", ink="#0c0c10", muted="#64646e", line="rgba(12,12,16,0.14)", accent=ACCENT),
    "dark": dict(bg="#0c0c10", bg2="#16161c", ink="#f1f1f3", muted="#8d8d97", line="rgba(241,241,243,0.14)", accent=ACCENT_DARK),
}


def svg(w, h, body, extra_css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
            f'<style>{FONT_CSS}{extra_css}</style>{body}</svg>')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# ---------- Header: halftone wordmark, like the portfolio hero ----------
def header(t):
    c = THEMES[t]
    W, H = 1280, 440
    cell = 9
    body = f"""
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <pattern id="dots" width="{cell}" height="{cell}" patternUnits="userSpaceOnUse">
    <circle cx="{cell/2}" cy="{cell/2}" r="3.15" fill="{c['ink']}"/>
  </pattern>
  <pattern id="dotsA" width="{cell}" height="{cell}" patternUnits="userSpaceOnUse">
    <circle cx="{cell/2}" cy="{cell/2}" r="3.15" fill="{c['accent']}"/>
  </pattern>
  <mask id="word" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
    <text x="44" y="300" font-size="296" font-weight="600" letter-spacing="-17" fill="#fff">oondraa</text>
  </mask>
  <mask id="dot" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
    <rect x="1124" y="236" width="64" height="64" fill="#fff"/>
  </mask>
  <radialGradient id="tint" cx="0.83" cy="0.62" r="0.3">
    <stop offset="0" stop-color="{c['accent']}" stop-opacity="0.9"/>
    <stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/>
  </radialGradient>
  <mask id="tintm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
    <rect width="{W}" height="{H}" fill="url(#tint)"/>
  </mask>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{c['bg']}"/>
  <g class="fly">
    <g mask="url(#word)"><rect width="{W}" height="{H}" fill="url(#dots)"/>
      <g mask="url(#tintm)"><rect width="{W}" height="{H}" fill="url(#dotsA)"/></g></g>
    <g mask="url(#dot)"><rect width="{W}" height="{H}" fill="url(#dotsA)"/></g>
  </g>
  <text x="44" y="62" font-size="24" font-weight="600" letter-spacing="-1" fill="{c['ink']}">oondraa<tspan fill="{c['accent']}">.</tspan></text>
  <text x="{W-44}" y="58" text-anchor="end" font-size="14" font-weight="500" letter-spacing="1.3" fill="{c['muted']}">DEVELOPER &amp; DESIGNER · HRADEC KRÁLOVÉ</text>
  <text x="44" y="372" font-size="38" font-weight="600" letter-spacing="-1.7" fill="{c['ink']}">Ondřej Zajíček</text>
  <text x="44" y="404" font-size="21" letter-spacing="-0.4" fill="{c['muted']}">I build software I want to use myself.</text>
  <text x="{W-60}" y="400" text-anchor="end" font-size="14" font-weight="500" letter-spacing="1.3" fill="{c['muted']}">SCROLL</text>
  <line x1="{W-44}" y1="350" x2="{W-44}" y2="404" stroke="{c['muted']}" stroke-width="1.5"/>
  <line class="cue" x1="{W-44}" y1="350" x2="{W-44}" y2="370" stroke="{c['accent']}" stroke-width="1.5"/>
</g>"""
    css = """
.fly { animation: fly 1.4s cubic-bezier(0.22,1,0.36,1) both; }
@keyframes fly { from { transform: translateY(46px); opacity: 0; } to { transform: none; opacity: 1; } }
.cue { animation: cue 2.4s cubic-bezier(0.22,1,0.36,1) infinite; }
@keyframes cue { 0% { transform: translateY(-20px); opacity: 0; } 30% { opacity: 1; } 100% { transform: translateY(54px); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .fly, .cue { animation: none; } }
"""
    write(f"header-{t}.svg", svg(W, H, body, css, "oondraa. Ondřej Zajíček, developer and designer. I build software I want to use myself."))


# ---------- Section heads: big title + blue counter + hairline, like .sec-head ----------
SECTIONS = [
    ("about", "About", "01"),
    ("work", "Selected work", "04"),
    ("stack", "Stack", "02"),
    ("activity", "Activity", "03"),
]


def section(t, key, title, kicker):
    c = THEMES[t]
    W, H = 1280, 118
    body = f"""
<text x="0" y="86" font-size="84" font-weight="600" letter-spacing="-5" fill="{c['ink']}">{escape(title)}</text>
<text x="{W}" y="84" text-anchor="end" font-size="16" font-weight="500" letter-spacing="1.4" fill="{c['accent']}">{escape(kicker)}</text>
<rect x="0" y="{H-1}" width="{W}" height="1" fill="{c['line']}"/>"""
    write(f"sec-{key}-{t}.svg", svg(W, H, body, label=title))


# ---------- Project cards: bar, icon + name, poster, like .project ----------
PROJECTS = [
    ("sis", "01", "OpenSISAKHK", "Web app · 2026", "sis-icon.svg", "sis-poster.jpg"),
    ("ozbeat", "02", "OZBEAT", "Desktop app · 2026", "ozbeat-icon.png", "ozbeat-poster.jpg"),
    ("hud", "03", "ClaudeHUD", "Desktop app · 2026", "hud-icon.svg", "hud-poster.jpg"),
    ("sosac", "04", "OpenSosacTV", "Web + Windows", "sosac-icon.svg", "sosac-poster.jpg"),
]


def card(t, key, n, name, kind, icon, poster):
    c = THEMES[t]
    W = 640
    MY, MH = 112, 480
    H = MY + MH
    body = f"""
<defs>
  <clipPath id="ic"><rect x="0" y="44" width="48" height="48" rx="12"/></clipPath>
  <clipPath id="md"><rect x="0" y="{MY}" width="{W}" height="{MH}" rx="16"/></clipPath>
</defs>
<text x="0" y="20" font-size="16" font-weight="600" fill="{c['accent']}">{n}</text>
<rect x="30" y="14" width="56" height="1.5" fill="{c['accent']}" opacity="0.45"/>
<text x="{W}" y="20" text-anchor="end" font-size="16" fill="{c['muted']}">{escape(kind)}</text>
<image x="0" y="44" width="48" height="48" clip-path="url(#ic)" preserveAspectRatio="xMidYMid slice" href="{data_uri(os.path.join(WEB, 'assets', icon))}"/>
<text x="64" y="81" font-size="40" font-weight="600" letter-spacing="-1.6" fill="{c['ink']}">{escape(name)}</text>
<rect x="0" y="{MY}" width="{W}" height="{MH}" rx="16" fill="{c['bg2']}"/>
<image x="0" y="{MY}" width="{W}" height="{MH}" clip-path="url(#md)" preserveAspectRatio="xMidYMid slice" href="{data_uri(os.path.join(WEB, 'assets', poster))}"/>"""
    write(f"card-{key}-{t}.svg", svg(W, H, body, label=f"{n} {name}, {kind}"))


# ---------- Footer: the dark contact block ----------
def footer():
    W, H = 1280, 400
    rows = "".join(
        f'<text x="{-60 - (i % 2) * 180}" y="{70 + i * 78}" font-size="96" font-weight="600" letter-spacing="-5" fill="#f1f1f3" opacity="0.035">OONDRAA OONDRAA OONDRAA OONDRAA</text>'
        for i in range(6))
    body = f"""
<defs><clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <radialGradient id="glow" cx="0.78" cy="0.15" r="0.6"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.32"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient></defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="#0c0c10"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  {rows}
  <text x="48" y="86" font-size="15" font-weight="500" letter-spacing="1.4" fill="#8d8d97">GOT AN IDEA, A JOB OR JUST A QUESTION?</text>
  <text x="38" y="262" font-size="188" font-weight="600" letter-spacing="-12" fill="#f1f1f3">Say hi<tspan class="arrow" dx="34" fill="{ACCENT_DARK}">→</tspan></text>
  <rect x="48" y="320" width="{W-96}" height="1" fill="rgba(241,241,243,0.14)"/>
  <text x="48" y="360" font-size="17" font-weight="500" fill="#f1f1f3">GitHub<tspan dx="28">LinkedIn</tspan><tspan dx="28">OZDIGITAL</tspan></text>
  <text x="{W-48}" y="360" text-anchor="end" font-size="15" fill="#8d8d97">© 2026 Ondřej Zajíček</text>
</g>"""
    write("footer.svg", svg(W, H, body, label="Say hi. GitHub, LinkedIn, OZDIGITAL."))


for t in THEMES:
    header(t)
    for s in SECTIONS:
        section(t, *s)
    for p in PROJECTS:
        card(t, *p)
footer()

# Preview page for a visual check
items = sorted(os.listdir(OUT))
with open(os.path.join(OUT, "..", "preview.html"), "w", encoding="utf-8") as f:
    f.write("<!doctype html><body style='margin:0;font-family:sans-serif'>")
    for t, bg in (("light", "#ffffff"), ("dark", "#0d1117")):
        f.write(f"<div style='background:{bg};padding:24px;width:880px'>")
        for name in [f"header-{t}.svg"] + [f"sec-{k}-{t}.svg" for k, *_ in SECTIONS[:2]]:
            f.write(f"<img src='assets/{name}' style='width:100%;display:block;margin:0 0 20px'>")
        f.write("<div style='display:flex;gap:16px'>" + "".join(
            f"<img src='assets/card-{k}-{t}.svg' style='width:50%'>" for k in ("sis", "ozbeat")) + "</div>")
        f.write("<img src='assets/footer.svg' style='width:100%;display:block;margin-top:20px'></div>")
    f.write("</body>")
print("\n".join(items))
