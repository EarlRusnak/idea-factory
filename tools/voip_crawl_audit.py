#!/usr/bin/env python3
"""voip_crawl_audit.py — read-only crawl-block audit for voip-int.com (or any site).

Answers, with evidence, the questions Search Console raised on 2026-07-18:
  * which sitemap URLs are blocked by robots.txt, noindexed, redirecting, or non-200
  * which "must rank" URLs are missing from the sitemap or carry a block
  * which "must not rank" URLs are only robots-blocked (so Google can never see a noindex
    and keeps them as "Indexed, though blocked by robots.txt")

Stdlib only. Never writes to the site. Run from any machine that can reach the domain:

    python3 tools/voip_crawl_audit.py                      # markdown report to stdout
    python3 tools/voip_crawl_audit.py --out report.md --csv urls.csv
    python3 tools/voip_crawl_audit.py --odoo               # also read Odoo page flags (read-only)

--odoo reads ODOO_URL, ODOO_DB, ODOO_LOGIN, ODOO_KEY from the environment and lists
website.page records (url, is_published, website_indexed), website.rewrite records and the
website's custom robots text, then cross-checks them against the decision list below.
"""
import argparse
import csv
import gzip
import io
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

BASE = "https://voip-int.com"
UA = "Mozilla/5.0 (compatible; VoIPIntCrawlAudit/1.0; +https://voip-int.com/contact)"
GOOGLEBOT = "Googlebot"
WEBSITE_ID = 5

# ---------------------------------------------------------------------------
# Decision list (see processes/voip-int-crawl-unblock.md). Paths only.
# ---------------------------------------------------------------------------
MUST_RANK = [
    "/", "/pricing", "/phone-service", "/pro-mobile", "/ai-receptionist", "/vfax",
    "/sip-trunking", "/mitel-replacement", "/features", "/integrations",
    "/integrations/appfolio", "/integrations/buildium", "/integrations/clio",
    "/integrations/follow-up-boss", "/integrations/gohighlevel", "/integrations/housecall-pro",
    "/integrations/jobber", "/integrations/microsoft-teams", "/integrations/rent-manager",
    "/integrations/servicetitan",
    "/property-management", "/field-service", "/sales-teams", "/multi-location",
    "/healthcare-practice-phone-system", "/dental-practice-phone-system",
    "/wellness-clinic-phone-system", "/legal-firm-phone-system", "/real-estate-phone-system",
    "/replace-cell-phone-allowance", "/vs", "/vs/8x8", "/vs/nextiva", "/vs/ooma", "/vs/ringcentral",
    "/locations", "/apopka-business-phone", "/central-florida-multi-location", "/clermont-business-phone",
    "/daytona-business-phone", "/downtown-orlando-business-phone", "/jacksonville-business-phone",
    "/kissimmee-business-phone", "/lake-city-business-phone", "/lake-mary-business-phone",
    "/lake-nona-business-phone", "/maitland-altamonte-business-phone", "/ocoee-business-phone",
    "/orlando-business-phone", "/ormond-beach-business-phone", "/sanford-business-phone",
    "/st-cloud-business-phone", "/tampa-business-phone", "/winter-garden-business-phone",
    "/winter-park-business-phone",
    "/hardware", "/about", "/contact", "/faq", "/get-started", "/blog",
    "/call-retrieve", "/message-waiting-indicator-mwi",
]
# Indexable but not worth chasing rankings for; only flagged if blocked.
MAY_RANK = ["/privacy", "/aup", "/cookie-policy", "/terms-of-service"]
# Must never appear in Google. Mechanism must be noindex (meta or X-Robots-Tag), not only robots.txt.
MUST_NOT_RANK = ["/web/login", "/my", "/get-started/thank-you", "/contactus", "/shop"]
# Legacy blog namespace: every URL should 301 (exact rewrite or catch-all to /blog).
LEGACY_BLOG_PREFIX = "/blog/voip-international-blog-posts-2"

ctx = ssl.create_default_context()


class Head(HTMLParser):
    """Collects <title>, meta robots/googlebot, canonical from the <head>."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.robots = []
        self.canonical = ""
        self._in_title = False
        self._done = False

    def handle_starttag(self, tag, attrs):
        if self._done:
            return
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and (a.get("name") or "").lower() in ("robots", "googlebot"):
            self.robots.append(f"{a.get('name').lower()}={a.get('content', '')}")
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "body":
            self._done = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "head":
            self._done = True

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()


def fetch(url, ua=UA, follow=False, timeout=25):
    """GET without following redirects. Returns dict(status, headers, body, location, error)."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    handlers = [] if follow else [NoRedirect()]
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), *handlers)
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*",
                                               "Accept-Encoding": "gzip, identity"})
    out = {"url": url, "status": 0, "headers": {}, "body": b"", "location": "", "error": ""}
    try:
        with opener.open(req, timeout=timeout) as r:
            out["status"] = r.status
            out["headers"] = {k.lower(): v for k, v in r.headers.items()}
            out["body"] = r.read()
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["headers"] = {k.lower(): v for k, v in e.headers.items()}
        out["location"] = e.headers.get("Location", "") or ""
        try:
            out["body"] = e.read()
        except Exception:
            pass
    except Exception as e:  # DNS, TLS, timeout
        out["error"] = f"{type(e).__name__}: {e}"
    if out["headers"].get("content-encoding") == "gzip" and out["body"][:2] == b"\x1f\x8b":
        out["body"] = gzip.decompress(out["body"])
    elif out["body"][:2] == b"\x1f\x8b":
        out["body"] = gzip.decompress(out["body"])
    return out


def load_robots(base):
    r = fetch(base + "/robots.txt")
    text = r["body"].decode("utf-8", "replace") if r["status"] == 200 else ""
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    return r, text, rp


def load_sitemap(url, seen=None, depth=0):
    """Returns list of (loc, lastmod, source_sitemap). Follows sitemap indexes."""
    seen = seen if seen is not None else set()
    if url in seen or depth > 3:
        return [], []
    seen.add(url)
    r = fetch(url, follow=True)
    problems = []
    if r["error"] or r["status"] != 200:
        problems.append(f"sitemap {url}: status {r['status']} {r['error']}")
        return [], problems
    body = r["body"]
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        problems.append(f"sitemap {url}: XML parse error {e} (first bytes: {body[:80]!r})")
        return [], problems
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tag = root.tag.split("}")[-1]
    urls = []
    if tag == "sitemapindex":
        for s in root.findall("sm:sitemap", ns):
            loc = (s.findtext("sm:loc", default="", namespaces=ns) or "").strip()
            if loc:
                u, p = load_sitemap(loc, seen, depth + 1)
                urls += u
                problems += p
    else:
        for u in root.findall("sm:url", ns):
            loc = (u.findtext("sm:loc", default="", namespaces=ns) or "").strip()
            lastmod = (u.findtext("sm:lastmod", default="", namespaces=ns) or "").strip()
            if loc:
                urls.append((loc, lastmod, url))
    return urls, problems


def path_of(url):
    p = urllib.parse.urlsplit(url)
    return (p.path or "/") + (("?" + p.query) if p.query else "")


def check_url(url, rp):
    r = fetch(url)
    row = {
        "url": url, "path": path_of(url), "status": r["status"], "error": r["error"],
        "location": r["location"], "x_robots": r["headers"].get("x-robots-tag", ""),
        "meta_robots": "", "canonical": "", "title": "",
        "robots_allowed_googlebot": rp.can_fetch(GOOGLEBOT, url),
        "robots_allowed_any": rp.can_fetch("*", url),
    }
    if r["status"] == 200 and b"<" in r["body"][:2000]:
        h = Head()
        try:
            h.feed(r["body"][:200000].decode("utf-8", "replace"))
        except Exception:
            pass
        row["meta_robots"] = "; ".join(h.robots)
        row["canonical"] = h.canonical
        row["title"] = h.title[:120]
    row["noindex"] = ("noindex" in row["x_robots"].lower()) or ("noindex" in row["meta_robots"].lower())
    row["robots_blocked"] = not row["robots_allowed_googlebot"]
    return row


def classify_sitemap_row(row, base):
    flags = []
    if row["error"]:
        flags.append("FETCH_ERROR")
    elif row["status"] in (301, 302, 307, 308):
        flags.append("REDIRECT_IN_SITEMAP")
    elif row["status"] != 200:
        flags.append(f"NON200_IN_SITEMAP({row['status']})")
    if row["robots_blocked"]:
        flags.append("ROBOTS_BLOCKED_IN_SITEMAP")
    if row["noindex"]:
        flags.append("NOINDEX_IN_SITEMAP")
    if row["status"] == 200 and row["canonical"]:
        want = row["url"].rstrip("/") or base
        got = row["canonical"].rstrip("/")
        if got and got != want:
            flags.append("CANONICAL_ELSEWHERE")
    return flags


def odoo_read():
    import xmlrpc.client
    url = os.environ.get("ODOO_URL", BASE)
    db = os.environ.get("ODOO_DB", "voipintl19")
    login = os.environ.get("ODOO_LOGIN")
    key = os.environ.get("ODOO_KEY") or os.environ.get("ODOO_APIKEY")
    if not (login and key):
        return None, "ODOO_LOGIN / ODOO_KEY not set — skipping Odoo read"
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, login, key, {})
    if not uid:
        return None, "Odoo auth failed"
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    def kw(m, meth, args, kwargs=None):
        return models.execute_kw(db, uid, key, m, meth, args, kwargs or {})

    out = {}
    out["pages"] = kw("website.page", "search_read", [[["website_id", "in", [WEBSITE_ID, False]]]],
                      {"fields": ["url", "name", "is_published", "website_indexed", "website_id"],
                       "order": "url"})
    out["rewrites"] = kw("website.rewrite", "search_read", [[]],
                         {"fields": ["url_from", "url_to", "redirect_type", "website_id", "active"]})
    wf = kw("website", "fields_get", [], {"attributes": ["string"]})
    fname = next((f for f in ("robots_txt", "robots") if f in wf), None)
    out["robots_field"] = fname
    out["robots_custom"] = kw("website", "read", [[WEBSITE_ID], [fname]])[0][fname] if fname else ""
    out["website"] = kw("website", "read", [[WEBSITE_ID], ["name", "domain"]])[0]
    return out, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--out", help="write markdown report here (default stdout)")
    ap.add_argument("--csv", help="write per-URL CSV here")
    ap.add_argument("--max", type=int, default=2000, help="max sitemap URLs to fetch")
    ap.add_argument("--odoo", action="store_true", help="also read Odoo page/rewrite/robots state (read-only)")
    a = ap.parse_args()
    base = a.base.rstrip("/")

    lines = [f"# Crawl-block audit — {base}", ""]
    rob_resp, rob_text, rp = load_robots(base)
    lines += [f"## robots.txt (HTTP {rob_resp['status']}{' ' + rob_resp['error'] if rob_resp['error'] else ''})", "",
              "```", rob_text.strip() or "(empty)", "```", ""]

    sm_urls, sm_problems = load_sitemap(base + "/sitemap.xml")
    lines += [f"## sitemap.xml — {len(sm_urls)} URLs"] + [f"- {p}" for p in sm_problems] + [""]

    rows = []
    for loc, lastmod, src in sm_urls[: a.max]:
        row = check_url(loc, rp)
        row["lastmod"] = lastmod
        row["source"] = "sitemap"
        row["flags"] = classify_sitemap_row(row, base)
        rows.append(row)
    sm_paths = {r["path"] for r in rows}

    # Decision-list checks
    for p in MUST_RANK + MAY_RANK:
        if p in sm_paths:
            continue
        row = check_url(base + p, rp)
        row["lastmod"] = ""
        row["source"] = "decision:must-rank" if p in MUST_RANK else "decision:may-rank"
        flags = []
        if p in MUST_RANK:
            flags.append("MISSING_FROM_SITEMAP")
        if row["robots_blocked"]:
            flags.append("ROBOTS_BLOCKED")
        if row["noindex"]:
            flags.append("NOINDEX")
        if row["status"] != 200:
            flags.append(f"NON200({row['status']})")
        row["flags"] = flags
        rows.append(row)
    for r in rows:
        if r["source"] == "sitemap" and r["path"] in MUST_RANK:
            if r["robots_blocked"]:
                r["flags"].append("MUST_RANK_BUT_ROBOTS_BLOCKED")
            if r["noindex"]:
                r["flags"].append("MUST_RANK_BUT_NOINDEX")

    for p in MUST_NOT_RANK:
        row = check_url(base + p, rp)
        row["lastmod"] = ""
        row["source"] = "decision:must-not-rank"
        flags = []
        if p in sm_paths:
            flags.append("MUST_NOT_RANK_BUT_IN_SITEMAP")
        if row["status"] in (301, 302, 307, 308):
            flags.append("REDIRECTS_OK")
        elif row["status"] == 200 and not row["noindex"]:
            flags.append("NO_NOINDEX")
            if row["robots_blocked"]:
                flags.append("ROBOTS_BLOCK_HIDES_NOINDEX")  # Google can never see a noindex here
        elif row["status"] == 200 and row["noindex"] and row["robots_blocked"]:
            flags.append("ROBOTS_BLOCK_HIDES_NOINDEX")
        row["flags"] = flags
        rows.append(row)

    # Legacy blog namespace probe
    for p in (LEGACY_BLOG_PREFIX + "/anything-at-all-000", LEGACY_BLOG_PREFIX + "/tag/voip"):
        row = check_url(base + p, rp)
        row["lastmod"] = ""
        row["source"] = "probe:legacy-blog"
        row["flags"] = ["LEGACY_301_OK"] if row["status"] in (301, 308) else [f"LEGACY_NOT_301({row['status']})"]
        rows.append(row)

    # Report
    def table(title, rs):
        if not rs:
            return [f"### {title}", "", "None.", ""]
        out = [f"### {title}", "", "| URL | HTTP | → Location | robots | noindex source | flags |", "|---|---|---|---|---|---|"]
        for r in rs:
            src = "; ".join(x for x in (r["meta_robots"], ("X-Robots-Tag: " + r["x_robots"]) if r["x_robots"] else "") if x)
            out.append(f"| {r['url']} | {r['status'] or r['error']} | {r['location']} | "
                       f"{'BLOCKED' if r['robots_blocked'] else 'allowed'} | {src} | {', '.join(r['flags'])} |")
        return out + [""]

    conflicts = [r for r in rows if r["source"] == "sitemap" and r["flags"]]
    lines += ["## Sitemap conflicts (what Search Console's 2026-07-18 alerts point at)", ""]
    lines += table("Sitemap URLs that redirect, are noindexed, robots-blocked or non-200", conflicts)
    lines += table("Must-rank pages with a problem", [r for r in rows if r["source"] != "sitemap" and r["path"] in MUST_RANK and r["flags"]]
                   + [r for r in rows if r["source"] == "sitemap" and any(f.startswith("MUST_RANK") for f in r["flags"])])
    lines += table("Must-not-rank pages (mechanism check)", [r for r in rows if r["source"] == "decision:must-not-rank"])
    lines += table("Legacy blog namespace", [r for r in rows if r["source"] == "probe:legacy-blog"])

    ok = [r for r in rows if r["source"] == "sitemap" and not r["flags"]]
    lines += [f"### Clean sitemap URLs: {len(ok)} of {len([r for r in rows if r['source'] == 'sitemap'])}", ""]

    if a.odoo:
        od, err = odoo_read()
        lines += ["## Odoo state (read-only)", ""]
        if err:
            lines += [err, ""]
        else:
            lines += [f"Website {WEBSITE_ID}: {od['website']}", "",
                      f"Custom robots field `{od['robots_field']}`:", "```", (od["robots_custom"] or "").strip() or "(empty)", "```", ""]
            bad = [p for p in od["pages"] if p["is_published"] and not p["website_indexed"]
                   and p["url"] in MUST_RANK + MAY_RANK]
            lines += ["Published pages with website_indexed = False that are on the rank list:"]
            lines += [f"- {p['url']} (id {p['id']})" for p in bad] or ["- none"]
            lines += [""]
            redirected_pages = {rw["url_from"] for rw in od["rewrites"] if rw["active"]}
            still = [p for p in od["pages"] if p["url"] in redirected_pages and p["is_published"] and p["website_indexed"]]
            lines += ["Published + indexed website.page records that ALSO have a 301 rewrite (these land in the sitemap as 'Page with redirect'):"]
            lines += [f"- {p['url']} (page id {p['id']})" for p in still] or ["- none"]
            lines += ["", f"Rewrites: {len(od['rewrites'])}"]
            lines += [f"- {rw['redirect_type']} {rw['url_from']} → {rw['url_to']}{'' if rw['active'] else ' (inactive)'}" for rw in od["rewrites"]]
            lines += [""]

    report = "\n".join(lines)
    if a.out:
        with open(a.out, "w") as f:
            f.write(report)
        print(f"wrote {a.out}")
    else:
        print(report)
    if a.csv:
        cols = ["source", "url", "status", "location", "robots_blocked", "noindex", "meta_robots", "x_robots",
                "canonical", "title", "lastmod", "flags", "error"]
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                r2 = dict(r)
                r2["flags"] = ", ".join(r["flags"])
                w.writerow(r2)
        print(f"wrote {a.csv}")
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
