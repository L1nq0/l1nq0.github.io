# L1nq Blog

Hugo + FixIt cybersecurity blog. CTF writeups, pentest labs, code audit, web security research.

Site: [sw1mblu3.fun](https://sw1mblu3.fun/)

## Quick Start

```powershell
# Preview locally
hugo server -D

# Build
hugo --cleanDestinationDir

# Verify images
python check_images.py

# Deploy to GitHub Pages
.\deploy.ps1
```

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `content/posts/` | Blog posts (page bundles: one directory per post) |
| `assets/css/` | Custom styles (`_custom.scss`) |
| `layouts/` | Template overrides |
| `themes/FixIt/` | Theme (do not edit) |
| `public/` | Build output (ignored, deployed by script) |

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `source` | Working branch — all source files live here |
| `main` | Deploy target — only static site files, served by GitHub Pages |

## Deployment

`deploy.ps1` builds the site and pushes `public/` contents to the `main` branch. GitHub Pages serves `main` at sw1mblu3.fun.

For detailed guidance, see [CLAUDE.md](CLAUDE.md).
