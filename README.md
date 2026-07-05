# L1nq Blog

A Hugo + FixIt cybersecurity blog focused on CTF writeups, pentest labs, code audit notes, and web security research.

## Documentation

- [PROJECT_STATUS.md](PROJECT_STATUS.md) - current project snapshot, completed work, risks, and next steps.
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - finalized phased roadmap for launch validation, UX polish, deployment hygiene, and optional features.
- [CUSTOMIZATION_PLAN.md](CUSTOMIZATION_PLAN.md) - customization roadmap inspired by `exp10it.io`.
- [PHASE1_COMPLETED.md](PHASE1_COMPLETED.md) and [PHASE1.3_COMPLETED.md](PHASE1.3_COMPLETED.md) - historical phase completion notes.
- [LINK_STYLE_OPTIMIZATION.md](LINK_STYLE_OPTIMIZATION.md) - link styling change record.

## Common Commands

```bash
# Verify migrated post image references
python check_images.py

# Preview locally, if Hugo is available in PATH
hugo server -D

# Build static output and remove stale generated pages
hugo --cleanDestinationDir
```

Current note: `hugo` is available in the current PowerShell environment. Clean build verified on 2026-05-02 with Hugo `v0.160.1+extended`.

## Deployment Policy

`public/` is currently treated as the deployable static output and should be committed when publishing the site. `resources/` is Hugo's generated cache and is ignored.

Current active roadmap: run Phase 1 launch validation, Phase 3 deployment/repository hygiene, and Phase 4 low-risk optional features. Phase 2 visual polish is intentionally skipped for now.
