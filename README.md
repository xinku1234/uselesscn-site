# UselessCN

A small static micro-entertainment site inspired by The Useless Web: one obvious button that opens a random weird, funny, beautifully pointless website in a new tab.

## Local preview

```bash
cd /home/admin/useless-web-site
python3 -m http.server 57941 --bind 127.0.0.1
```

## Structure

- `index.html` — minimal random-button homepage
- `sites.html` — searchable directory of collected useless sites
- `submit.html` — mailto-based submission page
- `about.html` — project explanation
- `data/sites.json` — canonical site pool
- `scripts/update_daily.py` — daily health check and featured pick updater

## Deployment

Static files can be deployed directly to Cloudflare Pages. Current Pages project: `uselesscn`.
