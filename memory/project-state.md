---
name: project-state
description: Current development phase, completed and pending tasks
metadata:
  type: project
---

# Project State

**Last updated**: 2026-07-06

## Current Phase

Frontend beautification — replicating exp10it.io design on Hugo + FixIt.

## Completed

- [x] Color system: exp10it.io palette (blue accent #006cac/#8fcef2, navy dark #212737)
- [x] System monospace font throughout
- [x] Link styles: dashed underline
- [x] Code blocks: mac mode, white bg (#ffffff) / dark bg (#1a1d2e)
- [x] Tables: horizontal borders only
- [x] Homepage: clean summary cards, calendar icon + date + description
- [x] Homepage: removed pagination UI, kept 4 posts + "All Posts →"
- [x] Homepage profile block
- [x] Navigation: text-only menu + icon-only Archives
- [x] Single post: back button "← Go back"
- [x] Single post: meta simplified to calendar + date + edit link
- [x] Single post: accent-colored title (1.5rem/1.875rem bold)
- [x] /posts/ section: card-style layout, 6 per page, clean heading
- [x] Footer: hr divider + social icons (GitHub, Email) + copyright
- [x] Global: smooth scroll, selection color, focus-visible ring, inline code bg
- [x] Date format: ISO on homepage, human-readable on single post

## Pending / Known Issues

- [ ] Edit page link has Windows backslash in URL path (%5c)
- [ ] Dark mode code block colors (currently #1a1d2e, exp10it uses #011627 Night Owl)
- [ ] /posts/ pagination style could be simplified to "Prev / N / M / Next"
- [ ] Navigation active state wavy underline (CSS written, not verified)

## Git

- Branch: `source` (work) / `main` (deploy)
- Latest: `8eb98af` — "Fix: unify summary card title font size across homepage and /posts/"

## Next Steps

Wait for user feedback on current state. Possible directions:
- Continue exp10it.io replication (pagination, dark code)
- Improve mobile layout
- Or user's new requirements
