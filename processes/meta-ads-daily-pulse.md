---
type: process
area: paid-social
cadence: daily
runs_at: 08:30 America/New_York (12:30 UTC)
routine_id: trig_01XpMUAQaVtaeR1ve7ZVwZcW
standing_page: https://claude.ai/code/artifact/e19616c9-1689-4037-80fa-f0af004b1e2a
owner: Earl Rusnak
status: active
created: 2026-09-10
---
# Meta Ads Daily Pulse

Daily report on Meta ad spend across Facebook and Instagram for the Healing Skin Medical Aesthetics
ad account, with accurate results, trends, and recommendations for Earl to review. Read-only: the
process never changes a campaign, budget, or ad.

## Inputs
- Meta Ads connector, ad account `809336507910420` (Healing Skin Medical Aesthetics), plus a spend check on
  `830439745878632` (Open Ad Account Acumed).
- Three further accounts are disabled by Meta and only listed in the account-health table:
  `1339425383084679`, `494756093493604`, `10150144726264819`.

## What it pulls
1. Yesterday, campaign level, broken down by publisher platform (Facebook / Instagram): spend, impressions,
   clicks, results, cost per result, CTR, CPC, reach, frequency.
2. Yesterday totals without breakdown, to reconcile the platform rows.
3. A 14-day daily series per campaign for trend lines.
4. 7-day and 28-day rollups, with and without the platform breakdown.
5. Meta's anomaly signal and performance-trend analysis.
6. Paused campaigns that still spent in the last 7 days.

## Accuracy rules
- All totals are computed in a script from the raw tool output.
- Result types are never mixed (form leads vs landing-page views vs purchases).
- Every report states that Meta can revise the previous day's figures for up to 72 hours.
- Missing data is named, never estimated.

## Outputs
- Standing page updated in place (same URL every day).
- Google Doc "Meta Ads Daily Pulse — YYYY-MM-DD" in Drive › Automated Reports (Claude Routines).
- Email to info@drrusnakwellness.com with KPI line, top trends, recommendations, and links.
- Push + email notification from the Routine when the run finishes.

## Report structure
Header (report day, generated stamp) · Yesterday at a glance (spend, FB, IG, leads, CPL, landing-page views) ·
Campaign breakdown table with FB and IG columns · Trends to watch · Recommendations for review (trigger condition
plus proposed move) · Account health · Footer describing the process.

## Seed run (Sep 9, 2026 data)
Spend $151.85 across 7 active campaigns; Facebook $113.86, Instagram $37.93; 41 form leads at $2.75 blended
(FB $2.32, IG $6.75); 96 landing-page views on the two traffic campaigns.
