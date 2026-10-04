#!/usr/bin/env python3
"""Re-skin Listening Timeline report HTML files to match the site palette.

The reports ship their own neutral palette in two places:
  1. CSS custom properties (--page, --surface, --ink, ...) for UI chrome
  2. JS theme objects {name:`light`,...} / {name:`dark`,...} for chart axes,
     grid, labels and empty bands (data/series colours are left alone).
This rewrites both to the hugo-academia light/dark colours in
themes/hugo-academia/assets/css/main.css. Idempotent; re-run after
regenerating the reports:

    python3 scripts/retheme-embeds.py static/embeds/listening/*.html
"""
import re, sys

FONT = '"IBM Plex Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
SERIF = '"Lora", "Palatino Linotype", "Book Antiqua", Palatino, Georgia, serif'
# Same Google Fonts the theme loads in baseof.html (subset to what plots use).
FONT_LINK = ('<link id="site-fonts" rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Lora:wght@600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">')
# The reports' CSP blocks web fonts; allow exactly Google Fonts.
CSP_EDITS = [("style-src 'unsafe-inline';", "style-src 'unsafe-inline' https://fonts.googleapis.com;"),
             ("font-src 'none';", "font-src https://fonts.gstatic.com;")]

CSS = {
    "light": {"--page": "#faf7f5", "--surface": "#ffffff", "--ink": "#2d2d2d",
              "--ink-2": "#5a5a5a", "--muted": "#696969", "--line": "#e8e0da",
              "--border": "#d6c9c0", "--accent": "#8f3a3a", "--accent-ink": "#ffffff",
              "--wash": "#8f3a3a12", "--shadow": "0 2px 4px #0000000f"},
    "dark":  {"--page": "#18130f", "--surface": "#221b16", "--ink": "#e8e8e8",
              "--ink-2": "#b8b8b8", "--muted": "#888888", "--line": "#3a2f27",
              "--border": "#4a3d33", "--accent": "#d98a7a", "--accent-ink": "#18130f",
              "--wash": "#d98a7a1f", "--shadow": "none"},
}
JS = {
    "light": {"surface": "#ffffff", "ink": "#2d2d2d", "ink2": "#5a5a5a", "muted": "#696969",
              "grid": "#e8e0da", "axis": "#d6c9c0", "emptyBand": "#f3ede9", "other": "#d6c9c0"},
    "dark":  {"surface": "#221b16", "ink": "#e8e8e8", "ink2": "#b8b8b8", "muted": "#888888",
              "grid": "#3a2f27", "axis": "#4a3d33", "emptyBand": "#1e1712", "other": "#5a4c41"},
}

# Compact the per-series legend ("top 20" list) under the timeline x-axes.
LAYOUT_CSS = (".legend{gap:2px 4px;margin-top:8px}"
              # One type scale for every plot: the co-listening map ships a
              # bigger heading (22px) and labels (13/11.5px) than the timelines.
              ".chart-title{font-family:" + SERIF.replace('"', "'") + ";font-size:18px!important;font-weight:600}"
              ".card svg,.card svg text{font-family:var(--font)}"  # beats the SVG font-family attribute
              ".map-hero svg text[font-size='13']{font-size:12px;font-weight:600}"
              ".map-hero svg text[font-size='11.5']{font-size:11px}"
              # Drop the "2017 – 2026 · Spotify listening, computed locally..." footer.
              ".report-foot{display:none!important}"
              ".legend-item{font-size:11.5px;padding:2px 6px;line-height:1.3}"
              ".legend-value{margin-left:4px}")

def css_block(mode):
    return ";".join(f"{k}:{v}" for k, v in CSS[mode].items())

def patch(src):
    # 1. Append an override stylesheet (replaced on re-run).
    css = (f':root,:root[data-theme=light]{{{css_block("light")};--font:{FONT}}}'
           f'@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{{css_block("dark")}}}}}'
           f':root[data-theme=dark]{{{css_block("dark")}}}' + LAYOUT_CSS)
    tag = f'<style id="site-palette">{css}</style>'
    src = re.sub(r'<style id="site-palette">.*?</style>', '', src, flags=re.S)
    src = re.sub(r'<link id="site-fonts"[^>]*>\n?', '', src)
    for old, new in CSP_EDITS:
        if new not in src:
            src = src.replace(old, new, 1)
    tag = FONT_LINK + tag
    src, n = re.subn(r'</head>', tag + '\n</head>', src, count=1)
    assert n == 1, "no </head>"
    # 2. Chart theme objects in the JS bundle.
    for mode, vals in JS.items():
        m = re.search(r'\{name:`%s`[^{}]*?series:' % mode, src)
        assert m, f"no {mode} theme object"
        block = m.group(0)
        for k, v in vals.items():
            block = re.sub(r'(\b%s:`)#[0-9a-fA-F]{3,8}(`)' % k, r'\g<1>%s\g<2>' % v, block)
        src = src[:m.start()] + block + src[m.end():]
    return src

for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        s = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(patch(s))
    print("patched", path)
