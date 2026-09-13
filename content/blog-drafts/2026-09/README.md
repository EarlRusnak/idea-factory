---
type: content-round
area: content
round: 2026-09
created: 2026-09-13
owner: Earl Rusnak
status: approved by Earl 2026-09-13; publishing in progress
---
# September 2026 blog round — one post per site

Five posts, one per brand, chosen from the Search Console signals, the May 2026 Healing Skin gap analysis,
the July 2026 VoIP SEO audit, and the Brand House hub-and-spoke rules. Shared facts and house rules live in
[_brief-and-facts.md](_brief-and-facts.md). Each post file carries its own front matter, publishing notes,
schema block, and body.

| Order | Site | Post | Why now | Focus keyword |
| --- | --- | --- | --- | --- |
| 1 | voip-int.com | What Are All Those Fees on Your Business Phone Bill? | The July audit named a fee-transparency explainer the most ownable, linkable asset for the "operator, not a reseller" position. It also gives the FAQ's "15–25%" line a long-form home that AI assistants can quote. | VoIP taxes and fees |
| 2 | healing-skin.com | Paramedical Tattoo Aftercare: A Day-by-Day Healing Timeline | Ranked HIGH in the gap analysis (Category 7) and still unwritten. Aftercare content converts booked patients into reviews and touch-ups, and it is the natural bridge to Dr. Rusnak Wellness products. | paramedical tattoo aftercare |
| 3 | acumedgroup.com | Your First Acupuncture Appointment in Kissimmee, FL | "acupuncture near me" (+6) and "chinese medicine near me" (+4) were August's fastest-growing queries. This is the decision-stage page that turns those searchers into a first visit. | first acupuncture appointment |
| 4 | drrusnakwellness.com | Post-Procedure Skincare | The store has a Post-Procedure Aftercare Kit and Scar Care collection with no editorial page pointing at them. Publishes after the Healing Skin post so the cross-links resolve. | post-procedure skincare |
| 5 | drrusnakacademy.com | How to Evaluate a Paramedical Tattoo Training Program | "paramedical tattoo training near me" is growing; New York (Oct 9–10), Orlando (Nov 13–14) and Las Vegas (Dec 4–5) cohorts are open; the Academy blog has technique and compliance briefs but no decision-stage piece. | paramedical tattoo training program |

## Earl's decisions (2026-09-13)

- **Cadence:** one post per site per month is the floor, not the target. Search engines reward consistent new,
  relevant content, so plan for more, starting with the two revenue sites.
- **Cross-brand linking:** link whatever is relevant when there is direct context. Healing Skin, AcuMedGroup,
  Dr. Rusnak Wellness and the Academy may all link to each other. Only voip-int.com stays unlinked from the
  Rusnak sites (and they from it).
- **Spanish:** Dr. Cecilia Rusnak and her entire clinical and training staff are bilingual (Earl is not fluent).
  "Se habla español" lines are now in the AcuMedGroup and Healing Skin posts. The full plan is in
  [../../bilingual-strategy-2026-09.md](../../bilingual-strategy-2026-09.md); the Spanish pilot of the
  AcuMedGroup post is in [es/](es/).
- **Instructor:** Dr. Rusnak teaches every Academy cohort personally; the Academy post now says so.
- **VoIP cost recovery:** reframed as a pass-through of the FCC regulatory fees the company pays as a licensed
  operator, itemized by name. No "provider-set" framing for VoIP International's own line.
- **Wellness inventory:** the Post-Procedure Aftercare Kit sentence was cut (kit at zero units). Re-add when restocked.
- **Images:** every post ships with a featured image and one inline graphic (see images/), generated 2026-09-13.
  Regenerate or replace with clinic photography whenever real, consented imagery exists.
- **Publishing:** Earl wants every post pasted, not just delivered as files. Status below.

## Publishing status

| Site | Platform | Status (2026-09-13) | What is needed to finish |
| --- | --- | --- | --- |
| drrusnakwellness.com | Shopify | **Draft created** on the News blog (unpublished), both images on the Shopify CDN, handle `post-procedure-skincare-guide` | Publish after the Healing Skin post is live (its link points there). |
| healing-skin.com | WordPress (Rank Math) | HTML + images ready in html/ and images/ | A WordPress Application Password for an Editor account, added to the Claude environment as `HS_WP_USER` / `HS_WP_APP_PASSWORD`. |
| acumedgroup.com | WordPress (SEOPress) | HTML + images ready | Same: `ACU_WP_USER` / `ACU_WP_APP_PASSWORD`. |
| drrusnakacademy.com | WordPress | HTML + images ready | Same: `ACAD_WP_USER` / `ACAD_WP_APP_PASSWORD`. |
| voip-int.com | Odoo 19 | HTML + images ready | `ODOO_API_KEY` for earl.rusnak@voip-int.com (the same pattern the July SEO scripts used), added to the Claude environment. |

Images are in images/ (PNG, 1344x752). The `build_html.py` script rebuilds html/ from the markdown; pass
`image-hosting.json` to swap local image paths for hosted URLs once each CMS has the files.

## Cross-link map (brand development, not brand blending)

- Healing Skin post → acumedgroup.com/staff/ (credentials), drrusnakwellness.com products and the store's
  post-procedure post (aftercare), Academy not linked (patient audience).
- Wellness post → healing-skin.com aftercare timeline (clinical detail), healing-skin.com home (where
  treatments happen). Founder/curator voice only.
- Academy post → healing-skin.com training-cost and financing posts (the training funnel still lives on
  healing-skin.com), Academy program pages, Academy briefs.
- AcuMedGroup post → AcuMedGroup pages and posts (no direct context for a cross-brand link in this post). Distinct local footprint is kept via separate NAP, not by avoiding links.
- VoIP post → VoIP pages and posts only.

## Publish order and dependencies

1. VoIP fees post (no dependencies).
2. Healing Skin aftercare (links forward to the store post; add that link after step 4 if publishing strictly in order).
3. AcuMedGroup first visit (no dependencies).
4. Wellness post-procedure (needs step 2 live for its clinical-timeline link).
5. Academy evaluation guide (no dependencies; publish before the Oct 9 New York cohort).

## Things to confirm before publishing (collected from the post files)

- Dr. Rusnak Wellness inventory: the Post-Procedure Aftercare Kit, Calm Flow Water Cream, Qi C+, Qi Brightening
  and Qi Clear show zero units in Shopify on Sep 13. The store post leans on in-stock items and mentions the
  kit once. Restock or swap before publishing.
- The Healing Skin aftercare guidance in the post mirrors the /scar-camouflage/ service page (dry, no sun,
  silicone gel twice daily for 4–6 weeks, SPF 40 daily, retinol after week 4). Cecilia should confirm this is
  also the protocol she wants stated for 3D areola work on post-mastectomy and radiated skin.
- AcuMedGroup: confirm single-use sterile needles and whether new-patient intake forms are online.
- VoIP: confirm the pricing page still shows $17 / $29 and that the 10-seat illustrative example matches
  current pass-through math for a Florida service address.
- Academy: confirm tuition and cohort dates on publish day.
