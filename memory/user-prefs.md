---
name: user-prefs
description: User style preferences, constraints, and feedback patterns
metadata:
  type: user
---

# User Preferences

## Rules (from CLAUDE.md + conversation)

- ⛔ **Never commit or push without explicit permission** — user was very clear about this
- ⛔ **Never edit files under `themes/FixIt/`**
- ✅ Build only to verify (`hugo --cleanDestinationDir`), preview with `hugo server`
- ✅ Answer in Chinese
- ✅ Ask before making multi-file or irreversible changes

## Design Preferences

- **Minimal changes**: Prefer surgical edits over large rewrites. One-step-at-a-time.
- **Don't add unrequested things**: Example — user wanted pagination removed but did NOT want "Recent Posts" heading added.
- **Don't change what works**: Keep post count (4 on home), TOC sidebar, etc. unless specifically asked.
- **Verify before claiming fixed**: If user says "I don't see changes", check CSS specificity, cache, and actual rendered output.
- **exp10it.io is reference, not exact copy**: Adapt what makes sense, skip what doesn't (e.g., tables, TOC).

## Communication Style

- Present analysis before plan, plan before code
- When user says "不对" (wrong), revert first, then discuss what went wrong
- Keep summaries brief — user prefers action over explanation

## Known Pitfalls

- CSS specificity: FixIt has `.home.posts .summary .single-title` that overrides generic `.summary .single-title`. Always check compiled CSS.
- Windows paths: Backslashes in `.File.Path` cause `%5c` in URLs. Need `strings.Replace` or `replace` in templates.
- Hugo server caches aggressively — need `--noHTTPCache` or different port for fresh preview.
- SCSS merging: Hugo/SCSS may merge duplicate selectors unexpectedly. Verify compiled output.

## Feedback History

- 2026-07-06: User rejected "Recent Posts" heading + 5-post change + date format change. Said changes were wrong. Rolled back.
- 2026-07-06: User wants each step validated individually rather than bundled changes.
