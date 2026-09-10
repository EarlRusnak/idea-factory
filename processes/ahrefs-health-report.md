---
type: process
area: seo
cadence: weekly
runs_at: Mondays 09:00 America/New_York (13:00 UTC)
routine_id: trig_01F7vMNr5Wz5doUVy3exq9by
standing_page: https://claude.ai/code/artifact/26cb3b0b-ddf5-47fa-be28-15134bbe8a92
feeds: seo-site-review
owner: Earl Rusnak
status: active
created: 2026-09-10
---
# Ahrefs Health Report

Weekly report built from the Ahrefs Site Audit crawl emails in Gmail: Health Score, error / warning / notice
counts, top issues per site, movement versus the previous crawl, and a ranked list of fixes with the expected
effect on the score. The Wednesday SEO review reads this page first.

## Inputs
- Gmail search for the past 10 days: `"Health Score"` and `subject:"New crawl" OR from:ahrefs.com`.
  Emails are forwarded to info@drrusnakwellness.com with subjects like
  `[voip-int] (Acumedgroup) Image file size too large: 188 URLs`.
- Last week's version of the standing page, for week-over-week comparison.
- Projects seen so far: Acumedgroup, Healing-skin, Drrusnakwellness, Voip-int. New projects are picked up automatically.

## Parsing
A script reads each email's HTML: project name, crawl date, URLs analyzed, Health Score, Errors, Warnings,
Notices and their deltas, and every row of the Top Issues table (issue, level, URL count). Newest crawl per
project wins; the previous crawl is kept for comparison.

## Ranking rules
Errors first (they drive Health Score), then by URL count, then warnings that affect indexing or click-through
(noindex, redirects in sitemap, titles and meta descriptions, H1), then alt text and notices. A drop of 3 or more
points is flagged as a regression. Where the email only shows the headline issue, the report says so and links
to the crawl in Ahrefs instead of guessing.

## Outputs
- Standing page updated in place.
- Google Doc "Ahrefs Health Report — YYYY-MM-DD" in Drive › Automated Reports (Claude Routines).
- Email to info@drrusnakwellness.com: score table, regressions first, action list, links.

## Seed run (crawls of Aug 29–30, 2026)
voip-int.com 96 · drrusnakwellness.com 94 · healing-skin.com 93 · acumedgroup.com 77
(193 errors: 188 oversized images, 5 sitemap redirects).

## Upgrade path
Add an Ahrefs API key to the Routine's environment to pull full issue lists instead of the emailed headline.
