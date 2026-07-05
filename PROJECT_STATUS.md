# Project Status

Last updated: 2026-05-02

## Purpose

This repository is a Hugo + FixIt personal cybersecurity blog for CTF writeups, pentest lab notes, code auditing, and web security research. The migration target is a clean, minimalist reading experience inspired by `exp10it.io`, while keeping FixIt's richer blog features available when needed.

## Working Rules

- Default language for site UI/docs/config comments is English unless the user explicitly asks for Chinese.
- Existing Chinese article content should stay unchanged.
- Avoid `WebFetch`; use built-in web search or `curl -x http://127.0.0.1:7897 -L <URL> -H "User-Agent: Mozilla/5.0"` when page content must be fetched.
- Prefer customizing site-level files such as `assets/css/_custom.scss`, `assets/css/_override.scss`, and `layouts/` overrides instead of editing theme files under `themes/FixIt`.

## Current Snapshot

- Framework: Hugo with FixIt theme.
- Site title: `L1nq Blog`.
- Base URL: `https://sw1mblu3.fun/`.
- Theme: `FixIt`.
- Default language: English.
- Default color mode: light.
- Content: 31 migrated posts in `content/posts`.
- Images: 1,308 post images.
- Image reference check: `python check_images.py` passed with 0 issues on 2026-05-02.
- Build check: `hugo --cleanDestinationDir` passed on 2026-05-02 with Hugo `v0.160.1+extended`.
- Cleanup check: removed stale root SEO files, temp Claude working files, old favicon duplicates, `.hugo_build.lock`, and the old `hugo.toml` backup on 2026-05-01.
- SEO/search check: Fuse search is enabled, `public/search.json` is generated, Open Graph/Twitter image metadata uses `/1.jpg`, and article author/publisher metadata is populated.
- Content restore check: post bundles were restored from the original Hexo source after metadata updates, then image paths and shortcode-like payload text were re-applied safely with UTF-8.
- Ignore rules: `.gitignore` now excludes Hugo lock files and Claude temporary working files.
- Deploy artifact policy: `public/` is intentionally kept as the deployable static output; Hugo `resources/` cache is ignored.
- Phase 2 visual polish is skipped by current decision. Phase 1, Phase 3, and Phase 4 are the active workstreams.
- Main styling file: `assets/css/_custom.scss`.
- Main config file: `hugo.toml`.

## Completed Work

- Migrated Hexo posts into Hugo page bundles under `content/posts/<slug>/index.md`.
- Copied post-local images into each page bundle.
- Converted front matter for Hugo/FixIt fields such as `slug`, `draft`, `comment`, and hidden flags.
- Created About page at `content/about/index.md`.
- Created Links page at `content/links/index.md`.
- Configured main navigation: Categories, Tags, Links, About, and icon-only Archives.
- Enabled profile-style home page with avatar, title, subtitle, and social links.
- Set home pagination to 4 posts per page.
- Added minimalist post list styling, hidden featured previews, and dashed link hover behavior.
- Removed visible Hugo/FixIt powered footer branding through config.
- Enabled archives pagination and tag cloud.
- Added favicon assets under `static/`.
- Set GitHub social icon to `fa-brands fa-github` and added CSS to force transparent background.
- Enabled Fuse search in the header for desktop and mobile.
- Filled site SEO image, thumbnail, page SEO image, publisher, and app title metadata.
- Removed `content/posts_backup_20260428_111421` from the content tree so backup pages no longer appear in the sitemap or search index.

## Current Feature State

- Fuse search is enabled: `[params.search].enable = true`.
- `public/search.json` is generated with 263 index entries after removing backup content from the source tree.
- TOC is enabled for posts.
- KaTeX math support is enabled.
- Code highlighting is configured through Hugo/FixIt settings.
- Social sharing is enabled for Twitter, Facebook, and Weibo.
- Comments are disabled.
- Analytics are disabled.
- Reading progress bar is enabled as the only active Phase 4 feature.
- PWA is disabled.
- Related posts are disabled.

## Known Risks

- Generated `public/robots.txt` and `public/sitemap.xml` use `https://sw1mblu3.fun/` after the 2026-05-02 build. Stale root-level `robots.txt` and `sitemap.xml` were removed.
- `content/posts_backup_20260428_111421` was removed because Hugo treated it as publishable content and included it in `sitemap.xml`.
- Generated `public/` output is intentionally visible because it is the current deploy artifact. `resources/` is ignored as a Hugo cache directory.
- The git branch is ahead 2 and behind 4 relative to `origin/main`; sync strategy should be decided before release work.
- Some generated/public files are dirty. Treat them as generated artifacts unless the deploy workflow intentionally commits `public/`.

## Recommended Next Steps

See `DEVELOPMENT_PLAN.md` for the finalized phased roadmap.

1. Execute Phase 1 launch validation: browser-level search smoke test, responsive page checks, favicon/social preview checks, RSS/sitemap/robots verification.
2. Keep `public/` committed for the current deployment workflow; revisit only if CI-based builds are introduced.
3. Skip Phase 2 visual/readability polish for now.
4. Keep comments, analytics, related posts, and PWA disabled until there is a concrete need and configuration target.

## Useful Commands

```bash
python check_images.py
hugo server -D
hugo
```

If network access is needed:

```bash
curl -x http://127.0.0.1:7897 -L <URL> -H "User-Agent: Mozilla/5.0"
```
