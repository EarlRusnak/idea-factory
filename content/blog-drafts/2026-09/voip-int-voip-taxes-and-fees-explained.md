---
site: voip-int.com
title: "What Are All Those Fees on Your Business Phone Bill? USF, E911, Regulatory Recovery, and What an Honest Invoice Looks Like"
seo_title: "VoIP Taxes and Fees Explained: USF, E911, Recovery Fees"
meta_description: "The quote said $17 a seat and the invoice said more. Here is what VoIP taxes and fees actually are, line by line: USF, E911, state taxes, recovery fees."
slug: what-are-the-fees-on-your-business-phone-bill-voip-taxes-and-fees-explained
blog: VoIP International Blog Posts
focus_keyword: "VoIP taxes and fees"
secondary_keywords:
  - regulatory recovery fee
  - USF fee on phone bill
  - E911 fee
  - business phone bill explained
  - VoIP surcharges
tags:
  - Small Business Phone
  - Pricing Transparency
  - VoIP Insights
author: Earl Rusnak
target_publish_date: 2026-09-16
word_count: 1999
status: draft
---

## Publishing notes

**Odoo placement**
- Blog: VoIP International Blog Posts (`/blog/voip-international-blog-posts-4/`).
- Slug: `what-are-the-fees-on-your-business-phone-bill-voip-taxes-and-fees-explained`.
- Author: Earl Rusnak. Tags: Small Business Phone, Pricing Transparency, VoIP Insights.
- Publish 2026-09-16. Once live, link to this post from the fee note on /pricing and the fee answer on /faq; the July SEO audit flagged a fee-transparency explainer as the most linkable asset on the site, so it needs inbound links from the money pages.
- The two markdown tables need to be rebuilt as Odoo table blocks; both are small.

**Meta fields**
- SEO title (55 chars): `VoIP Taxes and Fees Explained: USF, E911, Recovery Fees`
- Meta description (152 chars): `The quote said $17 a seat and the invoice said more. Here is what VoIP taxes and fees actually are, line by line: USF, E911, state taxes, recovery fees.`
- Focus keyword: `VoIP taxes and fees` (SEO title, slug, first 100 words, one H2, meta description, body).

**Image alt-text suggestions**
1. Hero: "Sample business phone invoice with the base service charge separated from itemized government taxes and pass-through fees"
2. Mid-post (worked example): "Illustrative ten-seat VoIP International invoice showing $290 base and itemized USF, E911, state tax and FCC cost recovery lines"

**FAQPage JSON-LD** (paste into the post's custom head or Odoo structured-data block; text matches the FAQ section in the body)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Can I avoid USF?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Not legally, if your service carries interstate or international calls. Every interconnected VoIP provider contributes and passes the cost through. You can ask how your provider calculates the interstate portion; the safe-harbor and traffic-study methods can produce different amounts."
      }
    },
    {
      "@type": "Question",
      "name": "Why did my E911 fee change?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Because a state or local government changed it. E911 fees are set by legislatures, utility commissions and county boards, not by providers, and they are revised periodically. If it coincided with a move, the new address may simply carry a different rate."
      }
    },
    {
      "@type": "Question",
      "name": "Is a regulatory recovery fee a tax?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. It is a provider-set fee. It may recover real costs of complying with FCC and state rules, and ours does, but the provider chooses whether to charge it and how much. When comparing providers, treat regulatory recovery as part of the base price."
      }
    },
    {
      "@type": "Question",
      "name": "Are fees different on Pro Mobile or SIP trunking?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, in structure. Pro Mobile lines run on wireless networks and carry the wireless-specific surcharges governments apply to mobile service, so the mix differs from a desk seat. SIP trunking is billed per channel with metered usage, so the taxable base moves with call volume, but the same categories of government pass-throughs apply. In every case they are itemized."
      }
    },
    {
      "@type": "Question",
      "name": "Do you charge for porting?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes: $15 per number, in or out. It is the only one-time charge we bill. Ports typically take 5 to 15 business days per number depending on the losing carrier. There is no activation fee and no per-extension setup fee."
      }
    },
    {
      "@type": "Question",
      "name": "Do fees change if I sign an annual term?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The government taxes and pass-throughs are calculated on your service charges and service address regardless of contract length. An annual term can lower the base rate modestly, and because most pass-throughs are a percentage of that base, those dollar amounts move with it. Our default is month-to-month with 30 days written notice; annual terms are optional."
      }
    }
  ]
}
```

**Internal-link checklist**
- [ ] https://voip-int.com/pricing (twice: "no hidden fees" section and CTA)
- [ ] https://voip-int.com/faq (twice: "no hidden fees" section and CTA)
- [ ] https://voip-int.com/phone-service ("no hidden fees" section)
- [ ] https://voip-int.com/pro-mobile (FAQ)
- [ ] https://voip-int.com/sip-trunking (FAQ)
- [ ] https://voip-int.com/about (FCC regulatory fees section, anchor "licensed telecommunications operator")
- [ ] https://voip-int.com/get-started (CTA)
- [ ] https://voip-int.com/contact (CTA)
- [ ] https://voip-int.com/blog/voip-international-blog-posts-4/cost-benefit-analysis-voip-for-small-businesses-97 (worked example section)
- [ ] https://voip-int.com/blog/voip-international-blog-posts-4/mitel-micloud-connect-and-mivoice-office-250-both-eol-deadlines-have-passed-here-s-where-that-leaves-you-271 (worked example section)
- External (new tab, rel="noopener"): FCC Understanding Your Telephone Bill, FCC Universal Service, USAC.

**Facts for Earl to verify before publish**
1. The illustrative example (10 seats x $29 = $290 base; surcharges roughly $43.50 to $72.50; total roughly $333.50 to $362.50) matches current pass-through math for a typical Florida address and at least one out-of-state address. If real invoices land outside 15 to 25 percent anywhere we serve, change the range here and on the FAQ together.
2. The pricing page still shows $17 per-minute and $29 unlimited at publish, and still uses the quoted line "No activation fee, no per-extension setup fee, and no contract."
3. The FAQ still says "typically 15-25% of the base service fee depending on your service location" and "itemized on every invoice", and still lists "FCC cost recovery, Federal USF, 911, and state & local communications taxes."
4. The native E911 description (registered extension address delivered to the dispatch center) matches how the platform actually routes 911. Adjust if we use a different delivery method.
5. The FCC cost recovery line is described as provider-set and itemized. Confirm that matches the invoice label and that we are comfortable saying so this plainly.
6. The Pro Mobile answer says mobile lines carry wireless-specific surcharges. Confirm against a real Pro Mobile invoice.
7. Porting timeline "5 to 15 business days per number" still matches the FAQ.
8. The secondary keyword "USF fee on phone bill" appears in the body only as the grammatical variant "USF fee on a phone bill". Left that way on purpose; change if Rank Math needs the exact string.

## Post body

# What Are All Those Fees on Your Business Phone Bill? USF, E911, Regulatory Recovery, and What an Honest Invoice Looks Like

The quote said $17 a seat. The invoice said more. If that describes your last phone bill, this is the explanation nobody gave you at signing.

I read a lot of competitor invoices, usually because a prospect forwarded one and asked what they were paying for. The pattern rarely changes: the base rate was accurate, and the rest of the page was never explained. VoIP taxes and fees are real. Most are set by governments, not by your provider. A few are set by the provider and named so they look like the government's idea. Here is what each line is, who sets it, and how to tell an honest invoice from a padded one.

## The three kinds of charges on every phone bill

Any business phone bill explained properly comes down to three buckets.

| Bucket | Who sets the amount | Typical line items | Can a provider waive it? |
|---|---|---|---|
| Government taxes | Federal, state, county, city | State communications services tax, local telecom taxes, sales tax where it applies | No |
| Government-mandated pass-throughs | Government sets the rate or requirement; the provider collects it | Federal USF, E911 or 911 surcharge, state TRS | No, though the amount depends on the provider's calculation |
| Provider-set fees | The provider | Regulatory recovery fee, cost recovery, "administrative" or "network access" fees | Yes. These are business decisions |

The first two appear on every carrier's bill, ours included. The third is where invoices diverge. Most confusion about VoIP taxes and fees comes from treating all three as one thing.

## Federal Universal Service Fund (USF)

Of all the VoIP taxes and fees on a bill, the USF fee on a phone bill is usually the largest single pass-through. It funds four federal programs: connectivity in rural and high-cost areas, Lifeline for low-income households, E-Rate for schools and libraries, and the Rural Health Care program. The FCC oversees the fund and the Universal Service Administrative Company (USAC) collects and disburses it. The FCC's [Universal Service page](https://www.fcc.gov/general/universal-service) and [USAC](https://www.usac.org/) explain the programs in detail.

Carriers contribute a percentage of their interstate and international telecommunications revenue. That percentage is the contribution factor. The FCC resets it every quarter based on projected program demand against projected contributor revenue, and it has run above 30 percent in recent years. When your USF line changes on a January, April, July or October invoice, the factor moved, not your provider's margin.

Two details matter for VoIP. The factor applies only to the interstate and international portion of your charges, not the whole bill, and the provider has to determine what that portion is. The FCC allows two approaches: a safe-harbor percentage it publishes for interconnected VoIP, or a traffic study that measures the provider's actual interstate share. Either way, the USF line should be the factor applied to the interstate portion, not the full base rate. If a provider applies it to 100 percent of the bill, ask why.

## E911 and 911 surcharges

The E911 fee is the cleanest example of a government pass-through. State and local governments set it, usually as a flat monthly amount per line or seat, and it funds public safety answering points, the dispatch centers that answer 911 calls. Because it is set locally, two customers in different counties see different amounts for identical service, and the amount changes when a legislature or county commission votes. The FCC's consumer guide, [Understanding Your Telephone Bill](https://www.fcc.gov/consumers/guides/understanding-your-telephone-bill), covers this line and the other common ones.

We support native E911 on every seat: the address registered to your extension is delivered to the dispatch center when someone dials 911 from that phone, instead of routing through a generic intake center first. That is what the surcharge pays for, which is why we ask you to keep registered addresses current.

## State and local communications taxes and TRS

This bucket is why two businesses on the same plan get different totals. States tax communications services in different ways: a dedicated communications services tax, general sales tax, or gross receipts taxes on the carrier that get passed along. Counties and cities often add their own. The rate is determined by your service address, which is why we ask for it before quoting, and why a company with offices in two states sees two different tax lines on one invoice.

State TRS (Telecommunications Relay Service) surcharges fund relay services for people who are deaf, hard of hearing or speech-disabled. They are typically small per-line charges set by each state.

None of these VoIP surcharges are within a provider's control. Showing them separately, with their real names, so you can match each to the jurisdiction that imposed it, is.

## FCC regulatory fees and cost recovery

The FCC charges licensed carriers annual regulatory fees to fund its operations. We hold our own licenses as a [licensed telecommunications operator](https://voip-int.com/about), so we pay those fees directly and recover them through an itemized FCC cost recovery line.

Here is the honest part. That recovery line is set by us. The FCC does not require us to charge it or tell us how much. It recovers a real compliance cost and we label it as such, but by the classification above it belongs in bucket three, not bucket two. The same goes for any line called "regulatory recovery fee", "compliance fee" or "cost recovery" on any invoice. Those fees are lawful and often legitimate. They are not taxes, and a provider that calls them government-mandated is being imprecise at best.

It gets murkier when a line has no traceable purpose at all. "Administrative fee", "network access fee" and "service assurance fee" are labels I have seen on forwarded invoices that recover nothing in particular. They are price increases with a formal name, and you should count them as base rate when you compare quotes.

## Why "no hidden fees" is not the same as "no fees"

We say no hidden fees. We do not say no fees, and you should be suspicious of any provider who does, because the first two buckets are not optional for anyone.

Here is what our [pricing page](https://voip-int.com/pricing) commits to: "No activation fee, no per-extension setup fee, and no contract." Government surcharges, in the words of our [FAQ](https://voip-int.com/faq), are "itemized on every invoice" and include "FCC cost recovery, Federal USF, 911, and state & local communications taxes." Those VoIP taxes and fees run "typically 15-25% of the base service fee depending on your service location." The one exception to the no-one-time-charges rule is number porting: "$15 per number, in or out", which the pricing page calls "the only one-time charge we bill." Porting your numbers away from any carrier, including us, is your right under FCC rules, and we charge the same $15 in both directions so there is no exit penalty in the fine print.

That is the whole fee story: the base rate on the [phone service page](https://voip-int.com/phone-service) is the base rate, the government lines are labeled by jurisdiction, and porting is the only one-time item.

## How to read your current invoice in five minutes

Pull up your most recent bill. This works on any provider's invoice, and it turns VoIP taxes and fees from a lump sum into a list you can argue with.

1. **Separate base from surcharges.** Add up every recurring line for the service itself: seats, add-ons, minutes, equipment. That is your base.
2. **Compute the percentage.** Add up everything else and divide by the base. Over 30 percent, keep going; something other than government is probably in there.
3. **Find the provider-set fees.** Anything labeled recovery, administrative, compliance, network access or assurance is set by the provider. Add those to the base. That is the real per-seat price.
4. **Check the term.** Look for auto-renewal language, the notice window to cancel, and any early termination fee.
5. **Check the porting language.** Confirm you can port your numbers out, what it costs, and how long it takes.

If the invoice lumps everything into one "Taxes and surcharges" line, that is a finding in itself. Ask for the breakdown. An operator who runs the switch has it.

## What VoIP taxes and fees look like on a VoIP International invoice

An illustrative example, not a quote: a ten-person office on the $29 unlimited US and Canada plan.

| Line | Amount |
|---|---|
| 10 seats, unlimited plan, $29 each | $290.00 |
| Federal USF (applied to the interstate portion) | itemized |
| E911 surcharge (per seat, set by your state or county) | itemized |
| State and local communications taxes and TRS | itemized |
| FCC cost recovery | itemized |
| Government taxes and pass-throughs, combined | roughly $43.50 to $72.50 |
| Estimated monthly total | roughly $333.50 to $362.50 |

The spread depends almost entirely on the service address; the base rate does not move. What you will not see: an activation fee, a per-extension setup fee, or a line with a vague name and no jurisdiction behind it.

For what that total replaces, our [cost-benefit analysis of VoIP for small businesses](https://voip-int.com/blog/voip-international-blog-posts-4/cost-benefit-analysis-voip-for-small-businesses-97) walks through the math against a legacy system. If you are still on a [Mitel platform that has passed end of life](https://voip-int.com/blog/voip-international-blog-posts-4/mitel-micloud-connect-and-mivoice-office-250-both-eol-deadlines-have-passed-here-s-where-that-leaves-you-271), the invoice above is what you would be moving to.

## Frequently asked questions

**Can I avoid USF?**
Not legally, if your service carries interstate or international calls. Every interconnected VoIP provider contributes and passes the cost through. You can ask how your provider calculates the interstate portion; the safe-harbor and traffic-study methods can produce different amounts.

**Why did my E911 fee change?**
Because a state or local government changed it. E911 fees are set by legislatures, utility commissions and county boards, not by providers, and they are revised periodically. If it coincided with a move, the new address may simply carry a different rate.

**Is a regulatory recovery fee a tax?**
No. It is a provider-set fee. It may recover real costs of complying with FCC and state rules, and ours does, but the provider chooses whether to charge it and how much. When comparing providers, treat regulatory recovery as part of the base price.

**Are fees different on Pro Mobile or SIP trunking?**
Yes, in structure. [Pro Mobile](https://voip-int.com/pro-mobile) lines run on wireless networks and carry the wireless-specific surcharges governments apply to mobile service, so the mix differs from a desk seat. [SIP trunking](https://voip-int.com/sip-trunking) is billed per channel with metered usage, so the taxable base moves with call volume, but the same categories of government pass-throughs apply. In every case they are itemized.

**Do you charge for porting?**
Yes: $15 per number, in or out. It is the only one-time charge we bill. Ports typically take 5 to 15 business days per number depending on the losing carrier. There is no activation fee and no per-extension setup fee.

**Do fees change if I sign an annual term?**
The government taxes and pass-throughs are calculated on your service charges and service address regardless of contract length. An annual term can lower the base rate modestly, and because most pass-throughs are a percentage of that base, those dollar amounts move with it. Our default is month-to-month with 30 days written notice; annual terms are optional.

## Want a real number for your locations?

Tell us your crew size, call volume, which platform you use and the service address for each location. We'll walk through what real coverage would look like, what it would replace, and what the VoIP taxes and fees will actually be for your addresses, itemized the same way they will appear on the invoice. Pricing is on the [pricing page](https://voip-int.com/pricing), the fee questions are answered in more depth in the [FAQ](https://voip-int.com/faq), and you can [get started](https://voip-int.com/get-started) or [contact us](https://voip-int.com/contact) whenever you are ready.
