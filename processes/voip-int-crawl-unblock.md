---
type: runbook
area: seo
site: voip-int.com
owner: Earl Rusnak (Odoo side) · Robert Riley (nginx side)
status: open — verification blocked from the cloud environment; scripts ready to run
created: 2026-09-10
standing_page: https://claude.ai/code/artifact/fcaa979a-43d4-400e-9e8f-d2ca53ed4cd2
---
# voip-int.com — unblock the crawl

Goal: one consistent answer per URL. Every page that should rank is crawlable, indexable, and in the
sitemap. Every page that should not rank answers **noindex** (so Google drops it) and is out of the
sitemap. robots.txt blocks only what has no HTML of its own to carry a noindex.

## 1. What was verified on 2026-09-10 (and what could not be)

Live checks of robots.txt and sitemap.xml are **blocked from the Claude cloud environment** (network
policy denies voip-int.com, and the Wayback Machine and Search Console via Adspirer are not reachable
either). Everything below comes from the evidence trail in Gmail and Drive. Run
`tools/voip_crawl_audit.py` from any machine that can reach the site to turn this into a live table.

| Date | Source | Fact |
| --- | --- | --- |
| Jul 1 | Drive › SEO_AUDIT_REPORT.md, crawl_findings.md | robots.txt allowed everything; sitemap.xml was empty; ~25 of 29 pages carried `meta robots noindex` because `website_indexed` was off on the website.page records. |
| Jul 2 | Drive › seo_fix_log.md | `run_seo_fixes.py --apply`: 8 legacy 301s created (incl. /contactus → /contact), `Disallow: /web/login` and `/my` appended to robots.txt, **61 pages switched to indexed** (only /get-started/thank-you left off), pricing view patched, blog meta descriptions set. Sitemap submitted to Search Console the same day. |
| Jul 6–7 | Drive › Mission Control | Production cutover complete. "robots.txt bug root-caused and fixed by Robert — was an Odoo field issue, not nginx." 15 high-value legacy-blog 301s applied. **This is the fix you remember.** |
| Jul 10 | Drive › VoIP_International_SEO_Audit_and_Recovery_Plan | robots.txt now blocks `/web/login`, `/my`, `/shop`, blog tag/date archives, legacy product images. Sitemap: 157 URLs, "Success". 294 indexed vs 1.19K not indexed (666 noindex, 468 crawled-not-indexed, 40 alternate-canonical). |
| Jul 10 | Gmail (bounced) + Drive › FOR_ROBERT_seo_deploy_2026-07-10_v2.md | Deploy package for Robert. Email bounced ("attachment type not allowed"); v2 posted to Drive. Robert investigated item 0 (no cache layer). Still unchecked in v2: `voip_seo` module (blog catch-all 301, llms.txt, IndexNow key), IndexNow ping, **X-Robots-Tag noindex on /web/login**. |
| Jul 16 | Gmail, sc-noreply | "Some fixes failed" for Review snippets structured data. |
| Jul 18 | Gmail, sc-noreply (two alerts) | (a) New reasons: **Blocked by robots.txt** and **Indexed, though blocked by robots.txt**. (b) Pages **in a sitemap**: **Excluded by 'noindex' tag** and **Page with redirect**. |
| Aug 3 | Gmail, Bing Webmaster | Bing ownership verification for voip-int.com **lost**. |
| Aug 29 | Gmail, Ahrefs crawl | 171 URLs, Health Score 96, 11 errors, 32 warnings; headline issue 9 missing meta descriptions. |
| Jul 18 → Sep 10 | Gmail, Drive, Mission Control, memory exports | **No record of anyone acting on the Jul 18 alerts.** No validation requested, no later Search Console mail, no Drive file, no Mission Control update touching robots/noindex after Jul 10. |

**Verdict.** The crawl *was* fixed on Jul 2–7: the site-wide noindex came off, the sitemap filled, and
Google indexed 294 pages. The Jul 18 alerts are a **second, different problem the fix created**: the
expanded robots.txt now hides pages that Google already had, and the sitemap advertises at least one
redirecting URL and some noindexed ones. That conflict has stood untouched since Jul 18.

## 2. Why the July fix produced the July 18 alerts

A robots.txt `Disallow` stops Googlebot from fetching the page, so Google **never sees the noindex** on
it. A URL Google already had (from the old site or from the Jul 2–10 window) stays in the index as
"Indexed, though blocked by robots.txt" for months. The Jul 6–10 robots expansion did exactly this to
`/web/login` (which Google had ranked in the site's top pages), `/shop`, and the blog tag/date
archives (which Odoo already serves with its own noindex; the 666 "Excluded by noindex" count on Jul 10
proves Google was reading it).

The sitemap alert has two halves:

- **Page with redirect** — `/contactus` still exists as a published, indexed website.page record, so
  Odoo lists it in the sitemap, while the Jul 2 rewrite 301s it to `/contact`. Same risk for any other
  page record that later gained a rewrite. The audit script's `--odoo` mode names every such record.
- **Excluded by noindex** — sitemap URLs that answer noindex. Candidates: shop product URLs if the
  eCommerce sitemap is still emitted while the shop is hidden, blog filter URLs, and any page record
  re-flagged during Robert's Jul 6 field fix. Google's own list is in Search Console › Pages ›
  "Excluded by 'noindex' tag" filtered to *All submitted pages*; the audit script produces the same
  list from outside.

## 3. Decision: what should rank

Rank list (in the sitemap, indexable, no robots block). This is the Jul 2 indexing list plus the
controller pages that never had the flag.

- **Money pages:** `/`, `/pricing`, `/phone-service`, `/pro-mobile`, `/ai-receptionist`, `/vfax`,
  `/sip-trunking`, `/mitel-replacement`, `/features`, `/integrations` and its 10 platform pages,
  `/replace-cell-phone-allowance`, `/hardware`, `/get-started`.
- **Verticals:** `/property-management`, `/field-service`, `/sales-teams`, `/multi-location`,
  `/healthcare-practice-phone-system`, `/dental-practice-phone-system`, `/wellness-clinic-phone-system`,
  `/legal-firm-phone-system`, `/real-estate-phone-system`.
- **Comparison and local:** `/vs` + `/vs/8x8`, `/vs/nextiva`, `/vs/ooma`, `/vs/ringcentral`;
  `/locations` + the 19 city pages.
- **Trust and content:** `/about`, `/contact`, `/faq`, `/blog` and every VoIP International post
  (blog 4), `/call-retrieve` and `/message-waiting-indicator-mwi` (already #1 for "call retrieved
  meaning"; the glossary hub grows from here).
- **Indexable, not chased:** `/privacy`, `/aup`, `/cookie-policy`, `/terms-of-service`.

Must not rank (noindex, out of the sitemap, **crawlable** until Google has dropped them):

| URL / pattern | Mechanism | Who |
| --- | --- | --- |
| `/web/login` | `X-Robots-Tag: noindex, nofollow` at nginx (Jul 10 package, item 4). Remove `Disallow: /web/login` until it has left the index. | Robert |
| `/shop` and `/shop/*` | Decision: **hidden until rebuilt on the site-5 theme** (it still renders the legacy website-1 header, contract pricelists and http og:urls). `X-Robots-Tag: noindex` at nginx on `^/shop`; remove `Disallow: /shop`; unpublish products so the eCommerce sitemap stops emitting them. If Earl wants the shop selling instead, the rebuild goes first and this row flips to "rank". | Robert (nginx) · Earl (products) |
| Blog tag/date archives | Odoo's own noindex. Drop the robots block that hides it. | Earl (script) |
| `/contactus` | Already 301s. Set `website_indexed = False` on the page record so it leaves the sitemap. | Earl (script) |
| `/get-started/thank-you` | Stays `website_indexed = False`. | — |
| `/blog/voip-international-blog-posts-2/*` | Catch-all 301 → `/blog` from the `voip_seo` module (exact rewrites keep winning). | Robert |
| Central Florida Telecom posts (blog 3) | Should not rank on voip-int.com; move to their own website record or unpublish. Decision open. | Earl |
| `/my/*`, `/web/signup`, `/web/reset_password`, `/web/session/*`, `/web/image/product*`, `?order=`, `?pricelist=` | robots.txt `Disallow` (no HTML worth a noindex; never indexed as content). | Earl (script) |

## 4. Steps

Run from a machine that can reach voip-int.com (the Mac or Windows PC with the `ODOO_*` exports, see
MACBOOK-CONTINUATION.md). Every script is dry-run by default.

1. **Audit first.** `python3 tools/voip_crawl_audit.py --odoo --out audit-before.md --csv urls-before.csv`
   Attach the output to this runbook. It lists every sitemap URL that redirects, is noindexed, is
   robots-blocked or is non-200, plus the Odoo page records behind them.
2. **Odoo side.** `python3 tools/voip_crawl_fix.py` (dry run) then `--apply`. It flips
   `website_indexed` on the rank list, turns it off for `/contactus` and the thank-you page, and
   replaces the custom robots block with the one in the script (no `/web/login`, `/shop` or tag/date
   disallows; explicit allows for GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended).
   Backups land in `tools/crawl_fix_backups/`.
3. **nginx side (Robert).** Add the two headers and install the `voip_seo` module from the Jul 10 package
   (Drive › voip_seo_deploy_for_robert.zip):

   ```nginx
   location = /web/login { add_header X-Robots-Tag "noindex, nofollow" always; # existing proxy_pass unchanged
   }
   location ^~ /shop { add_header X-Robots-Tag "noindex" always; # existing proxy_pass unchanged
   }
   ```
   Note: `add_header` inside a `location` replaces inherited headers; re-declare any site-wide headers there.
4. **Re-audit.** Same command as step 1 with `after` filenames. Acceptance: zero rows in "Sitemap
   conflicts", every must-rank page `200 / allowed / no noindex`, every must-not-rank page either
   `301` or `200 + noindex + allowed`, legacy blog probe `301`.
5. **Search Console.** Pages report: open "Blocked by robots.txt", "Indexed, though blocked by
   robots.txt", "Excluded by 'noindex' tag" and "Page with redirect", confirm the remaining URLs are
   all on the must-not-rank list, then press **Validate fix** on each. Resubmit `/sitemap.xml`.
   Request indexing for the 12 money pages (daily quota ~10, so two days).
6. **Bing.** Re-verify voip-int.com in Bing Webmaster Tools (verification lost Aug 3), resubmit the
   sitemap, then send the IndexNow ping from the Jul 10 package once the key file resolves.
7. **Ahrefs.** Trigger a fresh crawl of project "Voip-int"; Monday's Health Report picks up the delta.
8. **Close.** Update the site-inventory row and the Mission Control tracker row. Only then start the
   content work (glossary hub, title rewrites) from the Jul 10 recovery plan.

## 5. Inputs the process depends on

- Gmail: sc-noreply@google.com alerts for voip-int.com; Ahrefs `[voip-int] (Voip-int)` crawl emails.
- Drive: `seo-audit-2026-07-10/`, `seo_fix_log.md`, `FOR_ROBERT_seo_deploy_2026-07-10_v2.md`, `voip_seo/`.
- Odoo: website 5, DB `voipintl19`, XML-RPC with a per-user API key (never in the repo).
- To let the Wednesday SEO Review verify this itself, allow voip-int.com in the environment's network
  policy and connect Google Search Console inside Adspirer.
