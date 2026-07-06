# L1nq Blog - Development Guide

## Project Overview

Personal cybersecurity blog built with Hugo + FixIt theme, deployed to GitHub Pages.

- **Site**: https://sw1mblu3.fun/
- **Stack**: Hugo v0.160.1+extended, FixIt v0.4.X
- **Content**: CTF writeups, pentest labs, code audit notes, web security research
- **Repository**: github.com/L1nq0/L1nq0.github.io

## Project Structure

```
.
├── hugo.toml              # Hugo + FixIt configuration
├── content/
│   ├── posts/             # Blog posts (one directory per post, each with index.md)
│   ├── about/             # About page
│   └── links/             # Links page
├── themes/FixIt/          # Theme files (do not edit directly)
├── assets/css/            # Custom CSS overrides (_custom.scss)
├── layouts/               # Template overrides
├── static/                # Static files copied to site root on build
├── images/                # Site-wide images (favicon, avatar, etc.)
├── archetypes/            # Post template
├── deploy.ps1             # PowerShell deployment script
├── deploy.sh              # Bash deployment script
├── check_images.py        # Validate image references in posts
└── public/                # Build output (ignored by git, deployed via script)
```

### Branch Strategy

| Branch | Purpose |
|--------|---------|
| `source` | Working branch: Hugo source files (content, config, themes, etc.) |
| `main` | Deploy branch: static site files. Managed by `deploy.ps1` / `deploy.sh`. GitHub Pages serves this branch at root. |

## Rules

### Language

- Site UI, docs, config, and code comments must be in English
- Existing Chinese article content stays unchanged
- Answer user questions in Chinese

### Network

- `WebFetch` is unavailable — do not use it
- Use `WebSearch` for search queries
- Use `curl -x http://127.0.0.1:7897 -L <URL> -H "User-Agent: Mozilla/5.0"` to fetch web pages
- Proxy port: 7897

### Customization

- Prefer `assets/css/_custom.scss`, `assets/css/_override.scss`, and `layouts/` overrides
- **Never edit files under `themes/FixIt/`** — changes will be lost on theme update

## Common Tasks

### Create a New Post

Posts use **page bundle** format: each post is a directory under `content/posts/` containing `index.md` and any images.

1. Create a directory with a URL-friendly slug (English/pinyin, no spaces or special characters):
   ```
   content/posts/my-new-post-slug/
   ```

2. Create `index.md` with front matter:
   ```yaml
   ---
   title: Your Post Title
   date: 2026-07-05 12:00:00
   tags:
     - CTF
   categories:
     - CTF
   summary: "Brief summary"
   slug: your-post-slug
   draft: false
   author:
     name: L1nq
     link: https://github.com/L1nq0
     email: cryp71csec@gmail.com
     avatar: /1.jpg
   weight: 0
   hiddenFromHomePage: false
   hiddenFromSearch: false
   hiddenFromRelated: false
   ---
   ```

3. Place images in the same directory and reference them by filename only:
   ```markdown
   ![screenshot](image.png)
   ```

Note: Do not use `hugo new` — it fails on paths with Chinese characters or spaces.

### Preview Locally

```powershell
hugo server -D
```

Opens at `http://localhost:1313/` with live reload.

### Verify Images

```powershell
python check_images.py
```

Reports any broken image references in posts.

### Build

```powershell
hugo --cleanDestinationDir
```

Generates `public/` with the full static site.

### Deploy

```powershell
# PowerShell
.\deploy.ps1

# Git Bash
bash deploy.sh
```

The script:
1. Runs `hugo --cleanDestinationDir` to regenerate `public/`
2. Creates a temporary git repository inside `public/`
3. Force-pushes `public/` contents to the `main` branch
4. GitHub Pages serves `main` at sw1mblu3.fun

The git repository inside `public/` is disposable — it is recreated on every deployment and destroyed when Hugo rebuilds.

### Save Source Changes

```powershell
git add content/   # or specific files
git commit -m "Add post: title"
git push origin source
```

## Project Memory

The `memory/` directory stores key project context across sessions. When starting work, read:
- `memory/MEMORY.md` — index of all memory files
- `memory/project-state.md` — current phase, completed/pending tasks
- `memory/design-decisions.md` — design rationale
- `memory/user-prefs.md` — user style preferences and constraints

**After each session**: update `memory/project-state.md` with current status and next steps.

## Troubleshooting

| Problem | Solution |
|---------|---------|
| Hugo date parse error | Ensure date format is `YYYY-MM-DD HH:MM:SS` with zero-padded numbers |
| Image not showing | Run `python check_images.py`, verify image is in same directory as `index.md` |
| Deploy script fails | Check that Hugo builds successfully first with `hugo --cleanDestinationDir` |
| Line ending warnings | Normal on Windows; git will normalize on commit |
