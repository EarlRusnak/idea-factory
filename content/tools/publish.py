#!/usr/bin/env python3
"""Publish a blog draft (our markdown format) to its CMS as an UNPUBLISHED draft for Earl's review.

    python3 content/tools/publish.py render  <post.md>            # write HTML next to the post (html/), no network
    python3 content/tools/publish.py wordpress <post.md> [--dry-run]
    python3 content/tools/publish.py odoo      <post.md> [--dry-run]
    python3 content/tools/publish.py shopify   <post.md> [--dry-run]   # only if SHOPIFY_ADMIN_TOKEN is set;
                                                                       # otherwise use the Shopify connector in-session

Post front matter must carry: site, title, slug (or handle), seo_title, meta_description, focus_keyword,
tags, author, and optionally categories, excerpt, featured_image, featured_alt, inline_image, inline_alt,
inline_after_h2. Image paths are relative to the post's directory. The body starts after "## Post body".
A ```json FAQPage block inside "## Publishing notes" is appended to the HTML as JSON-LD.

Credentials come from the Claude environment (never from the repo):
  healing-skin.com      HS_WP_USER   HS_WP_APP_PASSWORD
  acumedgroup.com       ACU_WP_USER  ACU_WP_APP_PASSWORD
  drrusnakacademy.com   ACAD_WP_USER ACAD_WP_APP_PASSWORD
  voip-int.com          ODOO_URL (default https://voip-int.com) ODOO_DB (default voipintl19) ODOO_LOGIN ODOO_KEY (ODOO_APIKEY / ODOO_API_KEY also accepted)
  drrusnakwellness.com  SHOPIFY_STORE (xxxx.myshopify.com) SHOPIFY_ADMIN_TOKEN   (optional; connector path preferred)
Every CMS write creates a DRAFT (status draft / is_published False / isPublished false). Nothing goes live from here.
"""
import base64, json, mimetypes, os, re, sys, xmlrpc.client, pathlib
import yaml, requests, markdown

WP_ENV = {
    "healing-skin.com": ("HS_WP_USER", "HS_WP_APP_PASSWORD", "rankmath"),
    "acumedgroup.com": ("ACU_WP_USER", "ACU_WP_APP_PASSWORD", "seopress"),
    "drrusnakacademy.com": ("ACAD_WP_USER", "ACAD_WP_APP_PASSWORD", "generic"),
}

# ---------- parsing and rendering ----------
def load_post(path):
    path = pathlib.Path(path)
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = yaml.safe_load(m.group(1))
    notes = text.split("## Publishing notes", 1)[1].split("## Post body", 1)[0] if "## Publishing notes" in text else ""
    body = text.split("## Post body", 1)[1].strip()
    schema = re.search(r"```json\n(\{.*?\})\n```", notes, re.S)
    fm["_schema"] = schema.group(1) if schema else None
    fm["_dir"] = path.parent
    fm["_body_md"] = body
    return fm

def render_html(fm, image_urls=None):
    """Markdown body -> HTML. image_urls maps local image filename -> hosted URL (for the inline figure)."""
    image_urls = image_urls or {}
    body = re.sub(r"^# .*\n", "", fm["_body_md"], count=1).strip()   # CMS renders the title as H1
    if fm.get("inline_image") and fm.get("inline_after_h2"):
        idx = body.find("## " + fm["inline_after_h2"])
        if idx >= 0:
            para_start = body.find("\n", idx) + 2
            nxt = body.find("\n\n", para_start)
            src = image_urls.get(fm["inline_image"], fm["inline_image"])
            fig = (f'\n\n<figure><img src="{src}" alt="{fm.get("inline_alt","")}" loading="lazy" '
                   f'width="1344" height="752"></figure>\n\n')
            body = body[:nxt] + fig + body[nxt:]
    html = markdown.markdown(body, extensions=["tables", "attr_list", "md_in_html"])
    if fm.get("_schema"):
        html += '\n<script type="application/ld+json">\n' + fm["_schema"] + "\n</script>"
    return html

def slug_of(fm):
    return fm.get("slug") or fm.get("handle")

# ---------- WordPress ----------
def wp_publish(fm, dry_run=False):
    site = fm["site"]
    user_var, pass_var, seo = WP_ENV[site]
    user, pw = os.environ.get(user_var), os.environ.get(pass_var)
    if not (user and pw):
        sys.exit(f"Missing {user_var} / {pass_var} in the environment for {site}.")
    base = f"https://{site}/wp-json"
    auth = (user, pw)
    s = requests.Session(); s.auth = auth; s.headers["User-Agent"] = "rusnak-blog-round/1.0"

    def upload_media(filename, alt):
        p = fm["_dir"] / filename
        if dry_run:
            return {"id": 0, "source_url": f"(dry-run) {p}"}
        r = s.post(f"{base}/wp/v2/media", data=p.read_bytes(),
                   headers={"Content-Disposition": f'attachment; filename="{p.name}"',
                            "Content-Type": mimetypes.guess_type(p.name)[0] or "image/png"})
        r.raise_for_status(); media = r.json()
        s.post(f"{base}/wp/v2/media/{media['id']}", json={"alt_text": alt, "title": alt[:80]})
        return media

    def term_ids(kind, names):
        ids = []
        for name in names or []:
            r = s.get(f"{base}/wp/v2/{kind}", params={"search": name, "per_page": 20}); r.raise_for_status()
            match = next((t for t in r.json() if t["name"].lower() == name.lower()), None)
            if not match and kind == "tags" and not dry_run:
                match = s.post(f"{base}/wp/v2/tags", json={"name": name}).json()
            if match and "id" in match:
                ids.append(match["id"])
            elif kind == "categories":
                print(f"  note: category '{name}' not found on {site}; leaving for Earl")
        return ids

    featured = upload_media(fm["featured_image"], fm.get("featured_alt", "")) if fm.get("featured_image") else None
    inline = upload_media(fm["inline_image"], fm.get("inline_alt", "")) if fm.get("inline_image") else None
    html = render_html(fm, {fm.get("inline_image"): inline["source_url"]} if inline else {})
    meta = {}
    if seo == "rankmath":
        meta = {"rank_math_title": fm["seo_title"], "rank_math_description": fm["meta_description"],
                "rank_math_focus_keyword": fm["focus_keyword"]}
    elif seo == "seopress":
        meta = {"_seopress_titles_title": fm["seo_title"], "_seopress_titles_desc": fm["meta_description"],
                "_seopress_analysis_target_kw": fm["focus_keyword"]}
    payload = {
        "title": fm["title"], "slug": slug_of(fm), "content": html, "status": "draft",
        "excerpt": fm.get("excerpt") or fm["meta_description"],
        "categories": term_ids("categories", fm.get("categories")), "tags": term_ids("tags", fm.get("tags")),
        "meta": meta,
    }
    if featured and featured["id"]:
        payload["featured_media"] = featured["id"]
    if dry_run:
        print(json.dumps({k: (v if k != "content" else f"<{len(v)} chars>") for k, v in payload.items()}, indent=2))
        return
    r = s.post(f"{base}/wp/v2/posts", json=payload); r.raise_for_status(); post = r.json()
    if seo == "rankmath":   # best effort: Rank Math's own endpoint, in case post meta is not REST-registered
        s.post(f"{base}/rankmath/v1/updateMeta", json={"objectID": post["id"], "objectType": "post", "meta": meta})
    print(f"DRAFT created on {site}: id {post['id']} -> {post['link']} (edit: https://{site}/wp-admin/post.php?post={post['id']}&action=edit)")
    return post

# ---------- Odoo (voip-int.com) ----------
def odoo_publish(fm, dry_run=False):
    url = os.environ.get("ODOO_URL", "https://voip-int.com"); db = os.environ.get("ODOO_DB", "voipintl19")
    login = os.environ.get("ODOO_LOGIN", "earl.rusnak@voip-int.com")
    key = os.environ.get("ODOO_KEY") or os.environ.get("ODOO_APIKEY") or os.environ.get("ODOO_API_KEY")
    if not (login and key):
        sys.exit("Missing ODOO_KEY (the same variable the voip-int crawl tools use) in the environment.")
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common"); uid = common.authenticate(db, login, key, {})
    if not uid:
        sys.exit("Odoo authentication failed.")
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    def call(model, method, *args, **kw):
        return models.execute_kw(db, uid, key, model, method, list(args), kw)
    blog_ids = call("blog.blog", "search", [["name", "ilike", "VoIP International"]], limit=1)
    if not blog_ids:
        sys.exit("Blog 'VoIP International Blog Posts' not found.")
    def attach(filename, alt):
        p = fm["_dir"] / filename
        if dry_run:
            return f"(dry-run) {p}"
        att_id = call("ir.attachment", "create", {"name": p.name, "datas": base64.b64encode(p.read_bytes()).decode(),
                                                   "mimetype": "image/png", "public": True, "res_model": "ir.ui.view",
                                                   "description": alt})
        return f"/web/image/{att_id}"
    inline_url = attach(fm["inline_image"], fm.get("inline_alt", "")) if fm.get("inline_image") else None
    cover_url = attach(fm["featured_image"], fm.get("featured_alt", "")) if fm.get("featured_image") else None
    html = render_html(fm, {fm.get("inline_image"): inline_url} if inline_url else {})
    tag_ids = []
    for name in fm.get("tags") or []:
        found = call("blog.tag", "search", [["name", "=", name]], limit=1)
        tag_ids.append(found[0] if found else (0 if dry_run else call("blog.tag", "create", {"name": name})))
    partner = call("res.users", "read", [uid], fields=["partner_id"])[0]["partner_id"][0]
    vals = {"name": fm["title"], "blog_id": blog_ids[0], "content": html, "is_published": False,
            "author_id": partner, "website_meta_title": fm["seo_title"], "website_meta_description": fm["meta_description"],
            "website_meta_keywords": ", ".join([fm["focus_keyword"]] + list(fm.get("secondary_keywords") or [])),
            "tag_ids": [(6, 0, [t for t in tag_ids if t])]}
    if cover_url:
        vals["cover_properties"] = json.dumps({"background-image": f"url('{cover_url}')", "resize_class": "o_record_has_cover o_half_screen_height", "opacity": "0.4"})
    if dry_run:
        print(json.dumps({k: (v if k != "content" else f"<{len(v)} chars>") for k, v in vals.items()}, indent=2)); return
    post_id = call("blog.post", "create", vals)
    print(f"DRAFT created on voip-int.com: blog.post id {post_id} (unpublished). Review in Odoo > Website > Blog.")
    return post_id

# ---------- Shopify (token path; the Shopify connector is the normal path inside a Claude session) ----------
def shopify_publish(fm, dry_run=False):
    store, token = os.environ.get("SHOPIFY_STORE"), os.environ.get("SHOPIFY_ADMIN_TOKEN")
    if not (store and token):
        sys.exit("SHOPIFY_STORE / SHOPIFY_ADMIN_TOKEN not set. Use the Shopify connector in-session instead (fileCreate + articleCreate, isPublished false).")
    gql = f"https://{store}/admin/api/2026-07/graphql.json"
    def run(q, v):
        r = requests.post(gql, json={"query": q, "variables": v}, headers={"X-Shopify-Access-Token": token}); r.raise_for_status(); return r.json()
    print("Shopify token path: not exercised yet; see the connector steps in processes/weekly-blog-round.md.")
    if dry_run: return
    raise SystemExit("Implement after the first token-based run is approved.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, path = sys.argv[1], sys.argv[2]; dry = "--dry-run" in sys.argv
    fm = load_post(path)
    if cmd == "render":
        out = fm["_dir"] / "html" / (pathlib.Path(path).stem + ".html"); out.parent.mkdir(exist_ok=True)
        out.write_text(render_html(fm)); print(out)
    elif cmd == "wordpress": wp_publish(fm, dry)
    elif cmd == "odoo": odoo_publish(fm, dry)
    elif cmd == "shopify": shopify_publish(fm, dry)
    else: sys.exit(__doc__)
