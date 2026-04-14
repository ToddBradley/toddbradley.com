# Project: toddbradley.com (Jekyll Maintenance)

## AI Mandate: Infrastructure & Cost
Before suggesting any new tool, service, or infrastructure change (like hosting, databases, or email):
1. **Explicit Cost Check:** Verify if the service has a "Hobby" or "Free" tier that supports the *specific* features needed (e.g., outbound SMTP).
2. **Platform Limitation Audit:** Search for known "gotchas" or blocks (like Railway's port 587 block) that apply to those specific low-cost tiers.
3. **Integration Pre-flight:** Check if standard configurations (like environment variables) are overridden by specific templates or Dockerfiles.
4. **Present Alternatives:** Always present one "standard" and one "low-friction" alternative with their respective pros/cons regarding cost and complexity.

## Overview
...
- **Status:** Active Maintenance
- **History:** Converted from WordPress to Jekyll (Chirpy Theme) in Jan 2026.
- **Current Task:** General maintenance and improvements.
- **Hosting:** Cloudflare Pages

## Completed Milestones

- Migration from WordPress to Jekyll complete.
- `converter.py` used for content migration.
- `_posts` organized by year.
- `index.html` configured for pagination.
- Cleaned up sidebar pages (tabs).
- Investigated and split 'journal-archive' pages into 52 individual posts.
- Comment strategy implemented with Comentario (hosted on Railway).
- Investigated suspicious filenames (e.g., ' 4.md'); none found, issue resolved.

## Active Tasks

1. Fix remaining broken image links (many "bad-link.svg" placeholders exist).
2. Audit unconverted HTML files.
3. Review `pages/` directory (convert to posts/rename).
4. Resolve remaining ~1300 internal link failures (mostly legacy WordPress pages).



