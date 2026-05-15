#!/usr/bin/env python3
"""Verify UselessCN OpenGraph image coverage and basic file validity."""
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
errors = []

html_files = sorted(ROOT.glob("*.html"))
for page in html_files:
    text = page.read_text(encoding="utf-8", errors="ignore")
    og = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', text, re.I)
    tw = re.search(r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', text, re.I)
    card = re.search(r'<meta\s+name=["\']twitter:card["\']\s+content=["\']summary_large_image["\']', text, re.I)
    if not og:
        errors.append(f"missing og:image: {page.name}")
        continue
    if not tw:
        errors.append(f"missing twitter:image: {page.name}")
    if not card:
        errors.append(f"missing twitter:card summary_large_image: {page.name}")
    for label, match in [("og", og), ("twitter", tw)]:
        if not match:
            continue
        url = match.group(1)
        parsed = urlparse(url)
        if parsed.netloc != "uselesscn.cyou":
            errors.append(f"{page.name} {label} image is not canonical domain: {url}")
            continue
        local = ROOT / parsed.path.lstrip("/")
        if not local.exists():
            errors.append(f"{page.name} {label} image file missing: {local}")
            continue
        try:
            with Image.open(local) as img:
                if img.size != (1200, 630):
                    errors.append(f"{local} unexpected size {img.size}")
                if img.format != "PNG":
                    errors.append(f"{local} unexpected format {img.format}")
        except Exception as exc:
            errors.append(f"{local} unreadable image: {exc}")

if errors:
    print("Image verification failed:")
    for e in errors:
        print("-", e)
    sys.exit(1)
print(f"Image verification passed: {len(html_files)} pages have valid OG/Twitter PNG images")
