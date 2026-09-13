---
type: strategy
area: content
updated: 2026-09-13
owner: Earl Rusnak
status: proposal
---
# Bilingual (English / Spanish) web and blog strategy, Rusnak ecosystem

Scope: healing-skin.com, acumedgroup.com, drrusnakacademy.com (WordPress) and drrusnakwellness.com (Shopify Basic). voip-int.com is national B2B on Odoo and is out of scope for Spanish. Facts about the sites come from `brand-facts.md`; tool facts were checked live on 2026-09-13 (sources at the end). Note: the brief's line "no site currently states Spanish-speaking staff, so do not claim it" is superseded by this proposal once Earl confirms Phase 0.

## 1. Recommendation in five lines

1. Start with **acumedgroup.com**: it has the strongest local Spanish intent ("acupuncture near me" is its fastest-growing query), a Google Business Profile, and a fully bilingual clinical staff.
2. Use **Polylang (free)** with the `/es/` subdirectory pattern; SEOPress already lists Polylang as a supported multilingual plugin and builds per-language sitemaps.
3. Roll the same stack to **healing-skin.com** second; Rank Math v1.0.276 added native Polylang compatibility, so the old `rank-math-ppl.php` workaround is no longer needed.
4. On **drrusnakwellness.com** use Shopify's free **Translate & Adapt** app: it publishes Spanish at `/es`, adds hreflang and sitemap entries automatically on the Basic plan, and covers products, collections, pages and blog posts.
5. Every Spanish page is Claude-drafted and reviewed by a bilingual staff member before publishing; no machine-only Spanish goes live. Defer drrusnakacademy.com to Phase 3.

## 2. Why Spanish is a competitive advantage here

Kissimmee and Osceola County are heavily Spanish-speaking. Most competitors that show Spanish online are running a machine-translation widget over English pages while the phone and intake form stay English. Dr. Cecilia Rusnak and her entire clinical and training staff speak Spanish natively. That is a real experience and trust signal (Google's E-E-A-T), not a translation layer: a Spanish speaker who reads "consulta en español con la Dra. Rusnak" can call, book, fill out intake and be treated in Spanish.

The conversion asset is the whole path, not the page; the site only has to promise, accurately, what the clinic already delivers. That also keeps us clear of Google's spam policy, which names "translating" among the automated transformations that count as scaled content abuse when little value is added. Earl not being fluent is why section 5 puts a native-speaker review between drafting and publishing and locks brand terms in a glossary.

## 3. Architecture options

| Option | How it works | SEO | Effort | Verdict |
| --- | --- | --- | --- | --- |
| **Subdirectory `/es/` with hreflang (recommended)** | Language plugin creates a linked Spanish twin for each page at `site.com/es/...`; hreflang pairs EN and ES; one sitemap per language. | Clean. Google lists subdirectories as "easy to set up" and "low maintenance (same host)". Domain authority is shared. | Plugin install plus 6 to 8 pages per site to start. | Do this. |
| **Separate Spanish posts on the same blog, no language plugin** | Publish Spanish articles as ordinary posts, e.g. `/primera-cita-de-acupuntura/`, tagged "Español". | Messy. No hreflang, so Google cannot pair EN and ES versions; the Spanish post competes with the English one for the same intent, category and tag archives mix languages, RSS and email digests send Spanish to English readers, and menus, footers and CTAs stay in English around Spanish copy. | Lowest possible. | Acceptable only as a two-week bridge for one or two posts before Phase 1. Not the destination. |
| **Separate Spanish domain (e.g. acumedgroup.es or es-acumedgroup.com)** | Standalone site per language. | Splits authority across two domains with tiny click volumes (166/mo today), doubles hosting, plugins, NAP and GBP maintenance, and a .es TLD geotargets Spain, not Florida. | Highest. | Rejected. |

## 4. Per-site plan

### healing-skin.com (WordPress, Rank Math)
- Plugin: Polylang free. Rank Math has native Polylang support since v1.0.276 (sitemaps, canonicals, redirects); confirm the version first and remove any old `rank-math-ppl.php`.
- URL pattern: `healing-skin.com/es/camuflaje-de-cicatrices/` (Polylang's "language code in URL" option). Translate slugs where Polylang free allows; if slug translation for custom post types becomes a blocker, Polylang Pro is 99 EUR/year per site.
- Order: service pages first (`/scar-camouflage/`, `/stretch-mark-camouflage-tattoo/`, `/3d-areola-tattoo/`, `/paramedical-tattoo-training/`, `/dr-rusnak/`), then contact and booking (the GoHighLevel widget needs a Spanish form or at least Spanish labels), then the aftercare timeline post and the Orlando local posts.
- Rank Math: translate focus keyword, SEO title and meta description per language; keep FAQPage schema in Spanish on the Spanish page only.

### acumedgroup.com (WordPress, SEOPress)
- Plugin: Polylang free. SEOPress documents Polylang as compatible and generates language-specific sitemaps and translated metadata.
- URL pattern: `acumedgroup.com/es/acupuntura/`, `/es/ventosas/`, `/es/masaje-medico/`, `/es/para-veteranos/`, `/es/personal/`, `/es/contacto/`.
- Order: acupuncture, cupping, medical massage, homeopathic pain injections, staff, for-veterans, contact (7 pages), then the first-visit post, then Traumeel and Qi posts (already growing).
- Keep "Kissimmee, FL" in Spanish titles and H2s exactly as the English posts do.

### drrusnakacademy.com (WordPress)
- Defer. The training audience is national and searches in English. Phase 3 only: a Spanish landing page for the Orlando cohorts and one Spanish-first post on Florida licensing for Latin American trained artists. Same Polylang free stack.

### drrusnakwellness.com (Shopify Basic)
- Tool: Translate & Adapt (free, by Shopify). Settings > Languages > add Spanish, then publish; Shopify serves it at `drrusnakwellness.com/es` and states "Hreflang tags are added automatically, and all published languages are included in sitemaps." Available on all plans except Lite; Basic allows up to 20 languages.
- No separate Market is needed for one language on the primary domain. Do not enable browser-language auto-redirect; Google advises against it.
- Auto-translate is capped at two languages per store and does not run on new content automatically; use it as a first-pass draft only, then edit in the side-by-side editor after staff review.
- Order: the nine in-stock product pages, the Scar Care, Sensitive Skin and Sun Care collection pages, About and shipping/returns policy (policies are manual-only), then the post-procedure skincare post and the silicone gel guide. Cosmetic-claim firewall applies word for word in Spanish.

## 5. Content workflow (Earl is not fluent)

1. **Draft (Claude, 20 to 40 min).** Spanish version of the approved English page in neutral Latin American Spanish for Central Florida (Puerto Rican, Colombian, Venezuelan and Mexican readers), "usted" for patients and students, no regional slang, same H2 structure and links. Titles and meta descriptions are written for Spanish search intent, not translated literally.
2. **Review (bilingual Clinical Coordinator or Lead Trainer, 10 min).** Checks clinical accuracy, tone, and that nothing in the glossary was altered. Marks changes in the WordPress or Shopify editor directly.
3. **Publish (Earl or the web admin, 5 min).** Link the ES page to its EN twin in Polylang or publish in Translate & Adapt so hreflang pairs are complete in both directions; Google ignores hreflang without return links.
4. **Log.** Add the URL to the content round file with reviewer role and date.

### Glossary: never translate
Healing Skin Medical Aesthetics; AcuMedGroup; Dr. Rusnak Academy; Dr. Rusnak Wellness; Paramedical Artists Academy; Calm Flow; Qi Restore Oil; Qi Firm; Qi Revive; Qi Wash; Advanced ISR; 3D Areola (as a product/program name); VA Community Care; Cherry, Klarna, Affirm; MoCRA; the credential string `Dr. Cecilia Rusnak, LME, AP, DAc` (never expanded, never localized).

### Glossary: translate with care
| English | Spanish (use) | Note |
| --- | --- | --- |
| paramedical tattooing | tatuaje paramédico | Not "micropigmentación" alone; add it once as a synonym for search. |
| scar camouflage | camuflaje de cicatrices | Not "borrado" or "eliminación"; we do not claim removal. |
| stretch marks | estrías | Universal. |
| 3D areola tattoo | tatuaje de areola 3D | Keep "3D". |
| acupuncture physician | médico acupunturista (título en Florida: Acupuncture Physician, AP) | State the Florida title in English once on the staff page. |
| licensed esthetician | esteticista licenciada (Licensed Medical Esthetician, LME) | Same pattern. |
| medical massage | masaje médico | Not "masaje terapéutico" alone. |
| cupping | terapia con ventosas | "Cupping" in parentheses on first use. |
| aftercare | cuidados posteriores | Not "postratamiento" as a noun. |
| improves the look of | mejora la apariencia de | Wellness firewall wording. |

## 6. Spanish keyword starter list (10 per site)

**acumedgroup.com:** acupuntura cerca de mí Kissimmee · acupuntura en Kissimmee FL · acupuntura para el dolor de espalda Kissimmee · acupuntura para la ansiedad Orlando · acupunturista que habla español Kissimmee · primera cita de acupuntura qué esperar · acupuntura cubierta por el VA veteranos Florida · terapia con ventosas Kissimmee · masaje médico Kissimmee · medicina china tradicional Orlando

**healing-skin.com:** camuflaje de cicatrices Orlando · tatuaje paramédico Kissimmee · tatuaje de areola 3D Orlando · camuflaje de cicatriz de cesárea · tatuaje para estrías Florida · reconstrucción de areola después de mastectomía Orlando · camuflaje de cicatrices en piel morena · cuánto cuesta el camuflaje de cicatrices · cuidados después de un tatuaje paramédico · clínica de tatuaje paramédico que habla español

**drrusnakwellness.com:** protector solar mineral después de un procedimiento · gel de silicona para cicatrices · cuidado de la piel después de un tatuaje paramédico · crema para estrías con péptidos · agua micelar para piel sensible · rutina de cuidado post procedimiento · sérum de péptidos para cicatrices · ácido azelaico para manchas · limpiador suave sin enjuague · kit de cuidados posteriores

**drrusnakacademy.com (Phase 3):** curso de tatuaje paramédico · certificación en tatuaje paramédico Florida · curso de camuflaje de cicatrices · curso de areola 3D Orlando · formación en micropigmentación médica · requisitos para tatuar en Florida licencia · curso de tatuaje paramédico en español · cuánto gana un tatuador paramédico · escuela de tatuaje paramédico Orlando · facturación de seguros tatuaje paramédico

## 7. Staged rollout

| Phase | When | Work | Effort |
| --- | --- | --- | --- |
| **0** | September 2026 | "Se habla español" line in header or footer and on contact pages of the three clinic-facing sites; Spanish paragraph inside the GBP description for AcuMedGroup and Healing Skin (single-language field, so keep it to two sentences); turn on the GBP language attribute if the category offers it; Spanish call-to-action in one GBP post per month (separate post per language); 5-question Spanish FAQ on both contact pages; add "Preferred language" field to booking and contact forms. | 4 to 6 hours total, no plugins. |
| **1** | October 2026 | Install Polylang on acumedgroup.com, then healing-skin.com; 7 core pages each per section 4; Shopify: add Spanish, translate 9 product pages, 3 collections, About, policies. Verify hreflang pairs in Search Console after indexing. | 2 days admin plus about 3 hours of staff review across all pages. |
| **2** | November 2026 | Translate the September round: AcuMedGroup first-visit post first, then Healing Skin aftercare timeline, then the Wellness post-procedure post. Add Spanish versions of the two growing AcuMedGroup evergreen posts (Traumeel, Qi). | 1 day drafting, 1 hour review. |
| **3** | January 2027 onward | Spanish-first originals where the search behaviour is Spanish-native: "acupuntura y seguro médico en Florida", "camuflaje de cicatrices de cesárea: lo que preguntan las mamás en Kissimmee", Academy Orlando-cohort landing page, WAPA Orlando partnership content, Spanish-first hub link page and reels per the Brand House doc. | 1 post per site per month. |

## 8. Measurement

- Search Console: Performance filtered by page contains `/es/` (WordPress) or `/es` (Shopify) per property; clicks, impressions and top Spanish queries monthly. Baseline is zero; target 15 percent of acumedgroup.com clicks from `/es/` within six months.
- Search Console International Targeting / hreflang errors report: zero "no return tags" errors.
- GBP: calls and website clicks from the Spanish-language posts and the profile once the Spanish paragraph is live, compared with the prior 90 days.
- Booking and contact forms: count of "Español" in the new preferred-language field. This is the only direct measure of conversion, so add it in Phase 0.
- Shopify: sessions and orders by landing page `/es/`.

## 9. Risks and guardrails

- **No machine-only Spanish goes live.** Every page passes the bilingual staff review. Google's spam policy explicitly lists translation as an automated transformation that becomes abuse when little value is added.
- **Credential string stays identical** in Spanish: `Dr. Cecilia Rusnak, LME, AP, DAc`. Never "Dra. Cecilia Rusnak, PhD" or expanded titles in place of the string.
- **Compliance firewall applies equally.** Wellness pages use cosmetic claims only ("mejora la apariencia de", "ayuda a que la piel se sienta"); no "cura", "trata", "elimina". Clinic sites keep the honesty lines ("ninguna técnica de camuflaje elimina por completo una cicatriz").
- **Separate NAP per brand** in Spanish too: each site's own phone, its own GBP, no "la misma clínica" language.
- **No browser-language redirects** and no hreflang without return links.
- **Do not translate the URL slugs of pages that already rank** in English; Spanish slugs live only under `/es/`.
- **Plugin drift:** re-check Rank Math and Polylang compatibility after major updates; keep SEOPress and Polylang on current versions.

## 10. Open decisions for Earl

1. Approve the "Se habla español" claim for public use on Healing Skin, AcuMedGroup and Wellness, and name the staff role that owns the 10-minute review (Clinical Coordinator at AcuMedGroup, Lead Trainer at Healing Skin).
2. Confirm Polylang free for both WordPress clinic sites, or choose WPML Multilingual CMS (99 EUR, 3 sites) if you want automatic translation credits and one licence for all three WordPress sites.
3. Decide whether the GoHighLevel booking pages get a full Spanish form in Phase 1 or Spanish labels only.
4. Confirm the Academy stays English-first until January 2027 and whether the Orlando cohort landing page is the first Spanish Academy asset.
5. Set the Phase 0 budget cap for the GBP work and the form field (estimate 4 to 6 hours of admin time) and decide who executes it.

## Sources checked 2026-09-13

- Polylang pricing: https://polylang.pro/pricing/ (Pro from 99 EUR/year, 50 percent renewal discount) and https://wordpress.org/plugins/polylang/ (800,000+ installs; language code in URL, subdomain or domain per language; no language limit)
- WPML pricing: https://wpml.org/purchase/ (Blog 39 EUR / 1 site; CMS 99 EUR / 3 sites, 90,000 credits; Agency 199 EUR)
- TranslatePress pricing: https://translatepress.com/pricing/ (Personal 99 EUR / 1 site with SEO Pack; Business 199 EUR / 3 sites; Developer 349 EUR)
- Weglot pricing: https://www.weglot.com/pricing (Starter $17/mo, 1 language, 10,000 words; Business $32/mo, 3 languages, 50,000 words)
- Rank Math and Polylang: https://rankmath.com/kb/polylang-compatibility/ (native compatibility since v1.0.276; legacy workaround last updated Jul 14, 2026)
- SEOPress and Polylang: https://www.seopress.org/support/guides/seopress-polylang-multilingual-seo-guide/ and https://www.seopress.org/support/faq/which-multilingual-plugins-are-compatible-with-seopress/
- Shopify languages: https://help.shopify.com/en/manual/markets/languages and https://help.shopify.com/en/manual/markets/languages/setup (subfolder URLs, automatic hreflang and sitemaps, all plans except Lite, 20 languages on Basic)
- Shopify Translate & Adapt: https://help.shopify.com/en/manual/markets/languages/translate-adapt-app and https://apps.shopify.com/translate-and-adapt (free; auto-translate up to two languages; products, collections, blog posts, policies, pages, theme content; policies manual only)
- Google localized versions and hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions
- Google multi-regional guidance (URL structures, no auto-redirect): https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- Google spam policies, scaled content abuse: https://developers.google.com/search/docs/essentials/spam-policies
- Google Business Profile description guidelines: https://support.google.com/business/answer/3038177
- GBP language assistance attribute (healthcare since Dec 2021, expanding): https://www.seroundtable.com/google-business-profiles-expanding-language-assistance-options-35399.html
- GBP bilingual listing practice (single-language description, separate posts per language): https://www.dacgroup.com/insights/blog/search-optimization/everything-you-need-to-know-about-bilingual-business-listings/ and https://inboundrem.com/google-business-profile-languages/
