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

prank_page_path = ROOT / "funny-websites-to-prank-friends.html"
require(prank_page_path.exists(), "funny prank friends SEO page exists")
if prank_page_path.exists():
    prank_page = prank_page_path.read_text(encoding="utf-8")
    for phrase in [
        "Funny Websites to Prank Friends",
        "safe silly websites to send friends",
        "Quick safety checklist",
        "FAQPage",
        "Sponsor slot",
        "Random Generator",
    ]:
        require(phrase in prank_page, f"funny prank friends page contains: {phrase}")
    require("https://uselesscn.cyou/funny-websites-to-prank-friends.html" in sitemap, "sitemap includes funny prank friends page")
    require("Funny websites to prank friends" in llms_text, "llms.txt includes funny prank friends page")
    index_text = (ROOT / "index.html").read_text(encoding="utf-8")
    require("funny-websites-to-prank-friends.html" in index_text, "homepage links funny prank friends page")

ambient_page_path = ROOT / "ambient-visual-websites.html"
require(ambient_page_path.exists(), "ambient visual SEO page exists")
if ambient_page_path.exists():
    ambient_page = ambient_page_path.read_text(encoding="utf-8")
    for phrase in [
        "Ambient Visual Websites for Calm Browser Breaks",
        "Curated ambient visual examples",
        "Slow Roads",
        "Oimo Life",
        "FAQPage",
        "Random Generator",
    ]:
        require(phrase in ambient_page, f"ambient visual page contains: {phrase}")
    require("https://uselesscn.cyou/ambient-visual-websites.html" in sitemap, "sitemap includes ambient visual page")
    require("Ambient visual websites" in llms_text, "llms.txt includes ambient visual page")
    index_text = (ROOT / "index.html").read_text(encoding="utf-8")
    require("ambient-visual-websites.html" in index_text, "homepage links ambient visual page")

for new_site_id in ["slow-roads", "oimo-life", "google-gravity-mrdoob"]:
    require(any(s.get("id") == new_site_id for s in sites), f"site pool includes {new_site_id}")
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
require("ai-input=yes" in robots and "ai-train=no" in robots, "robots declares AI search input allowed and AI training reserved")

if errors:
    print("GEO verification failed:")
    for e in errors:
        print("-", e)
    sys.exit(1)
print(f"GEO verification passed: {len(checks)} checks")
