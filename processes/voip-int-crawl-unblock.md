---
type: runbook
area: seo
site: voip-int.com
owner: Earl Rusnak (Odoo side) · Robert Riley (nginx / TLS side)
status: open — live audit done 2026-09-11; Search Console re-verified 2026-09-11; fixes staged, not applied
created: 2026-09-10
updated: 2026-09-11
standing_page: https://claude.ai/code/artifact/fcaa979a-43d4-400e-9e8f-d2ca53ed4cd2
---
# voip-int.com — unblock the crawl

Goal: one consistent answer per URL. Every page that should rank is crawlable, indexable, and in the
sitemap. Every page that should not rank answers **noindex** (so Google drops it) and is out of the
sitemap. robots.txt blocks only what has no HTML of its own to carry a noindex.

## 1. Live state on 2026-09-11

`tools/voip_crawl_audit.py` ran against the live site once voip-int.com was allowed in the environment
network policy. 164 sitemap URLs fetched, 154 clean.

**The July fixes did land.** The Jul 10 package items are live: `/web/login` answers
`X-Robots-Tag: noindex, nofollow`, the legacy blog namespace 301s to `/blog` (the `voip_seo` catch-all),
`/contactus` 301s to `/contact` and is no longer in the sitemap, and http → https redirects. robots.txt
was edited again on Aug 16 (Odoo system routes) and Sep 1 (Central Florida Telecom category unblocked
on purpose). The earlier draft of this runbook said nothing was done after Jul 18; that was wrong for
the site work. What was never done is the Search Console side: no validation was requested, and the
property has probably gone dark (see finding 4).

### Findings, most valuable first

1. **The two glossary pages that carried the site's best query are 404.** `/call-retrieve` and
   `/message-waiting-indicator-mwi` return 404 with no redirect and no replacement anywhere in the
   sitemap. In June `/call-retrieve` had 11 clicks and "call retrieved meaning" was position 1 with
   ~4,900 impressions a quarter. Nothing in Drive or Mail records their removal.
2. **www.voip-int.com fails TLS.** The certificate on 72.21.12.147 is `CN=voip-int.us` with no
   `www.voip-int.com` name, so every https://www request errors, and http://www returns 404 instead of a
   301. Anyone who types www gets a browser warning.
3. **voip-int.us still serves the full site with 200.** Its pages canonical to voip-int.com, which
   limits the damage, but it should 301 host-wide (July H1 item, still open).
4. **Search Console has probably lost ownership of https://voip-int.com/.** No monthly performance
   email arrived for July or August while healing-skin.com and acumedgroup.com got theirs on Sep 8; last
   year voip-int.com's came Sep 4. Bing reported on Aug 3 that it lost verification because the site was
   "not in the list of verified sites imported" from Search Console. No `google-site-verification` meta
   tag is in the homepage HTML. If verification was by HTML tag or file, an Odoo module update removed it.
5. **Ten sitemap URLs are blocked by robots.txt** (the "Blocked by robots.txt / in a sitemap" alert):
   `/shop`, `/appointment`, `/calendar` (301 → /appointment), `/slides`, `/slides/all` (303),
   `/profile/users`, `/profile/ranks_badges`, `/website/info`, `/blog/our-blog-5`, `/blog/our-blog-5/feed`.
   Odoo emits them because the eLearning, appointment, profile and a default empty blog are installed
   and published; the Aug 16 robots edit blocked them but left them in the sitemap.
6. **Two robots blocks hide a noindex.** `/web/login` now has the noindex header but is still
   `Disallow`ed, so Google cannot see it and keeps the URL as "Indexed, though blocked". `/shop` is
   blocked, in the sitemap, and has no noindex at all.
7. robots.txt has two `User-agent: *` groups (Odoo's own, then the custom block). Google merges them;
   Python's parser and some tools read only the first, which is why an earlier pass of the audit script
   reported nothing blocked. The script now merges groups the way Google does.

Not an issue any more: the Jul 18 "Page with redirect / noindex in sitemap" pair. `/contactus` is out of
the sitemap and no sitemap URL answers noindex today.

### Search Console Pages report (exported 2026-09-11, data through 2026-09-03)

Google kept collecting while the property was unverified, so the export shows the whole summer.

| Date | Indexed | Not indexed | Impressions / day (7-day feel) |
| --- | --- | --- | --- |
| Jun 29 (first day with counts) | 294 | 1,186 | ~950 |
| Jul 10 – Jul 23 | 333 | 1,528 | ~1,000 |
| Jul 24 | 296 | 1,624 | ~650 |
| Aug 7 – Aug 16 | 279 → 276 | 1,641 → 1,652 | ~700 |
| Sep 3 (latest) | 256 | 1,580 | ~750 |

Indexed pages fell by 77 (23%) between Jul 23 and Sep 3, in steps on Jul 24, Aug 5–10, Aug 17, Aug 21
and Aug 28. Daily impressions fell from ~1,000 in mid-July to ~600–800 from Jul 24 on.

| Not-indexed reason | Pages | Read against the live audit |
| --- | --- | --- |
| Blocked by robots.txt | 550 | Tag/date archive URLs, `/shop/*`, product images, system routes. Expected for the junk; the 10 sitemap URLs in finding 5 are inside this number. |
| Crawled, currently not indexed | 375 | Mostly legacy blog URLs and pagination Google chose not to keep. |
| Excluded by noindex | 363 | Down from 666 on Jul 10 as blocked archive URLs stopped being fetched. |
| Page with redirect | 161 | The legacy 301s working. Normal. |
| Not found (404) | 81 | Includes the two glossary pages. Needs the URL list. |
| Alternate page with proper canonical | 39 | Normal. |
| Discovered, not indexed | 8 | Normal. |
| Duplicate, Google chose different canonical | 3 | Normal. |
| **Indexed, though blocked by robots.txt** | **94** | These sit inside the 256 "indexed": URLs Google keeps but cannot read. `/web/login`, `/shop/*` and legacy archive URLs. They leave only when the block comes off and a noindex is visible (finding 6). |

So of 256 indexed URLs, 94 are ones we do not want, which leaves about 162 wanted pages indexed
against 164 in the sitemap. The indexing itself is close to right; the losses are the 94 stuck
junk URLs and the pages that dropped since Jul 24 (the 404 and "crawled, not indexed" lists say which).

### Evidence trail (from Gmail and Drive, kept for the record)

| Date | Source | Fact |
| --- | --- | --- |
| Jul 1 | Drive › SEO_AUDIT_REPORT.md | robots.txt allowed everything; sitemap empty; ~25 pages noindexed via `website_indexed` off. |
| Jul 2 | Drive › seo_fix_log.md | 8 legacy 301s, `Disallow: /web/login` and `/my`, 61 pages switched to indexed, sitemap submitted. |
| Jul 6–7 | Mission Control | Cutover complete; "robots.txt bug root-caused and fixed by Robert — an Odoo field issue"; 15 blog 301s. |
| Jul 10 | Drive › Recovery Plan, FOR_ROBERT v2 | robots.txt blocks login, /my, /shop, tag/date archives. 294 indexed. Deploy package for Robert (email bounced, v2 on Drive). |
| Jul 18 | Gmail · Search Console | Alerts: Blocked by robots.txt; Indexed though blocked; sitemap pages noindex / redirect. Never validated. |
| Aug 3 | Gmail · Bing Webmaster | Verification lost; Bing could not find the site among the sites imported from Search Console. |
| Aug 16, Sep 1 | Live robots.txt comments | System routes blocked; Central Florida Telecom category unblocked. |
| Sep 8 | Gmail · Search Console | August performance emails for healing-skin.com and acumedgroup.com. None for voip-int.com (none for July either). |
| Sep 11 | Live audit | Findings 1–7 above. Full table in `tools/audit-2026-09-11.md`. |
| Sep 11 | Search Console export (data to Sep 3) | Indexed 256 (94 of them robots-blocked), not indexed 1,580; indexed count down 77 since Jul 23. |

## 2. Why a robots block is the wrong tool for pages Google already has

A robots.txt `Disallow` stops Googlebot from fetching the page, so Google never sees the noindex on it. A
URL Google already had stays in the index as "Indexed, though blocked by robots.txt" for months. The
right sequence for anything Google has already indexed is: serve noindex, leave it crawlable until it
drops out, then (optionally) block it. Blocking is fine for URLs Google never indexed as content.

## 3. Decision: what should rank

Rank list (in the sitemap, indexable, no robots block):

- **Money pages:** `/`, `/pricing`, `/phone-service`, `/pro-mobile`, `/ai-receptionist`, `/vfax`,
  `/sip-trunking`, `/mitel-replacement`, `/features`, `/integrations` and its platform pages,
  `/replace-cell-phone-allowance`, `/hardware`, `/get-started`, `/voip-insights`, `/voip-reseller-program`.
- **Verticals:** property management, field service, sales teams, multi-location, healthcare, dental,
  wellness, legal, real estate.
- **Comparison and local:** `/vs` + 8x8, Nextiva, Ooma, RingCentral; `/locations` + the 19 city pages.
- **Trust and content:** `/about`, `/contact`, `/faq`, `/blog`, every VoIP International post (blog 4),
  and per the Sep 1 decision the Central Florida Telecom local posts (blog 3).
- **Glossary:** `/call-retrieve` and `/message-waiting-indicator-mwi` restored (or 301 to a new
  glossary URL), then the glossary hub from the Jul 10 plan.
- **Indexable, not chased:** `/privacy`, `/aup`, `/cookie-policy`, `/terms-of-service`.

Must not rank:

| URL / pattern | Today | Mechanism to reach | Who |
| --- | --- | --- | --- |
| `/web/login` | noindex header + robots block | Remove `Disallow: /web/login` so Google can read the header and drop the URL; re-add the block after it is gone. | Earl (script) |
| `/shop`, `/shop/*` | robots block, in sitemap, no noindex | `X-Robots-Tag: noindex` at nginx on `^/shop`, remove the Disallow, unpublish products. Stays hidden until rebuilt on the site-5 theme. | Robert (nginx) · Earl |
| `/appointment`, `/calendar`, `/slides*`, `/profile/*`, `/website/info`, `/blog/our-blog-5*` | robots block, in sitemap | Delete the empty "our-blog-5" blog; for the module routes either uninstall the unused module or add a sitemap exclusion in `voip_seo` (override `website._enumerate_pages` / the sitemap rule to drop these prefixes). Until then these are Search Console warnings, not ranking problems. | Earl · Robert |
| `/my/*`, `/web/signup`, `/web/reset_password`, `/web/session/*`, `/web/image/product*`, `?date_begin=`, `?date_end=`, `/blog/*tag*` | robots block | Keep. Never indexed as content. | — |
| `/get-started/thank-you` | meta noindex | Keep. | — |
| `/blog/voip-international-blog-posts-2/*` | 301 → /blog | Keep. | — |
| `voip-int.us` (whole host) | serves 200, canonical → .com | 301 every path to `https://voip-int.com`. | Robert |
| `www.voip-int.com` | TLS error | Add the name to the Let's Encrypt cert and 301 to the apex. | Robert |

## 4. Steps

Both scripts are dry-run by default and back up before writing. They need `ODOO_URL`, `ODOO_DB`,
`ODOO_LOGIN`, `ODOO_KEY` in the environment (see MACBOOK-CONTINUATION.md; never commit them).

1. **Search Console ownership.** Done 2026-09-11: the property was not verified; Earl re-verified it.
   Still to do in the same sitting: resubmit `/sitemap.xml` under the property, and in Bing Webmaster
   Tools re-import from Search Console (or add the site again) so Bing verification comes back. The
   Pages and Performance reports refill over the next few days; expect a fresh "Blocked by robots.txt"
   alert for the ten sitemap URLs in finding 5 until step 5 is done.
2. **Glossary pages (Earl).** Find the two page records in Odoo (Website › Pages, search "retrieve" and
   "mwi"): republish if unpublished, restore from the Jul backups if deleted, or create the glossary
   hub and 301 the old URLs to it. Request indexing once they answer 200.
3. **nginx and TLS (Robert) — before step 4, so `/shop` never goes crawlable without a noindex.**

   ```nginx
   location = /web/login { add_header X-Robots-Tag "noindex, nofollow" always; }   # already live
   location ^~ /shop     { add_header X-Robots-Tag "noindex" always; }             # new
   # add_header inside a location replaces inherited headers: re-declare site-wide ones there.
   ```
   Add `www.voip-int.com` to the certificate (`certbot --expand`), then 301 `www.voip-int.com` and
   `voip-int.us` (all paths) to `https://voip-int.com$request_uri`.
4. **Odoo side (Earl).** `python3 tools/voip_crawl_fix.py` (dry run), then `--apply`. It keeps every
   published page indexed except the thank-you page, and rewrites the custom robots block to the one in
   the script: same blocks as today minus `/web/login` and `/shop`, one merged group, explicit allows
   for GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and Google-Extended.
5. **Sitemap hygiene (Earl + Robert).** Delete the empty "our-blog-5" blog. Decide per module: eLearning
   (`/slides`, `/profile`) and appointments (`/appointment`, `/calendar`) are either in use, in which case
   `voip_seo` gets a sitemap exclusion for those prefixes, or unused and uninstalled.
6. **Re-audit.** `python3 tools/voip_crawl_audit.py --odoo --out audit-after.md --csv urls-after.csv`.
   Acceptance: zero rows under "Sitemap conflicts"; every rank-list page 200 / allowed / no noindex;
   `/web/login` and `/shop` allowed + noindex; legacy blog probe 301; `www` and `.us` 301 to the apex.
7. **Search Console.** Validate the four Jul 18 issues, resubmit the sitemap, request indexing for the
   money pages and the two glossary pages over two days.
8. **Close.** Update the site-inventory row and the Mission Control tracker row, then start the content
   work from the Jul 10 recovery plan.

## 5. Inputs

- Gmail: sc-noreply@google.com alerts for voip-int.com; Ahrefs `[voip-int] (Voip-int)` crawl emails.
- Drive: `seo-audit-2026-07-10/`, `seo_fix_log.md`, `FOR_ROBERT_seo_deploy_2026-07-10_v2.md`, `voip_seo/`.
- Odoo: website 5, DB `voipintl19`, XML-RPC with a per-user API key.
- The environment network policy now allows the six site domains, so the Wednesday SEO Review can run
  the audit script itself. Search Console will not be connected in Adspirer (the single slot stays on
  Google Ads), so Search Console evidence keeps coming from Gmail.

## 6. Request-indexing batches (Search Console › URL Inspection › Request indexing)

All 35 URLs answered 200 on 2026-09-11. Ten a day is the practical quota; do them in this order and
tick the day off in the tracker row. The two glossary URLs are excluded until they answer 200.

| Day | URLs |
| --- | --- |
| 1 | `/` · `/pricing` · `/phone-service` · `/pro-mobile` · `/ai-receptionist` · `/vfax` · `/sip-trunking` · `/mitel-replacement` · `/integrations` · `/features` |
| 2 | `/property-management` · `/field-service` · `/sales-teams` · `/multi-location` · `/healthcare-practice-phone-system` · `/dental-practice-phone-system` · `/wellness-clinic-phone-system` · `/legal-firm-phone-system` · `/real-estate-phone-system` · `/replace-cell-phone-allowance` |
| 3 | `/vs` · `/vs/ringcentral` · `/vs/nextiva` · `/vs/8x8` · `/vs/ooma` · `/locations` · `/orlando-business-phone` · `/hardware` · `/voip-insights` · `/voip-reseller-program` |
| 4 | `/about` · `/faq` · `/contact` · `/get-started` · `/blog` · then `/call-retrieve` and `/message-waiting-indicator-mwi` once restored |
