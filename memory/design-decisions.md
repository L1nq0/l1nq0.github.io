---
name: design-decisions
description: Key design decisions and rationale during frontend beautification
metadata:
  type: project
---

# Design Decisions

## Color System

**Decision**: Adopt exp10it.io's blue accent palette instead of original black.
**Why**: exp10it.io uses blue (#006cac light / #8fcef2 dark) as accent for links and headings. Black accent looked too plain.
**When**: 2026-07-06, commit `e0944a6`.

## Tables: Horizontal Borders Only

**Decision**: Keep horizontal borders only, NOT exp10it.io's all-sides bordered tables.
**Why**: Horizontal-only is cleaner and matches prose reading flow. exp10it.io's all-border style looks like spreadsheet.
**When**: 2026-07-05, commit `e6c096b`.

## TOC: Keep FixIt Sidebar

**Decision**: Keep FixIt's sidebar TOC, NOT replicate exp10it.io's inline `<details>` TOC.
**Why**: Sidebar TOC stays visible while scrolling. exp10it.io's inline collapsible TOC requires clicking to expand and disappears when scrolling past it.
**When**: 2026-07-06.

## Date Format: Mixed

**Decision**: ISO format (2006-01-02) for homepage/post cards, human-readable (2 Jan, 2006) for single post meta.
**Why**: Homepage benefits from compact ISO dates. Single post meta reads better with "5 Jul, 2026" matching exp10it.io.
**When**: 2026-07-06.

## Homepage: Remove Pagination, Keep Post Count

**Decision**: Remove pagination UI (1,2,3,…,8) from homepage but keep the 4-post limit (from `paginate = 4`). Add "All Posts →" link.
**Why**: exp10it.io has no pagination on homepage. Users browse recent posts and go to /posts/ for full listing.
**User constraint**: Do NOT change post count (4), do NOT add "Recent Posts" heading.
**When**: 2026-07-06, commit `a7b088b`.

## /posts/ Section: Card Layout Instead of Archive

**Decision**: Override FixIt's default section template (year-grouped archive list) with card-style layout using `summary.html`.
**Why**: exp10it.io's /posts/ page uses same card style as homepage, not an archive view. Better browsing experience.
**When**: 2026-07-06, commit `72a6e03`.

## Single Post Meta: Minimal

**Decision**: Reduce meta from 2 lines (author+category+date+lastmod+wordcount+readingtime) to 1 line (calendar+date+edit link).
**Why**: Matches exp10it.io's clean meta. Removes noisy information (visitor counts, comment counts never used since comments disabled).
**When**: 2026-07-06, commit `a7b088b`.

## Never Edit themes/FixIt/

**Decision**: All customization through `assets/css/_custom.scss` and `layouts/` overrides.
**Why**: Theme updates would overwrite edits. This is FixIt's documented customization approach.
**When**: From project start.

## No Unsolicited Git Operations

**Decision**: Never commit or push without explicit user permission.
**Why**: User requirement. They want to control when changes are saved to git.
**When**: Established early in development.
