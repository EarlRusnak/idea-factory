#!/usr/bin/env python3
"""voip_legacy_redirects.py — 301 the Odoo 15 legacy pages that Search Console still crawls (404 list,
export of 2026-09-11) to their nearest page on the Odoo 19 site, as website.rewrite records.

DRY-RUN by default; --apply to write. Existing rewrites for a source URL are never touched.
Environment: ODOO_URL, ODOO_DB, ODOO_LOGIN, ODOO_KEY (same as the other tools/ scripts).

Not in this map on purpose — these two must be RECREATED, not redirected, because they still rank
(call-retrieve: 15 clicks / 3,701 impressions / position 4.95 in the last 90 days while 404):
    /call-retrieve
    /message-waiting-indicator-mwi
Their content lives in the Odoo 15 database; export it before that server is decommissioned.
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
APPLY = "--apply" in sys.argv

HERE = pathlib.Path(__file__).resolve().parent
LOG = HERE / "legacy_redirects_log.md"

# Source (Odoo 15 URL still in Google's index, 404 today) -> target on the Odoo 19 site.
REDIRECTS = {
    # PBX feature pages -> the features page (until a glossary hub exists; then re-point them)
    "/call-waiting": "/features",
    "/voicemail": "/features",
    "/delayed-simultaneous-ring": "/features",
    "/simultaneous-ring-ring-all": "/features",
    "/call-screen-pops": "/features",
    "/auto-attendant": "/features",
    "/auto-attendant-speech-recognition": "/features",
    "/call-park": "/features",
    "/call-history": "/features",
    "/call-transfer": "/features",
    "/text-to-speech": "/features",
    "/conferencing-dedicated-or-owned-bridge": "/features",
    "/operator-forward": "/features",
    "/music-on-hold": "/features",
    "/call-pickup": "/features",
    "/call-queue-routing": "/features",
    "/dnd-do-not-disturb": "/features",
    "/call-time-frames": "/features",
    "/paging": "/features",
    "/full-feature-list": "/features",
    "/enterprise-text-messaging": "/features",
    "/worldwide-phone-number-availability": "/features",
    "/integrated-wallboard-for-real-time-monitoring": "/features",
    "/pro-contact-center-solution": "/features",
    "/pro-call-center-pbx-extension": "/features",
    "/device-agnostic": "/phone-service",
    # Products
    "/pro-sip-trunking": "/sip-trunking",
    "/pro-mobile-voip": "/pro-mobile",
    "/pro-integrated-mobile-voip": "/pro-mobile",
    "/mobile-application-pro-mobile-app": "/pro-mobile",
    "/voip-international-mobile-app": "/pro-mobile",
    "/app-free-solution": "/pro-mobile",
    "/enhanced-mobility-and-accessibility": "/pro-mobile",
    "/flexibility-and-mobility": "/pro-mobile",
    "/pro-audio-intelligence": "/voip-insights",
    "/voicemail-transcription": "/voip-insights",
    "/recorded-call-transcription-1": "/voip-insights",
    # Integrations
    "/crm-integrations": "/integrations",
    "/crm-integration": "/integrations",
    "/integration-with-business-applications": "/integrations",
    "/integration-with-business-applications-1": "/integrations",
    "/seamless-business-integration": "/integrations",
    "/teams-integrator": "/integrations/microsoft-teams",
    # Benefit pages -> phone service
    "/increased-security-and-compliance": "/phone-service",
    "/exceptional-customer-service": "/phone-service",
    "/enhanced-customer-service": "/phone-service",
    "/simplified-it-management": "/phone-service",
    "/flexible-and-scalable": "/phone-service",
    "/unified-communication-experience": "/phone-service",
    "/efficient-user-onboarding": "/phone-service",
    "/improved-productivity-and-collaboration": "/phone-service",
    "/enhanced-work-life-balance-for-employees": "/phone-service",
    "/cost-savings-and-simplified-billing": "/pricing",
    "/cost-effective-communication": "/pricing",
    # Support / misc
    "/knowledge": "/faq",
    "/forum": "/faq",
    "/helpdesk/helpdesk_support_ticket": "/contact",
    "/free-trial": "/get-started",
    "/about-voip-international": "/about",
    # Blog slugs that changed
    "/blog/voip-international-blog/the-real-cost-of-missed-calls":
        "/blog/voip-international-blog-posts-4/the-real-cost-of-missed-calls-and-what-an-ai-receptionist-actually-fixes-268",
    "/blog/voip-international-blog/property-management-communication-problem": "/property-management",
    "/blog/our-blog-22": "/blog",
}

RECREATE = ["/call-retrieve", "/message-waiting-indicator-mwi"]


def log(msg):
    print(msg)
    with open(LOG, "a") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()}Z {msg}\n")


if not KEY:
    sys.exit("Set ODOO_KEY (or ODOO_APIKEY) first.")
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, LOGIN, KEY, {})
if not uid:
    sys.exit("AUTH FAILED — check API key / login.")
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")


def kw(m, meth, args, kwargs=None):
    return models.execute_kw(DB, uid, KEY, m, meth, args, kwargs or {})


log(f"## run {'APPLY' if APPLY else 'DRY-RUN'} uid={uid} url={URL} ({len(REDIRECTS)} redirects)")
existing = {r["url_from"]: r for r in kw("website.rewrite", "search_read", [[]],
                                        {"fields": ["url_from", "url_to", "redirect_type", "website_id", "active"]})}
# Targets must exist as published pages or controller routes; check the website.page ones we know.
pages = {p["url"] for p in kw("website.page", "search_read",
                              [[["website_id", "in", [WEBSITE_ID, False]], ["is_published", "=", True]]],
                              {"fields": ["url"]})}
created = skipped = 0
for src, dst in REDIRECTS.items():
    if src in existing:
        e = existing[src]
        log(f"[skip] EXISTS {src} -> {e['url_to']} ({e['redirect_type']}{'' if e['active'] else ', inactive'})")
        skipped += 1
        continue
    note = "" if (dst in pages or dst.startswith("/blog") or dst in ("/integrations/microsoft-teams",)) \
        else "  (target not a website.page — controller route or check it)"
    if APPLY:
        rid = kw("website.rewrite", "create", [{
            "name": f"Legacy 301 {src}", "url_from": src, "url_to": dst,
            "redirect_type": "301", "website_id": WEBSITE_ID}])
        log(f"[create] 301 {src} -> {dst} (id {rid}){note}")
    else:
        log(f"[would create] 301 {src} -> {dst}{note}")
    created += 1
log(f"[summary] {'created' if APPLY else 'would create'} {created}, skipped {skipped}")
log("[recreate] NOT redirected, rebuild these pages: " + ", ".join(RECREATE))
log("## run complete\n")
print(f"\nLog: {LOG}")
