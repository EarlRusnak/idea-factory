# Crawl-block audit — https://voip-int.com

## robots.txt (HTTP 200)

```
User-agent: *
Allow: /social_instagram/
Sitemap: https://voip-int.com/sitemap.xml


##############
#   custom   #
##############

User-agent: *
Allow: /cards/

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
```

## sitemap.xml — 154 URLs

## Sitemap conflicts (what Search Console's 2026-07-18 alerts point at)

### Sitemap URLs that redirect, are noindexed, robots-blocked or non-200

None.

### Must-rank pages with a problem

| URL | HTTP | → Location | robots | noindex source | flags |
|---|---|---|---|---|---|
| https://voip-int.com/call-retrieve | 404 |  | allowed |  | MISSING_FROM_SITEMAP, NON200(404) |
| https://voip-int.com/message-waiting-indicator-mwi | 404 |  | allowed |  | MISSING_FROM_SITEMAP, NON200(404) |

### Must-not-rank pages (mechanism check)

| URL | HTTP | → Location | robots | noindex source | flags |
|---|---|---|---|---|---|
| https://voip-int.com/web/login | 200 |  | allowed | X-Robots-Tag: noindex, nofollow |  |
| https://voip-int.com/my | 303 | /web/login?redirect=%2Fmy%3F | BLOCKED |  |  |
| https://voip-int.com/get-started/thank-you | 200 |  | allowed | robots=noindex |  |
| https://voip-int.com/contactus | 301 | /contact | allowed |  | REDIRECTS_OK |
| https://voip-int.com/shop | 200 |  | allowed | X-Robots-Tag: noindex |  |

### Legacy blog namespace

| URL | HTTP | → Location | robots | noindex source | flags |
|---|---|---|---|---|---|
| https://voip-int.com/blog/voip-international-blog-posts-2/anything-at-all-000 | 301 | /blog | allowed |  | LEGACY_301_OK |
| https://voip-int.com/blog/voip-international-blog-posts-2/tag/voip | 301 | /blog | allowed |  | LEGACY_301_OK |

### Clean sitemap URLs: 154 of 154
