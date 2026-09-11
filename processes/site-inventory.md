---
type: reference
area: seo
updated: 2026-09-10
---
# Site inventory

| Domain | Business | Platform | In Ahrefs Site Audit | In Search Console | Notes |
| --- | --- | --- | --- | --- | --- |
| healing-skin.com | Healing Skin Medical Aesthetics (clinic + paramedical tattoo training) | WordPress | Yes (project "Healing-skin") | Yes | Revenue site; Meta ads land here |
| acumedgroup.com | AcuMedGroup medical clinic | WordPress | Yes ("Acumedgroup") | Yes | #1 profit center; Health Score 77 on Aug 29 |
| drrusnakwellness.com | Dr. Rusnak Wellness | Shopify | Yes ("Drrusnakwellness") | Yes | 4xx indexing fix under validation since Sep 7 |
| drrusnakacademy.com | Dr. Rusnak Academy | WordPress | No | Yes | Milestone: 50 clicks / 28 days (Aug 13) |
| voip-int.com | VoIP International | Odoo | Yes ("Voip-int") | Yes | Crawl unblocked Jul 2–7; Jul 18 GSC alerts (robots-block hides noindex; sitemap lists a redirect + noindexed URLs) still open — see [voip-int-crawl-unblock](voip-int-crawl-unblock.md) |
| 3390oceanshore.com | Ormond Beach condo listing | Unknown | No | Yes | Temporary property; on market through 12/31/2026 |

Ahrefs crawl emails arrive forwarded from info@drrusnakwellness.com to itself with the subject prefix
`[voip-int] (Project name)`. Search Console emails come from sc-noreply@google.com.

Live page fetches from the Claude cloud environment are currently blocked by the environment's network policy
for all six domains (environment "Default", trusted network access). To enable live checks, open claude.ai/code ›
Environments › Default › Network access, choose custom allowed domains, and add:

```
voip-int.com  www.voip-int.com  voip-int.us  voip-int.co.uk
healing-skin.com  www.healing-skin.com
acumedgroup.com  www.acumedgroup.com
drrusnakwellness.com  www.drrusnakwellness.com
drrusnakacademy.com  www.drrusnakacademy.com
3390oceanshore.com  www.3390oceanshore.com
web.archive.org  archive.org
```

The policy is applied when a session starts, so sessions opened before the change keep the old policy.
