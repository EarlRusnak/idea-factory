---
type: edit-spec
area: web
status: ready-to-apply
blocked_on: wp-admin session on Earl's Mac (Cloudflare challenge blocks cloud sessions)
decided: 2026-09-16
decided_by: Earl Rusnak
---
# Pending edits — Powder Botox date + paramedical format

Two decisions from 2026-09-16 that require a logged-in `wp-admin` session. A Claude cloud session
cannot apply them: `wp-admin` returns 302 and Cloudflare challenges the login. Apply from the Mac
session that has Chrome signed in, using the same REST path used on 2026-09-11.

## Decision 1 — Powder Botox next class date is **November 6, 2026**

Replaces the "date confirmed at enrollment" placeholder that was put in on 2026-09-16 because no
real date existed at the time. A date now exists, so the placeholder should go.

**Site: healing-skin.com — page `/powder-botox-masterclass/`** (verified 2026-09-16; note that
`/powder-botox/` carries no date text and needs no change)

| Find (current live text) | Replace with |
| --- | --- |
| `Next cohort: Orlando. Date confirmed at enrollment.` | `Next cohort: Orlando · November 6, 2026` |
| `The next class date is confirmed on your enrollment call.` | `The next class is November 6, 2026 in Orlando.` |
| `Date confirmed at enrollment.` (details row value) | `November 6, 2026` |
| `Upcoming Class` (label, currently followed by no date) | keep label, ensure the value reads `November 6, 2026` |

Leave unchanged: Kissimmee clinic, 10 AM–4 PM, $2,350 all-in, $500 deposit.

**Site: drrusnakacademy.com — page `/programs/powder-botox/`**
The Format/schedule row is injected client-side, so the current value could not be read from the
raw HTML. Open the page in wp-admin and set the schedule value to `November 6, 2026 · Orlando`.
The "one-day intensive" wording is correct and stays — Powder Botox is one day; only the date changes.

Also check `/faq/`, which says "one-day intensive. Specific schedules are provided during the
candidacy conversation." That remains accurate and needs no edit.

## Decision 2 — Both paramedical certifications are **3 days: 1 day at home, 2 days in person**

**Site: healing-skin.com — page `/paramedical-tattoo-training/`**

- The foundation certification **already reads correctly**: "3-day certification includes 1 online
  day of theory followed by 2 [days in person]". No change needed.
- The 3D Areola Masterclass currently reads **"2-day certification covering 3D areola color
  restoration for post-mastectomy…"**. This is the mismatch. Change to:
  `3-day certification — 1 online day of theory followed by 2 days in person — covering 3D areola color restoration for post-mastectomy…`

**Site: healing-skin.com — the booking page**
Previously flagged as describing the certification as a "2-day class". Align it to
`3 days — 1 online, 2 in person`. Not reachable for verification from a cloud session; confirm the
current string before replacing.

**Site: healing-skin.com — page `/3d-areola-masterclass/`**
Not checked in this pass. Verify it does not also carry "2-day" before closing this out.

**Site: drrusnakacademy.com — page `/programs/areola-masterclass/`**
The Format row is injected client-side and could not be read from raw HTML. Confirm in wp-admin
that it reads 3 days / 1 online + 2 in person. The meta description no longer contains "2-day"
(it was rewritten on 2026-09-11), so only the on-page Format row is at issue.

## Verification after applying

1. Purge the CDN cache, then re-fetch each edited URL and confirm zero occurrences of
   `Date confirmed at enrollment`, `date is confirmed on your enrollment call`, and `2-day` on the
   areola pages.
2. Confirm every `application/ld+json` block still parses — the FAQ answers are duplicated into
   JSON-LD, so plain-text replacements must not inject HTML there.
3. Keep the WordPress revision for each page for rollback.

## Residual issue found while verifying

`pages/home.html` still contains three escaped references to
`acumedgroup.com/wp-content/uploads/2023/04/site-logo-highres.png`. The `og:image` **was**
successfully repointed to the Academy share card, but the AcuMed 2023 logo survives inside the
escaped JSON (Yoast's JSON-LD graph, most likely the Organization `logo` node). Worth clearing so
no AcuMed asset remains in the Academy's structured data.
