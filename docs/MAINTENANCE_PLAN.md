# Master Maintenance Plan for toddbradley.com

## Phase 1: Immediate Site Fixes & Features

- [x] **Sidebar Cleanup:** Fix items appearing as tabs that shouldn't be (remove
      unsuitable pages or front matter).
- [x] **Image Links:** Fix broken image links. Change unfixable links to a "bad
      link" icon.
- [x] **Comments System:** Implement [Comentario](https://comentario.app/)
      for discussions (replaces planned Cusdis/Giscus implementations).
  - [x] Set up email notification bypass using GitHub Actions.
  - [ ] Migrate old static YAML comments (`_data/comments/`) into the new Comentario PostgreSQL database.
- [x] **Subscriptions:**
  - [x] Set up a system for users to subscribe to changes.
  - [x] Extract old subscribers from `wp_comments.csv` and migrate them.
- [ ] **File Hygiene:**
  - [x] **Pages Audit:** Review `pages/` directory. Convert appropriate pages
        to `_posts` and rename/cleanup others.
  - [x] **Suspicious Filenames:** Investigated files ending in spaces or numbers.
        None found; issue resolved.
  - [x] **Journal Archives:** Investigate `todd-bradley-s-galaxy-journal-archive-`
        files (e.g., `pages/todd-bradley-s-galaxy-journal-archive-2000-to-2002.md`).
        Determine if they are duplicate archives and split or delete them as
        necessary.
  - [x] **Link Cleanup:** Removed irrelevant links (empty text/URL or linking to `/`) from all posts and pages.
  - [ ] Audit unconverted HTML files to ensure no content is lost.
  - [ ] Clean up various partial archives of the WP site to reduce clutter.

## Phase 2: Content Expansion

- [ ] **Legacy Content:** Convert "toddbradley.com before WordPress" content
      into Jekyll pages (verify existence first).
- [x] **Migrate Other Sites:** Move other domains hosted by WebHostingHub to
      Jekyll/static sites (Cancelled/No longer needed).

## Phase 3: Infrastructure & Hosting

- [x] **DNS Transition:** Switch registrar from WebHostingHub (Tucows reseller)
      to AWS.
- [x] **Decommission:** Cancel WebHostingHub service.
