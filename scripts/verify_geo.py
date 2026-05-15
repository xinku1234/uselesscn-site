#!/usr/bin/env python3
"""Lightweight GEO/AI-search verification for the static UselessCN site."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

checks = []
errors = []

def require(condition, message):
    checks.append(message)
    if not condition:
        errors.append(message)

llms = ROOT / "llms.txt"
require(llms.exists() and llms.stat().st_size > 800, "llms.txt exists and is substantial")
llms_text = llms.read_text(encoding="utf-8") if llms.exists() else ""
for phrase in [
    "UselessCN is an English-first portal",
    "Random website generator guide",
    "websites like The Useless Web",
    "pointless but fun",
]:
    require(phrase in llms_text, f"llms.txt contains: {phrase}")

random_page = (ROOT / "random-website-generator.html").read_text(encoding="utf-8")
for phrase in [
    "Random website generator FAQ",
    "How does the UselessCN random website generator work?",
    "What kind of websites can I discover here?",
    "FAQPage",
    "https://schema.org",
]:
    require(phrase in random_page, f"random page contains: {phrase}")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
require("https://uselesscn.cyou/random-website-generator.html" in sitemap, "sitemap includes random generator page")
require("<lastmod>2026-05-15</lastmod>" in sitemap, "sitemap lastmod updated to 2026-05-15")

for path in ROOT.glob("*.html"):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    require(not re.search(r"[\u4e00-\u9fff]", txt), f"no public Chinese residue in {path.name}")

sites = json.loads((ROOT / "data/sites.json").read_text(encoding="utf-8"))
require(len(sites) >= 30, "site pool has at least 30 entries")

if errors:
    print("GEO verification failed:")
    for e in errors:
        print("-", e)
    sys.exit(1)
print(f"GEO verification passed: {len(checks)} checks")
