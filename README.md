# L1nq Blog

A Hugo + FixIt cybersecurity blog focused on CTF writeups, pentest labs, code audit notes, and web security research.

Site: [https://sw1mblu3.fun/](https://sw1mblu3.fun/)

## Documentation

- [PROJECT_STATUS.md](PROJECT_STATUS.md) - current project snapshot, completed work, risks, and next steps.
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - finalized phased roadmap for launch validation, UX polish, deployment hygiene, and optional features.
- [CUSTOMIZATION_PLAN.md](CUSTOMIZATION_PLAN.md) - customization roadmap inspired by `exp10it.io`.
- [PHASE1_COMPLETED.md](PHASE1_COMPLETED.md) and [PHASE1.3_COMPLETED.md](PHASE1.3_COMPLETED.md) - historical phase completion notes.
- [LINK_STYLE_OPTIMIZATION.md](LINK_STYLE_OPTIMIZATION.md) - link styling change record.

## Common Commands

```bash
# Preview locally with live reload
hugo server -D

# Build static output (generates public/)
hugo --cleanDestinationDir

# Verify migrated post image references
python check_images.py
```

Hugo `v0.160.1+extended` is available in the current PowerShell environment.

## Branch Structure

| Branch | Purpose |
|--------|---------|
| `source` | Hugo project source (content, themes, config, etc.). This is the **working branch**. |
| `main` | Deployed static site files. Managed automatically by `deploy.sh`. |

`public/` and `resources/` are not tracked in `source` branch (see `.gitignore`).

## Deployment

The `deploy.sh` script builds the Hugo site and pushes the generated `public/` output to the `main` branch, which is served by GitHub Pages.

```bash
# Deploy to GitHub Pages
bash deploy.sh
```

### How it works

1. `hugo --cleanDestinationDir` regenerates `public/` from scratch
2. A temporary git repository is created inside `public/`
3. Contents are force-pushed to the `main` branch of `L1nq0.github.io`
4. GitHub Pages serves the `main` branch at [sw1mblu3.fun](https://sw1mblu3.fun/)

The git repository inside `public/` is disposable — it is created fresh each deployment and destroyed when Hugo rebuilds. This is the standard Hugo deployment pattern for `username.github.io` repositories.

### Daily workflow

```bash
# 1. Ensure you are on source branch
git branch                    # should show * source

# 2. Write or edit posts under content/posts/

# 3. Preview locally
hugo server -D

# 4. Commit source changes
git add content/
git commit -m "Add new post: post-title"

# 5. Deploy site
bash deploy.sh

# 6. Push source branch
git push origin source
```
