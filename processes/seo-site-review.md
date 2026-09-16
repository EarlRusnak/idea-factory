---
type: process
area: seo
cadence: weekly
runs_at: Wednesdays 09:00 America/New_York (13:00 UTC)
routine_id: trig_013AxiYoyAmWVTraE7W5ADAu
standing_page: https://claude.ai/code/artifact/2ef21298-a12c-4698-8c0a-fb61fb6315ab
depends_on: ahrefs-health-report
owner: Earl Rusnak
status: active
created: 2026-09-10
---
# Rusnak SEO Review

Weekly SEO review of every website (see [site-inventory](site-inventory.md)) with a single ranked action list.
It starts from Monday's Ahrefs Health Report, adds Google Search Console signals from Gmail, and, when the
live page checks. Search Console is not connected to any API tool (the free Adspirer
plan does not include it), so all Search Console figures come from Google's notification emails; where an action
needs page-level data the emails do not carry, the report names the exact Search Console report to open.

## Inputs
1. Monday's Ahrefs Health Report page (scores, movement, open actions carried forward with status).
2. Gmail, last 35 days from sc-noreply@google.com: monthly performance emails (clicks, impressions, top and
   growing pages and queries, devices, countries), indexing alerts, validation results, structured-data
   notices, milestone emails. Prior month's email is fetched for percentage change.
3. Live fetch of each homepage for title, meta description, H1, canonical, noindex. **Working as of 2026-09-16** —
   all six domains returned HTTP 200 from the cloud environment, so live checks are no longer recorded as
   unavailable. Crawling the full sitemap per site is also possible (see reports/ for the Academy example).

## Ranking rules
Revenue sites first (healing-skin.com, acumedgroup.com). Within that: indexing blockers and 4xx / redirect
problems, then Health Score errors carried from Ahrefs, then title / meta / H1 fixes on pages that already get
impressions, then content opportunities from growing queries (named query plus the page to strengthen).
Each item names the site, the evidence with a number or date, the concrete action, and who can do it.

## Outputs
- Standing page updated in place: portfolio scoreboard, per-site detail cards, suggested actions this week.
- Google Doc "Rusnak SEO Review — YYYY-MM-DD" in Drive › Automated Reports (Claude Routines).
- Email to info@drrusnakwellness.com: scoreboard, action list, links to this page, the Ahrefs page and the Doc.

## Seed run (data through Sep 8, 2026)
healing-skin.com 208 clicks in August, down 19% from July, with a Sep 6 indexing alert (redirect / noindex).
acumedgroup.com 166 clicks, up 2%, with 404s reported Sep 6 and Health Score 77.
drrusnakwellness.com 4xx indexing fix validating since Sep 7. voip-int.com robots.txt and sitemap noindex
conflicts open since July.
