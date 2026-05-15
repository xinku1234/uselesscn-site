#!/usr/bin/env python3
"""Generate playful OpenGraph PNG images and wire social meta tags."""
from __future__ import annotations

from pathlib import Path
import hashlib
import html
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og"
BASE = "https://uselesscn.cyou/assets/og"
OUT.mkdir(parents=True, exist_ok=True)

PAGE_CONFIG = {
    "index.html": ("TAKE ME TO A USELESS WEBSITE", "One button. Infinite boredom relief.", "home"),
    "sites.html": ("COLLECTED USELESS WEBSITES", "Browse weird, funny, pointless links.", "sites"),
    "useless-websites.html": ("USELESS WEBSITES", "Pointless but fun websites for short breaks.", "useless-websites"),
    "random-website-generator.html": ("RANDOM WEBSITE GENERATOR", "Open a weird site in one click.", "random-website-generator"),
    "weird-websites.html": ("WEIRD WEBSITES", "Strange web toys and odd internet experiments.", "weird-websites"),
    "fun-websites.html": ("FUN WEBSITES", "Tiny web distractions for when you are bored.", "fun-websites"),
    "bored-websites.html": ("WEBSITES TO VISIT WHEN BORED", "Quick boredom breaks from the weird internet.", "bored-websites"),
    "pointless-websites.html": ("POINTLESS WEBSITES", "Useless, silly, oddly satisfying links.", "pointless-websites"),
    "websites-like-the-useless-web.html": ("WEBSITES LIKE THE USELESS WEB", "A curated random-button alternative.", "websites-like-the-useless-web"),
    "cool-websites.html": ("COOL WEBSITES", "Interactive browser toys worth a click.", "cool-websites"),
    "interactive-websites.html": ("INTERACTIVE WEBSITES", "Click, drag, play, and discover.", "interactive-websites"),
    "quick-online-games.html": ("QUICK ONLINE GAMES", "Tiny browser games for instant breaks.", "quick-online-games"),
    "internet-time-wasters.html": ("INTERNET TIME WASTERS", "Delightful distractions for a few minutes.", "internet-time-wasters"),
    "online-boredom-cure.html": ("ONLINE BOREDOM CURE", "Random fun websites for a reset.", "online-boredom-cure"),
    "fun-sites-for-boredom.html": ("FUN SITES FOR BOREDOM", "Weird links to open now.", "fun-sites-for-boredom"),
    "best-useless-websites.html": ("BEST USELESS WEBSITES", "A playful list of pointless internet classics.", "best-useless-websites"),
    "weird-internet.html": ("THE WEIRD INTERNET", "Strange sites, odd toys, memorable clicks.", "weird-internet"),
    "about.html": ("ABOUT USELESSCN", "A tiny portal for pointless but fun websites.", "about"),
    "submit.html": ("SUBMIT A USELESS WEBSITE", "Send a weird, fun, pointless link.", "submit"),
    "advertise.html": ("ADVERTISE ON USELESSCN", "Sponsor a playful boredom-break portal.", "advertise"),
    "contact.html": ("CONTACT USELESSCN", "Questions, links, sponsors, weird ideas.", "contact"),
    "privacy.html": ("USELESSCN PRIVACY", "Simple privacy notes for a simple site.", "privacy"),
    "terms.html": ("USELESSCN TERMS", "Basic rules for pointless browsing.", "terms"),
    "cookie-policy.html": ("USELESSCN COOKIE POLICY", "Cookie notes for a tiny web portal.", "cookie-policy"),
}

COLORS = [
    (126, 87, 255),
    (0, 229, 255),
    (255, 214, 0),
    (255, 83, 178),
    (35, 255, 153),
]

def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size=size)
    return ImageFont.load_default()

TITLE_FONT = font(68, True)
SUB_FONT = font(32, False)
SMALL_FONT = font(25, True)
BUTTON_FONT = font(44, True)


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], fnt, fill, width: int, line_gap=10):
    lines = []
    for para in text.split("\n"):
        current = ""
        for word in para.split():
            test = (current + " " + word).strip()
            if draw.textbbox((0, 0), test, font=fnt)[2] <= width or not current:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
    return y


def make_image(title: str, subtitle: str, slug: str):
    w, h = 1200, 630
    seed = int(hashlib.sha1(slug.encode()).hexdigest()[:8], 16)
    bg1 = (18 + seed % 20, 14, 36 + seed % 30)
    bg2 = (5, 20 + seed % 25, 42)
    img = Image.new("RGB", (w, h), bg1)
    px = img.load()
    for y in range(h):
        ratio = y / h
        for x in range(w):
            if x % 4 == 0 and y % 4 == 0:
                r = int(bg1[0] * (1-ratio) + bg2[0] * ratio)
                g = int(bg1[1] * (1-ratio) + bg2[1] * ratio)
                b = int(bg1[2] * (1-ratio) + bg2[2] * ratio)
                for yy in range(y, min(y+4, h)):
                    for xx in range(x, min(x+4, w)):
                        px[xx, yy] = (r, g, b)
    d = ImageDraw.Draw(img)
    # Grid and decorative windows
    for x in range(0, w, 60):
        d.line((x, 0, x, h), fill=(255,255,255,18), width=1)
    for y in range(0, h, 60):
        d.line((0, y, w, y), fill=(255,255,255,18), width=1)
    for i in range(9):
        c = COLORS[(seed + i) % len(COLORS)]
        x = 760 + ((seed // (i+1)) % 310)
        y = 70 + ((seed // (i+3)) % 420)
        ww = 80 + ((seed // (i+5)) % 140)
        hh = 45 + ((seed // (i+7)) % 95)
        d.rounded_rectangle((x, y, x+ww, y+hh), radius=16, outline=c, width=3)
        d.rectangle((x+12, y+14, x+ww-12, y+18), fill=c)
    # Card
    d.rounded_rectangle((70, 70, 830, 560), radius=38, fill=(255,255,255), outline=(0,229,255), width=6)
    d.text((105, 105), "UselessCN", font=SMALL_FONT, fill=(126,87,255))
    y = draw_wrapped(d, title, (105, 170), TITLE_FONT, (22,18,44), 640, line_gap=8)
    y += 18
    draw_wrapped(d, subtitle, (105, y), SUB_FONT, (55,53,75), 620, line_gap=8)
    d.rounded_rectangle((105, 455, 350, 535), radius=40, fill=(255,83,178), outline=(22,18,44), width=4)
    d.text((142, 468), "PLEASE", font=BUTTON_FONT, fill=(255,255,255))
    d.text((382, 480), "→ pointless but fun", font=SMALL_FONT, fill=(22,18,44))
    out = OUT / f"{slug}.png"
    img.save(out, "PNG", optimize=True)
    return out


def set_meta(html_text: str, prop_or_name: str, key: str, content: str) -> str:
    attr = "property" if prop_or_name == "property" else "name"
    pattern = re.compile(rf'<meta\s+{attr}=["\']{re.escape(key)}["\'][^>]*>', re.I)
    tag = f'<meta {attr}="{key}" content="{html.escape(content, quote=True)}">'
    if pattern.search(html_text):
        return pattern.sub(tag, html_text, count=1)
    return html_text.replace("</head>", f"  {tag}\n</head>", 1)


def main():
    generated = []
    for filename, (title, subtitle, slug) in PAGE_CONFIG.items():
        path = ROOT / filename
        if not path.exists():
            continue
        out = make_image(title, subtitle, slug)
        generated.append(out)
        image_url = f"{BASE}/{out.name}"
        text = path.read_text(encoding="utf-8")
        text = set_meta(text, "property", "og:image", image_url)
        text = set_meta(text, "name", "twitter:card", "summary_large_image")
        text = set_meta(text, "name", "twitter:image", image_url)
        path.write_text(text, encoding="utf-8")
    print(f"Generated {len(generated)} OpenGraph images")
    for p in generated:
        print(p.relative_to(ROOT), p.stat().st_size)

if __name__ == "__main__":
    main()
