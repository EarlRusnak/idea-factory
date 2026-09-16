---
type: report
area: seo
site: drrusnakacademy.com
reviewed: 2026-09-16
method: live crawl of all 24 sitemap URLs + Search Console notification emails
owner: Earl Rusnak
status: complete
supersedes_session: Dr. Rusnak Academy site review (session_01JgP6ahF3xw4p9gcchhxsdj, never ran)
---
# Dr. Rusnak Academy — Site Review

Full review of drrusnakacademy.com on 2026-09-16. Every URL in the Yoast page sitemap was fetched
live (24 of 24 returned HTTP 200) and checked for title, meta description, canonical, robots
directive, heading structure, word count, image alt text and structured data. Search Console
figures come from the `sc-noreply@google.com` notification emails, since the site has no Search
Console API connection.

## Verdict

The site is in **good technical health**. There are no broken pages, no redirect chains in the
sitemap, no noindexed pages, no duplicate titles or descriptions, no missing image alt text, and
structured data on every page. The defects are concentrated in two fixable areas: **duplicate H1
tags from a CSS class used as a heading tag**, and **two thin archive URLs that should not be
indexable**. Both indexing complaints Google has sent are explained by the latter.

## Traffic

| Date | Clicks / 28 days | Source |
| --- | --- | --- |
| Jun 18, 2026 | first impressions collected | SC onboarding email |
| Jul 14, 2026 | 15 | SC milestone email |
| Aug 13, 2026 | 50 | SC milestone email |

Growth of 3.3x in one month. **No Search Console email has arrived since Aug 15**, so there is no
evidence either way for the Aug 13 – Sep 16 window; the Performance report has to be opened
directly to get the current number.

## Actions, ranked

### 1. Remove the duplicate H1 on seven pages
`<h1 class="h1">` is being used as a style hook inside the bottom call-to-action block. The hero H1
is correct on every page; the CTA block adds a second one. On the four program pages the second H1
is **identical text to the first**, which is the worst case for a money page.

| Page | H1 #1 (correct) | H1 #2 (should be H2) |
| --- | --- | --- |
| `/` | Where Tattooing Becomes Restoration. | Request Information. |
| `/programs/` | Four Tracks. One Certifying Academy. | Speak with the Academy about your candidacy. |
| `/about/` | Dr. Cecilia Rusnak | Train under the founder of the Academy. |
| `/programs/paramedical-tattoo-certification/` | Paramedical Tattoo Certification | Paramedical Tattoo Certification |
| `/programs/areola-masterclass/` | 3D Areola Masterclass | 3D Areola Masterclass |
| `/programs/mastering-paramedical-billing/` | Mastering Paramedical Billing | Mastering Paramedical Billing |
| `/programs/powder-botox/` | Powder Botox Masterclass | Powder Botox Masterclass |

Fix: in the CTA section template change `<h1 class="h1">` to `<h2 class="h1">`. The `h1` class keeps
the visual size, so nothing changes for the eye. One template edit covers all seven pages.

### 2. Stop `/category/uncategorized/` from being indexed
It returns HTTP 200 with `index, follow`, a self-referencing canonical, 84 words of content, zero
article links, and the H1 "Category: Uncategorized". This is a thin indexable page carrying a junk
name on a credentialing site.

Fix: Yoast › Settings › Categories › set **Show Categories in search results = Off** (it emits
`noindex`). The blog entries are WordPress *pages*, not posts, so no category archive is needed at
all.

### 3. Resolve `/blog/page/2/`
It returns HTTP 200 and is byte-for-byte the same listing as `/blog/` — same title, same H1, 540
words versus 541, and **zero article links**. It correctly canonicals to `/blog/`, which is why this
has not damaged rankings, but it is the direct cause of the **"Alternate page with proper canonical
tag"** notice Google sent on Jul 18. An empty page 2 exists because pagination is switched on while
all ten entries fit on page 1.

Fix: set the blog listing to show more posts per page than exist, or disable pagination on that
template, so `/blog/page/2/` 404s instead of duplicating page 1.

### 4. Shorten 15 meta descriptions
All 15 exceed the ~165-character display limit and will be cut mid-sentence in results. Worst first:

`/blog/paramedical-insurance-billing-primer` 202 · `/blog/areola-tattoo-consultation-guide` 195 ·
`/blog/state-by-state-regulatory-landscape` 195 · `/blog/scar-camouflage-technique-brief` 192 ·
`/programs/powder-botox` 191 · `/programs/mastering-paramedical-billing` 183 · `/master-trainer` 182 ·
`/about` 179 · `/enrollment` 179 · `/` 176 · `/blog/hipaa-paramedical-practice-guide` 174 ·
`/programs/` 172 · `/blog/paramedical-vs-cosmetic-tattooing` 171 · `/blog/why-an-academy-why-now` 171 ·
`/contact/` 170

Priority order for rewriting: the four program pages and the homepage first, then `/enrollment/`
and `/master-trainer/`, then the blog entries.

### 5. Shorten the homepage title
At 85 characters it is the longest on the site and will truncate. Current:

> Dr. Rusnak Academy — Professional Training and Certification in Paramedical Tattooing

Suggested (61): `Paramedical Tattoo Certification & Training | Dr. Rusnak Academy` — leads with the
term people search for instead of the brand name. Eleven other pages are also over 60 characters
but read acceptably; the homepage is the one worth changing.

### 6. Add the brand suffix to two blog titles
Every page uses `… | Dr. Rusnak Academy` except these two, which is inconsistent in results:

- `/blog/paramedical-vs-cosmetic-tattooing/`
- `/blog/paramedical-tattoo-compliance-framework/`

### 7. Thicken the four program pages
These are the pages that convert, and they are the thinnest substantive pages on the site:
`/programs/paramedical-tattoo-certification/` 577 words, `/programs/areola-masterclass/` 600,
`/programs/powder-botox/` 600, `/programs/mastering-paramedical-billing/` 607. The blog entries run
981–2,081 words. `/contact/` at 258 words and `/programs/` at 473 are hub pages and are fine as is.

Each program page already has strong internal linking and 4 structured-data blocks. Adding
curriculum detail, prerequisites, assessment criteria and outcomes would roughly double the body
copy on the highest-value URLs.

### 8. Set width and height on images
None of the 11 homepage images declare `width`/`height`, which causes layout shift as they load
(a Core Web Vitals CLS cost). 7 of 11 are lazy-loaded, which is correct. Also worth noting: 11
external stylesheets, 38 KB of inline CSS and 5 Google Fonts references on the homepage — an
Elementor default that is worth a pass if Core Web Vitals ever flags the site.

## Search Console notices, reconciled

| Notice | Date | Status on the live site |
| --- | --- | --- |
| Alternate page with proper canonical tag | Jul 18 | **Live** — caused by `/blog/page/2/` (action 3) |
| Not found (404) | Jul 3 | **Not reproducible** — all 24 sitemap URLs return 200 |
| Page with redirect | Jul 3 | **Not reproducible** — no sitemap URL redirects |
| Excluded by 'noindex' tag | Jul 3 | **Not reproducible** — all 24 pages are `index, follow` |

The three Jul 3 reasons date from the build period (the site was verified in Search Console on
Jun 18) and the live site no longer exhibits any of them. If they are still listed in the indexing
report, open each and click **Validate Fix**.

## What is already correct

- 24/24 sitemap URLs return HTTP 200; no redirects or errors inside the sitemap.
- Self-referencing canonical on every page, all matching the sitemap URL exactly.
- `index, follow, max-image-preview:large` on all 24 pages.
- `http://` → `https://`, `www` → non-`www`, `/index.php/` and `/home/` all 301 to the canonical host.
- No duplicate titles and no duplicate meta descriptions anywhere on the site.
- Every image on every page has an `alt` attribute — no missing and no empty values.
- Structured data on all 24 pages (1–5 `application/ld+json` blocks each); `og:image` on all 24.
- `robots.txt` is clean (`Disallow:` empty) and declares the sitemap.
- `/?p=1` and `/author/admin/` correctly return 404.
- Blog content is substantial: ten entries averaging ~1,400 words.

## Method note

Live page fetching **worked for all six portfolio domains** during this review. The
`site-inventory.md` and `seo-site-review.md` claim that the environment network policy blocks these
domains is out of date and has been corrected in both files.
