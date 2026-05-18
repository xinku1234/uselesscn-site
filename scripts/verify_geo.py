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
require("<lastmod>" in sitemap, "sitemap includes lastmod values")

for path in ROOT.glob("*.html"):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    require(not re.search(r"[\u4e00-\u9fff]", txt), f"no public Chinese residue in {path.name}")

sites = json.loads((ROOT / "data/sites.json").read_text(encoding="utf-8"))
require(len(sites) >= 30, "site pool has at least 30 entries")

for page in ["weird-browser-toys.html", "websites-to-waste-time.html", "random-fun-websites.html"]:
    page_text = (ROOT / page).read_text(encoding="utf-8")
    require("application/ld+json" in page_text, f"{page} has structured data")
    require("https://uselesscn.cyou/" + page in sitemap, f"sitemap includes {page}")
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
require("ai-input=yes" in robots and "ai-train=no" in robots, "robots declares AI search input allowed and AI training reserved")

if errors:
    print("GEO verification failed:")
    for e in errors:
        print("-", e)
    sys.exit(1)
print(f"GEO verification passed: {len(checks)} checks")
