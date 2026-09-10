# idea-factory

Earl Rusnak's process library. Each process here is a scheduled Claude Routine that
produces a standing report page, a Google Doc copy for the Obsidian second brain, and
an email summary. The Markdown files are written to be dropped straight into the vault.

| Process | Cadence (ET) | Standing page | Routine ID |
| --- | --- | --- | --- |
| [Meta Ads Daily Pulse](processes/meta-ads-daily-pulse.md) | Daily 8:30 AM | https://claude.ai/code/artifact/e19616c9-1689-4037-80fa-f0af004b1e2a | `trig_01XpMUAQaVtaeR1ve7ZVwZcW` |
| [Ahrefs Health Report](processes/ahrefs-health-report.md) | Mondays 9:00 AM | https://claude.ai/code/artifact/26cb3b0b-ddf5-47fa-be28-15134bbe8a92 | `trig_01F7vMNr5Wz5doUVy3exq9by` |
| [Rusnak SEO Review](processes/seo-site-review.md) | Wednesdays 9:00 AM | https://claude.ai/code/artifact/2ef21298-a12c-4698-8c0a-fb61fb6315ab | `trig_013AxiYoyAmWVTraE7W5ADAu` |

Shared outputs

- Google Drive folder for Doc copies: **Automated Reports (Claude Routines)**, inside the Mission Control folder
  (folder id `1kUddIH6aN9ky8tgrpPQmzdQvKGMtxJBy`).
- Email summaries go to info@drrusnakwellness.com.
- Rows ready to paste into the Mission Control task tracker: [mission-control/rows.md](mission-control/rows.md).
- Site inventory used by the SEO processes: [processes/site-inventory.md](processes/site-inventory.md).
- One-off runbooks: [voip-int.com crawl unblock](processes/voip-int-crawl-unblock.md) with its audit and fix scripts in `tools/`.

Schedules are stored in UTC (12:30, 13:00). They read as 8:30 / 9:00 AM Eastern during daylight time and
7:30 / 8:00 AM after clocks change in November; adjust the cron by one hour then if the earlier time is a problem.
