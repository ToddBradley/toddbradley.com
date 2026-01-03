# Master Maintenance Plan for toddbradley.com

## Phase 1: Immediate Site Fixes & Features

- [x] **Sidebar Cleanup:** Fix items appearing as tabs that shouldn't be (remove unsuitable pages or front matter).
- [ ] **Image Links:** Fix broken image links. Change unfixable links to a "bad link" icon.
- [ ] **Comments System:** Implement [Giscus](https://github.com/giscus/giscus) for discussions.
- [ ] **Subscriptions:**
  - [ ] Set up a system for users to subscribe to changes.
  - [ ] Extract old subscribers from `wp_comments.csv` and migrate them.
- [ ] **File Hygiene:**
  - [ ] **Pages Audit:** Review `pages/` directory. Convert appropriate pages to `_posts` and rename/cleanup others.
  - [ ] Investigate suspicious filenames (e.g., ending in spaces or numbers like `4.md`).
  - [x] **Journal Archives:** Investigate `todd-bradley-s-galaxy-journal-archive-` files (e.g., `pages/todd-bradley-s-galaxy-journal-archive-2000-to-2002.md`). Determine if they are duplicate archives and split or delete them as necessary.
  - [ ] Audit unconverted HTML files to ensure no content is lost.
  - [ ] Clean up various partial archives of the WP site to reduce clutter.

## Phase 2: Content Expansion

- [ ] **Legacy Content:** Convert "toddbradley.com before WordPress" content into Jekyll pages (verify existence first).
- [ ] **Migrate Other Sites:** Move other domains hosted by WebHostingHub to Jekyll/static sites:
  - [ ] ascromintended.com
  - [ ] lookslikeimgoingnowhere.com
  - [ ] pookiewookiee.com
  - [ ] broomfieldrestaurantreviews.com
  - [ ] tsao.toddbradley.com (check if obsoleted)
  - [ ] 404notfound (content check)

## Phase 3: Infrastructure & Hosting

- [ ] **DNS Transition:** Switch registrar from WebHostingHub (Tucows reseller) to Cloudflare (recommended) or AWS/Google.
- [ ] **Decommission:** Cancel WebHostingHub service.
