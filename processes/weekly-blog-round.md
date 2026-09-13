---
type: process
area: content
cadence: weekly
runs_at: Tuesdays 08:00 America/New_York (12:00 UTC)
routine_id: trig_01F6zJUf4w21ZBHryLzvG9jc
standing_page: https://claude.ai/code/artifact/d6e77af4-f12e-4213-aee6-6f387f53e888
depends_on: seo-site-review
owner: Earl Rusnak
status: active
created: 2026-09-13
---
# Weekly Blog Round

Every Tuesday morning Claude drafts one new blog post for each of the five sites (healing-skin.com,
acumedgroup.com, drrusnakwellness.com, drrusnakacademy.com, voip-int.com), generates a featured image and
an inline graphic for each, posts every article to its CMS as an **unpublished draft**, and reports to Earl.
Earl reviews and presses Publish. The round never publishes anything itself.

Cadence rule (Earl, 2026-09-13): one post per site per week is the floor. Search engines reward consistent
new, relevant content, so the backlog is kept deep enough to add a second post for the revenue sites when
Earl asks.

## Inputs
1. [content/brand-facts.md](../content/brand-facts.md): house rules, credential string, compliance firewall,
   per-site voice, verified link targets, prices and program facts. Updated whenever a fact changes.
2. [content/topic-backlog.md](../content/topic-backlog.md): ranked candidate topics per site with the reason
   each is there. The round takes the top unclaimed line unless a fresher signal justifies a swap.
3. [content/published-log.md](../content/published-log.md): everything drafted or published, to avoid repeats.
4. The latest Rusnak SEO Review Doc (Drive › Automated Reports) and the Search Console monthly emails in
   Gmail, for growing queries and pages.
5. Live page fetches of every URL and price a post will cite, and Shopify inventory for any product mentioned.

## What it produces
- `content/blog-drafts/YYYY-MM-DD/`: five markdown posts (front matter, publishing notes with FAQPage JSON-LD,
  body), `images/` (10 PNGs), `html/` (rendered bodies), and a README explaining topic choices.
- Drafts in each CMS, unpublished:
  - WordPress sites via `content/tools/publish.py wordpress <post.md>` (REST API, Application Passwords;
    uploads both images, sets featured image, categories, tags, excerpt, and Rank Math / SEOPress meta).
  - voip-int.com via `content/tools/publish.py odoo <post.md>` (XML-RPC; `blog.post` with `is_published`
    false, cover image, tags, meta title and description).
  - drrusnakwellness.com via the Shopify connector (`fileCreate` for images, `articleCreate` with
    `isPublished: false` on blog `gid://shopify/Blog/93843062884`, `articleUpdate` for the SEO metafields).
- Standing page updated in place; Google Doc "Weekly Blog Round — YYYY-MM-DD" in Drive › Automated Reports
  (Claude Routines); email to info@drrusnakwellness.com with each site, title, review location, and blockers.
- Repo commit to the default branch with the round folder and the backlog / log updates.

## Credentials (stored in the Claude environment, never in the repo)
| Site | Variables | How Earl creates them |
| --- | --- | --- |
| healing-skin.com | `HS_WP_USER`, `HS_WP_APP_PASSWORD` | WordPress › Users › (an Editor account) › Application Passwords › name "Claude blog round" |
| acumedgroup.com | `ACU_WP_USER`, `ACU_WP_APP_PASSWORD` | same |
| drrusnakacademy.com | `ACAD_WP_USER`, `ACAD_WP_APP_PASSWORD` | same |
| voip-int.com | `ODOO_LOGIN`, `ODOO_API_KEY` (optional `ODOO_URL`, `ODOO_DB`; defaults https://voip-int.com, voipintl19) | Odoo › Preferences › Account Security › New API Key |
| drrusnakwellness.com | Shopify connector attached to the Routine (preferred). Optional token path: `SHOPIFY_STORE`, `SHOPIFY_ADMIN_TOKEN` | claude.ai › Routines › this Routine › connectors |

Add the variables in claude.ai › Code › Environments › (this environment) › Environment variables. Connector
grants cannot be set from inside a session in this organization, so the Shopify, Gmail, Google Drive and
Higgsfield connectors must be attached to the Routine in claude.ai › Routines (same step the other three
Routines needed).
Until a credential exists, the round still writes the post and the HTML and reports exactly what is missing.

## Quality gates (each post)
- Facts, prices, dates and links verified live the same day; nothing invented.
- Voice, length and structure per brand-facts.md; credential string exact; no em-dashes or emojis.
- Focus keyword in title, slug, first 100 words, one H2, meta description; FAQ with FAQPage JSON-LD.
- Cross-links only where there is direct context; voip-int.com never linked to or from the Rusnak sites.
- Images reviewed by eye: no typos in graphics, no odd anatomy, no logos or real likenesses.
- Compliance firewall on drrusnakwellness.com: founder / curator voice, cosmetic claims only.

## Seed run (2026-09-13)
Five posts drafted and reviewed; images generated; Shopify draft created (article 569887260772); the four
other CMS drafts are waiting on credentials. Spanish pilot of the AcuMedGroup post drafted, pending bilingual
staff review. See [content/blog-drafts/2026-09/README.md](../content/blog-drafts/2026-09/README.md).

## Upgrade path
- Bilingual: once Polylang / Translate & Adapt are in place (see content/bilingual-strategy-2026-09.md), the
  round drafts the Spanish twin of each Rusnak post and posts it as the linked translation, flagged for staff review.
- Second weekly post for healing-skin.com and acumedgroup.com when Earl says go.
- Replace generated featured photos with consented clinic photography as it becomes available.
