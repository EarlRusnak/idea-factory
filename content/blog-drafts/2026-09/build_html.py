#!/usr/bin/env python3
"""Convert each post's markdown body to paste-ready HTML with images and FAQ schema.
Usage: python3 build_html.py [image_url_overrides.json]
Image placeholders: a JSON map {"01-healing-skin-featured": "https://...", ...} overrides local paths."""
import re, json, sys, pathlib, markdown
here = pathlib.Path(__file__).parent
overrides = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
POSTS = {
 "healing-skin-paramedical-tattoo-aftercare-timeline.md": {"featured":"01-healing-skin-featured","inline":"02-healing-skin-timeline",
   "inline_after_h2":"Why Paramedical Tattoo Aftercare Decides Your Final Result",
   "inline_alt":"Paramedical tattoo healing timeline: Day 1 protected, Days 2 to 7 looks too dark, Week 2 flaking and ghosting, Weeks 3 to 6 true color settles. Dry, shaded, hands off.",
   "featured_alt":"Hands applying a thin layer of silicone gel to a healed lower-abdomen scar during paramedical tattoo aftercare"},
 "acumedgroup-first-acupuncture-appointment-kissimmee.md": {"featured":"03-acumed-featured","inline":"04-acumed-checklist",
   "inline_after_h2":"Before Your First Acupuncture Appointment: How to Prepare",
   "inline_alt":"Checklist for your first acupuncture appointment: eat a light meal, go easy on caffeine and skip alcohol, bring your medication list, wear loose clothing, arrive a few minutes early. Se habla español.",
   "featured_alt":"Patient resting comfortably during a first acupuncture appointment at AcuMedGroup in Kissimmee, FL"},
 "drrusnakwellness-post-procedure-skincare-guide.md": {"featured":"05-wellness-featured","inline":"06-wellness-three-steps",
   "inline_after_h2":"A Simple Three-Step Post-Procedure Routine",
   "inline_alt":"Post-procedure skincare in three steps: cleanse without rinsing, comfort and hydrate, protect with mineral SPF. Pause retinol, acids, vitamin C, scrubs and fragrance for now.",
   "featured_alt":"Micellar water, facial oil and mineral sunscreen on a marble shelf, a simple post-procedure skincare routine"},
 "drrusnakacademy-how-to-evaluate-paramedical-tattoo-training-program.md": {"featured":"07-academy-featured","inline":"08-academy-eight-questions",
   "inline_after_h2":"Why the Choice of Paramedical Tattoo Training Program Matters More Than in Cosmetic Tattooing",
   "inline_alt":"Eight questions to ask any paramedical tattoo training program: who teaches, live models, when not to treat, OSHA bloodborne standard, state FDA and HIPAA coverage, what happens after day three, is the business taught, what the credential attests.",
   "featured_alt":"Master trainer supervising a student practicing paramedical tattooing on a live model during Academy training"},
 "voip-int-voip-taxes-and-fees-explained.md": {"featured":"09-voip-featured","inline":"10-voip-bill-buckets",
   "inline_after_h2":"The three kinds of charges on every phone bill",
   "inline_alt":"What is on your business phone bill: government taxes, government pass-throughs such as Federal USF, E911 and state TRS, carrier-level FCC regulatory fee recovery, and provider-set fees. Typically 15 to 25 percent above the base rate depending on location.",
   "featured_alt":"Small-business owner reviewing a monthly phone invoice next to a VoIP desk phone"},
}
def img_url(key):
    return overrides.get(key, f"images/{key}.png")
def split(md_text):
    fm = re.search(r"^---\n(.*?)\n---\n", md_text, re.S).group(1)
    notes = md_text.split("## Publishing notes",1)[1].split("## Post body",1)[0] if "## Publishing notes" in md_text else ""
    body = md_text.split("## Post body",1)[1].strip()
    schema = re.search(r"```json\n(\{.*?\})\n```", notes, re.S)
    return fm, body, (schema.group(1) if schema else None)
for fn, cfg in POSTS.items():
    md_text = (here/fn).read_text()
    fm, body, schema = split(md_text)
    title = re.search(r'^title: "?(.*?)"?$', fm, re.M).group(1)
    # drop the H1 (CMS renders the title) and insert the inline graphic after the chosen H2's first paragraph
    body = re.sub(r"^# .*\n", "", body, count=1).strip()
    marker = "## " + cfg["inline_after_h2"]
    idx = body.find(marker)
    if idx >= 0:
        para_start = body.find("\n", idx) + 2            # first paragraph after that H2
        nxt = body.find("\n\n", para_start)              # end of that paragraph
        fig = f'\n\n<figure class="wp-block-image size-large"><img src="{img_url(cfg["inline"])}" alt="{cfg["inline_alt"]}" loading="lazy" width="1344" height="752"></figure>\n\n'
        body = body[:nxt] + fig + body[nxt:]
    html = markdown.markdown(body, extensions=["tables","attr_list","md_in_html"])
    # tel: links and external links open normally; add rel to external
    out = [f"<!-- {title} -->", f"<!-- Featured image: {img_url(cfg['featured'])} | alt: {cfg['featured_alt']} -->", html]
    if schema:
        out.append('<script type="application/ld+json">\n'+schema+'\n</script>')
    (here/"html"/(fn.replace(".md",".html"))).write_text("\n".join(out)+"\n")
    print(fn, "->", len(html), "chars")
