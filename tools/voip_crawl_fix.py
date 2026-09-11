#!/usr/bin/env python3
"""voip_crawl_fix.py — apply the crawl-unblock decisions to voip-int.com (Odoo 19) via XML-RPC.

DRY-RUN by default. Nothing is written without --apply. Every write is backed up first to
./crawl_fix_backups/ and logged to ./crawl_fix_log.md.

Steps (select with --steps a,b; default runs only "robots"; "indexing" is opt-in):
  indexing  : website.page on website 5 — set website_indexed=True for every published page
              except the NEVER_INDEX list, and website_indexed=False for NEVER_INDEX (this is
              what removes a redirecting or private page from Odoo's sitemap).
  robots    : replace the website's custom robots block with ROBOTS_CUSTOM below. The rule is
              "block only what has no HTML noindex of its own"; everything Google should DROP
              from its index must stay crawlable and answer noindex (see the runbook).
  verify    : re-read and print the resulting state (always runs last).

Environment: ODOO_URL (default https://voip-int.com), ODOO_DB (voipintl19), ODOO_LOGIN, ODOO_KEY.
Same conventions as the July scripts (run_seo_fixes.py, db_fixes_2026-07-10.py).
"""
import datetime
import json
import os
import pathlib
import sys
import xmlrpc.client

URL = os.environ.get("ODOO_URL", "https://voip-int.com")
DB = os.environ.get("ODOO_DB", "voipintl19")
LOGIN = os.environ.get("ODOO_LOGIN", "earl.rusnak@voip-int.com")
KEY = os.environ.get("ODOO_KEY") or os.environ.get("ODOO_APIKEY")
WEBSITE_ID = 5

HERE = pathlib.Path(__file__).resolve().parent
BACKUP_DIR = HERE / "crawl_fix_backups"
LOG = HERE / "crawl_fix_log.md"

# Pages that exist as website.page records but must NOT be in the sitemap or the index.
NEVER_INDEX = {
    "/get-started/thank-you",   # conversion page
    "/contactus",               # 301 → /contact since 2026-07-02; if a page record still exists it
                                # must stay out of the sitemap ("Page with redirect")
    # Partner-program pages, deliberately unlisted (seen non-indexed on the 2026-09-11 dry run)
    "/partners/refer",
    "/partners/refer-thanks",
    "/partners/thank-you",
    "/partners/welcome",
}

# Custom robots block for website 5. Odoo renders its own "User-agent: *" group (Allow: /social_instagram/,
# Sitemap), then a "custom" banner, then "User-agent: *" + "Allow: /cards/", then THIS field verbatim.
# So this text must start with rules, not a User-agent line (the 2026-09-11 dry run confirmed the field
# starts at "Disallow: /web/login").
# Same blocks as the live 2026-09-11 file minus /web/login and /shop: both already carry (or will
# carry) an X-Robots-Tag noindex, and a robots block would stop Google from ever reading it.
# Re-add those two Disallows once Search Console shows the URLs gone.
# NOTE: Robert's voip_seo module keeps a sitemap-exclusion prefix list that mirrors these Disallow lines
# (added 2026-09-11). Any change here must be mirrored there; tell Robert when this block changes.
ROBOTS_CUSTOM = """\
# --- custom rules managed by tools/voip_crawl_fix.py (2026-09-11); Odoo emits the User-agent line above ---
Disallow: /my
Disallow: /web/signup
Disallow: /web/reset_password
Disallow: /web/session/
# Blog tag/date archive combinatorial URLs (thin/duplicate filter pages)
Disallow: /blog/*tag*
Disallow: /*date_begin=*
Disallow: /*date_end=*
# Legacy product image URLs from deleted/unpublished catalog
Disallow: /web/image/product
# Odoo system/demo routes - no marketing value, thin or empty (added 2026-08-16)
Disallow: /website/info
Disallow: /slides
Disallow: /profile
Disallow: /appointment
Disallow: /calendar
Disallow: /partners/thank-you
Disallow: /blog/our-blog-5
# /web/login and /shop intentionally NOT blocked: they answer X-Robots-Tag noindex (nginx)

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
"""

APPLY = "--apply" in sys.argv
sel = [a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1]
       for a in sys.argv if a.startswith("--steps")]
STEPS = sel[0].split(",") if sel else ["robots"]


def log(msg):
    print(msg)
    with open(LOG, "a") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()}Z {msg}\n")


if not KEY:
    sys.exit("Set ODOO_KEY (or ODOO_APIKEY) first.")
BACKUP_DIR.mkdir(exist_ok=True)
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, LOGIN, KEY, {})
if not uid:
    sys.exit("AUTH FAILED — check API key / login.")
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")


def kw(m, meth, args, kwargs=None):
    return models.execute_kw(DB, uid, KEY, m, meth, args, kwargs or {})


ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
log(f"## run {'APPLY' if APPLY else 'DRY-RUN'} steps={STEPS} uid={uid} url={URL}")

# ---------------------------------------------------------------------------
if "indexing" in STEPS:
    pages = kw("website.page", "search_read", [[["website_id", "=", WEBSITE_ID]]],
               {"fields": ["url", "name", "is_published", "website_indexed"], "order": "url"})
    (BACKUP_DIR / f"pages_before_{ts}.json").write_text(json.dumps(pages, indent=1))
    to_on = [p for p in pages if p["is_published"] and not p["website_indexed"] and p["url"] not in NEVER_INDEX]
    to_off = [p for p in pages if p["website_indexed"] and p["url"] in NEVER_INDEX]
    for p in to_on:
        log(f"[indexing] {'SET' if APPLY else 'would set'} indexed=True  {p['url']} (id {p['id']})")
    for p in to_off:
        log(f"[indexing] {'SET' if APPLY else 'would set'} indexed=False {p['url']} (id {p['id']})")
    log(f"[indexing] {len(pages)} pages on website {WEBSITE_ID}; {len(to_on)} to switch on, {len(to_off)} to switch off")
    if APPLY:
        if to_on:
            kw("website.page", "write", [[p["id"] for p in to_on], {"website_indexed": True}])
        if to_off:
            kw("website.page", "write", [[p["id"] for p in to_off], {"website_indexed": False}])
        rem = kw("website.page", "search_read",
                 [[["website_id", "=", WEBSITE_ID], ["is_published", "=", True], ["website_indexed", "=", False]]],
                 {"fields": ["url"]})
        log(f"[indexing] applied; published+non-indexed now: {sorted(p['url'] for p in rem)} (expect only NEVER_INDEX)")

# ---------------------------------------------------------------------------
if "robots" in STEPS:
    wfields = kw("website", "fields_get", [], {"attributes": ["string"]})
    fname = next((f for f in ("robots_txt", "robots") if f in wfields), None)
    if not fname:
        log("[robots] no custom robots field on website model — set it in Website › Settings › SEO. SKIPPED")
    else:
        cur = kw("website", "read", [[WEBSITE_ID], [fname]])[0][fname] or ""
        (BACKUP_DIR / f"robots_before_{ts}.txt").write_text(cur)
        if cur.strip() == ROBOTS_CUSTOM.strip():
            log("[robots] custom block already matches — nothing to do")
        else:
            log("[robots] current custom block:\n" + (cur.strip() or "(empty)"))
            log("[robots] " + ("REPLACING with" if APPLY else "would replace with") + ":\n" + ROBOTS_CUSTOM.strip())
            if APPLY:
                kw("website", "write", [[WEBSITE_ID], {fname: ROBOTS_CUSTOM}])
                log("[robots] written; verify with: curl -s https://voip-int.com/robots.txt")

# ---------------------------------------------------------------------------
# verify (always)
pages = kw("website.page", "search_read",
           [[["website_id", "=", WEBSITE_ID], ["is_published", "=", True]]],
           {"fields": ["url", "website_indexed"], "order": "url"})
off = [p["url"] for p in pages if not p["website_indexed"]]
log(f"[verify] published pages: {len(pages)}; not indexed: {off}")
rewrites = kw("website.rewrite", "search_read", [[["active", "=", True]]],
              {"fields": ["url_from", "url_to", "redirect_type"]})
clash = [p["url"] for p in pages if p["website_indexed"] and p["url"] in {r["url_from"] for r in rewrites}]
log(f"[verify] indexed pages that also 301 (sitemap 'Page with redirect' candidates): {clash or 'none'}")
log("## run complete\n")
print(f"\nLog: {LOG}\nBackups: {BACKUP_DIR}")
