# AcuMed staging deploy — InstaWP site 2488901 (healing-skin-staging.instawp.site)

Built Sep 12, 2026 from `EarlRusnak/claude-projects` → `acumed-site-rebuild` (theme 0.1.3, 21 block pages, importer + page builder).
Files here:

- `acumed-theme-0.1.3.zip` — the block theme, installs with `wp theme install <url>`
- `acumed-bundle-013.tgz` — theme + `acumed-import.php` + `acumed-pages.php` + `resize-photos.php` + `acumed-pages/<slug>.html` (21 pages)
- `SHA256SUMS`

One change versus the source repo: `acumed-pages.php` lists `iv-therapy` in its `check` table (the page was added Sep 12; the source copy in claude-projects still needs the same one-line edit).

Raw URLs:

    https://raw.githubusercontent.com/EarlRusnak/idea-factory/claude/acumed-staging-deploy-ait48r/deploy/acumed/acumed-theme-0.1.3.zip
    https://raw.githubusercontent.com/EarlRusnak/idea-factory/claude/acumed-staging-deploy-ait48r/deploy/acumed/acumed-bundle-013.tgz

Order of operations. Each block is idempotent and ends with a DONE marker. Site root is
`/web/healing-skin-staging.instawp.site/public_html`. In the InstaWP Web Terminal use absolute paths only (it mangles `$` and `~`).

## 1 — Wipe the Healing Skin content (posts, pages, media, Site Editor templates)

```
cd /web/healing-skin-staging.instawp.site/public_html && wp post list --post_type=post,page,attachment,wp_navigation,wp_template,wp_template_part,wp_block,wp_global_styles --post_status=any --format=ids --posts_per_page=-1 | xargs -r -n 50 wp post delete --force --quiet; echo POSTS-LEFT; wp post list --post_type=any --post_status=any --format=count; echo DONE-1
```

Expected: `POSTS-LEFT`, `0` (or a small number), `DONE-1`. 1–3 minutes.

## 2 — Fetch and unpack the bundle (theme 0.1.3, scripts, page sources)

```
cd /web/healing-skin-staging.instawp.site/public_html && curl -sL https://raw.githubusercontent.com/EarlRusnak/idea-factory/claude/acumed-staging-deploy-ait48r/deploy/acumed/acumed-bundle-013.tgz -o /tmp/acumed-bundle-013.tgz && sha256sum /tmp/acumed-bundle-013.tgz && rm -rf /tmp/ab && mkdir -p /tmp/ab && tar xzf /tmp/acumed-bundle-013.tgz -C /tmp/ab && rm -rf wp-content/themes/acumed && cp -r /tmp/ab/acumed wp-content/themes/acumed && cp /tmp/ab/acumed-import.php /tmp/ab/acumed-pages.php /tmp/ab/resize-photos.php . && rm -rf acumed-pages && cp -r /tmp/ab/acumed-pages . && php -l wp-content/themes/acumed/functions.php && php -l acumed-pages.php && php -l acumed-import.php && echo DONE-2
```

Expected: the sha256 `954b9a1971a4c8289ff35e7cc2c6428266688e0db4a21c70d6e697f16081c7c6`, three `No syntax errors` lines, `DONE-2`.

## 3 — Activate the theme and set site basics

```
cd /web/healing-skin-staging.instawp.site/public_html && wp theme activate acumed && wp option update blogname 'AcuMedGroup Wellness Center' --quiet && wp option update blogdescription 'Acupuncture and Integrative Medicine in Kissimmee, FL' --quiet && wp rewrite structure '/%postname%/' --hard --quiet && curl -sL -o wp-content/themes/acumed/assets/img/acumed-logo-horizontal-800.png https://acumedgroup.com/wp-content/uploads/2023/04/site-logo-highres.png && wp theme list --status=active --field=name && echo DONE-3
```

Expected: `acumed`, `DONE-3`.

## 4 — Import the live posts (105, with featured images)

```
cd /web/healing-skin-staging.instawp.site/public_html && wp eval-file acumed-import.php posts && wp post list --post_type=post --format=count && echo DONE-4
```

Expected: one line per post, `Success: Posts imported: 105`, `105`, `DONE-4`. 5–10 minutes.

## 5 — Build the 21 block pages, copy the 4 legal pages from live, check

```
cd /web/healing-skin-staging.instawp.site/public_html && wp eval-file acumed-pages.php build && wp eval-file acumed-pages.php legal && wp eval-file acumed-pages.php check && echo DONE-5
```

Expected: 21 `created` lines, `Reading settings: front = home #…, posts = blog #…`, `Legal pages: 4`, a check table with no `MISSING`, `DONE-5`.

## 6 — Verify

```
cd /web/healing-skin-staging.instawp.site/public_html && wp theme list --status=active --field=name && wp post list --post_type=page --post_status=publish --format=count && wp post list --post_type=post --format=count && wp option get show_on_front && for p in '' iv-therapy/ contact-us/ conditions/chronic-pain/ faqs/; do curl -s -o /dev/null -w "%{http_code} /$p\n" "https://healing-skin-staging.instawp.site/$p"; done; curl -sI https://healing-skin-staging.instawp.site/glutathione-injections/ | grep -i '^location'; echo DONE-6
```

Expected: `acumed`, `25`, `105`, `page`, five `200` lines, `location: https://healing-skin-staging.instawp.site/what-we-offer/`, `DONE-6`.

Afterwards: review the site, tweak on staging, then migrate to GHL per Step 5 of `STAGING-RUNBOOK.md` (All-in-One WP Migration export → import on u88fdz4e3p.wpdns.site). Live acumedgroup.com is untouched by all of the above.

## Result — deployed Sep 12, 2026 ~21:50 UTC (run from Claude Code cloud via `instawp exec 2488901 --api`)

- Rollback point: InstaWP version **10205** `pre-acumed-2026-09-12` (`instawp versions restore 2488901 10205`).
- Step 1 wipe: 269 items deleted, 0 left. Step 2: bundle sha256 matched, PHP lint clean. Step 3: theme `acumed` 0.1.3 active, title/tagline/permalinks set, logo curled from live.
- Step 4: 105 posts imported, 104 attachments (the NAD+ IV post has no featured image on live either), 0 warnings. Step 5: 21 pages created + 4 legal pages, front = home #460, posts = blog #454, check table complete.
- Step 6: 25 published pages, 105 posts, `show_on_front=page`; all sampled URLs 200; 301 map verified (glutathione → what-we-offer, b-12 → metabolic-support, shop → drrusnakwellness.com, hippa → hipaa).
- Notes for API transport: the shell starts in `/home/wiluwumaba0429/web/healing-skin-staging.instawp.site/public_html` (not `/web/...`), and one command is capped at 300 s, so the post import ran under `nohup` with its log at `/tmp/acumed-import.log`.
- Source follow-up in claude-projects: add `'iv-therapy'` to `$expected` in `acumed-site-rebuild/server/acumed-pages.php` (already done in the bundled copy).
