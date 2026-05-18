# UselessCN

UselessCN is an English-first random-button directory for useless websites, weird internet experiments, one-click web toys, quick boredom breaks, oddly satisfying websites, tiny games, ambient sound toys, visual loops, and beautifully pointless browser experiences.

Live site: https://uselesscn.cyou/

## What it does

Press one obvious button and UselessCN opens a curated useless website. If you prefer browsing, the site also includes searchable collections and long-tail guide pages for:

- Useless websites
- Weird websites
- Random fun websites
- One-click web toys
- Oddly satisfying websites
- Quick boredom break websites
- Browser toys and tiny online games

The project is intentionally lightweight: static HTML, JSON data, no login wall, no heavy app shell, and no serious productivity claims.

## Useful links

- Homepage: https://uselesscn.cyou/
- Full collection: https://uselesscn.cyou/sites.html
- Random website generator guide: https://uselesscn.cyou/random-website-generator.html
- Quick boredom breaks: https://uselesscn.cyou/quick-boredom-breaks.html
- One-click web toys: https://uselesscn.cyou/one-click-web-toys.html
- Oddly satisfying websites: https://uselesscn.cyou/oddly-satisfying-websites.html
- AI/search reference: https://uselesscn.cyou/llms.txt
- Sitemap: https://uselesscn.cyou/sitemap.xml

## Current inventory

The canonical collection lives in `data/sites.json`. The site is maintained by a daily updater that checks link status, refreshes `data/meta.json`, rotates a daily pick, and produces a short ops report.

## Local preview

```bash
cd /home/admin/useless-web-site
python3 -m http.server 57941 --bind 127.0.0.1
```

Then open `http://127.0.0.1:57941/`.

## Structure

- `index.html` — minimal one-button homepage
- `sites.html` — searchable directory of collected useless sites
- `submit.html` — mailto-based submission page
- `about.html` — project explanation
- `data/sites.json` — canonical site pool
- `data/meta.json` — daily status snapshot
- `llms.txt` — AI/search grounding summary
- `sitemap.xml` — public sitemap
- `scripts/update_daily.py` — daily health check and featured pick updater
- `scripts/verify_geo.py` — lightweight SEO/GEO verification
- `outreach/` — link-building and launch copy assets

## Deployment

Static files can be deployed directly to Cloudflare Pages. Current Pages project: `uselesscn`.

## Short description for directories

UselessCN is a one-button portal for random useless websites, weird browser toys, quick boredom breaks, oddly satisfying web experiments, and beautifully pointless internet fun.
