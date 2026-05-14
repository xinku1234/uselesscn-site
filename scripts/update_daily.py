#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily updater for 摸鱼传送门.

What it does:
1. Read data/sites.json.
2. Check whether each URL is reachable.
3. Rotate a deterministic daily pick.
4. Write data/meta.json.
5. Write reports/YYYY-MM-DD.md.

This is designed for a static site. After it runs in a git/Cloudflare Pages repo,
commit+push can trigger redeploy. Without git, it still keeps local data fresh.
"""
import datetime as _dt
import json
import os
import random
import ssl
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SITES_PATH = ROOT / "data" / "sites.json"
META_PATH = ROOT / "data" / "meta.json"
REPORT_DIR = ROOT / "reports"
UA = "Mozilla/5.0 (compatible; MoyuPortalBot/1.0; +https://example.com/bot)"
TIMEOUT = 8


def load_sites():
    return json.loads(SITES_PATH.read_text(encoding="utf-8"))


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_url(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    ctx = ssl.create_default_context()
    start = time.time()
    try:
        with urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            code = getattr(resp, "status", 200)
            elapsed = round((time.time() - start) * 1000)
            if 200 <= code < 400:
                return "alive", code, elapsed, ""
            return "warning", code, elapsed, "non-2xx/3xx status"
    except HTTPError as e:
        elapsed = round((time.time() - start) * 1000)
        # 403/429 may mean bot protection, not necessarily dead.
        if e.code in (401, 403, 429):
            return "blocked", e.code, elapsed, "blocked or rate-limited"
        return "dead", e.code, elapsed, str(e)[:120]
    except URLError as e:
        elapsed = round((time.time() - start) * 1000)
        return "dead", 0, elapsed, str(e.reason)[:120]
    except Exception as e:
        elapsed = round((time.time() - start) * 1000)
        return "dead", 0, elapsed, str(e)[:120]


def daily_pick(sites, today):
    candidates = [s for s in sites if s.get("status") in ("alive", "blocked", "warning", "unknown")]
    if not candidates:
        candidates = sites[:]
    random.seed(today.strftime("%Y%m%d"))
    return random.choice(candidates) if candidates else None


def make_report(today, sites, pick):
    total = len(sites)
    alive = sum(1 for s in sites if s.get("status") == "alive")
    blocked = sum(1 for s in sites if s.get("status") == "blocked")
    dead = sum(1 for s in sites if s.get("status") == "dead")
    warning = sum(1 for s in sites if s.get("status") == "warning")
    lines = [
        "# 摸鱼传送门日报 - %s" % today.isoformat(),
        "",
        "## 今日概览",
        "",
        "- 收录总数：%d" % total,
        "- 可访问：%d" % alive,
        "- 被拦截/限流但可能可访问：%d" % blocked,
        "- 警告：%d" % warning,
        "- 疑似失效：%d" % dead,
        "",
    ]
    if pick:
        lines += [
            "## 今日推荐",
            "",
            "- %s" % pick.get("title"),
            "- %s" % pick.get("url"),
            "- %s" % pick.get("description", ""),
            "",
        ]
    bad = [s for s in sites if s.get("status") in ("dead", "warning")]
    lines += ["## 需要人工看一眼", ""]
    if bad:
        for s in bad:
            lines.append("- [%s](%s)：%s %s" % (s.get("title"), s.get("url"), s.get("status"), s.get("last_error", "")))
    else:
        lines.append("- 暂无。")
    lines += ["", "## 下一步建议", "", "- 每天新增 3-5 个候选网站，先人工审核再加入 data/sites.json。", "- 上线后把投稿表单接到邮箱、Airtable 或 Supabase。", "- 每周挑 10 个做一篇 SEO 周榜。", ""]
    return "\n".join(lines)


def maybe_git_commit(report_path):
    if not (ROOT / ".git").exists():
        return "未检测到 git 仓库，已跳过 commit/push。"
    import subprocess
    cmds = [
        ["git", "add", "data/sites.json", "data/meta.json", str(report_path.relative_to(ROOT))],
        ["git", "commit", "-m", "daily useless web update"],
        ["git", "push"],
    ]
    outputs = []
    for cmd in cmds:
        p = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        outputs.append("$ " + " ".join(cmd) + "\n" + p.stdout[-1200:])
        if p.returncode != 0 and cmd[1] != "commit":
            break
    return "\n".join(outputs)


def main():
    today = _dt.date.today()
    now = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    sites = load_sites()
    for s in sites:
        status, code, ms, err = check_url(s["url"])
        s["status"] = status
        s["last_http_code"] = code
        s["last_latency_ms"] = ms
        s["last_checked_at"] = now
        if err:
            s["last_error"] = err
        else:
            s.pop("last_error", None)
    pick = daily_pick(sites, today)
    meta = {
        "updated_at": now,
        "total_sites": len(sites),
        "alive_sites": sum(1 for s in sites if s.get("status") == "alive"),
        "blocked_sites": sum(1 for s in sites if s.get("status") == "blocked"),
        "dead_sites": sum(1 for s in sites if s.get("status") == "dead"),
        "today_pick": pick.get("id") if pick else None,
        "today_pick_title": pick.get("title") if pick else None,
    }
    save_json(SITES_PATH, sites)
    save_json(META_PATH, meta)
    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / (today.isoformat() + ".md")
    report = make_report(today, sites, pick)
    report_path.write_text(report, encoding="utf-8")
    git_note = maybe_git_commit(report_path)
    print(report)
    print("\n---\n" + git_note)


if __name__ == "__main__":
    main()
