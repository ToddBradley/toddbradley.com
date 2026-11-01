# toddbradley.com

Todd Bradley's personal blog ("Todd Bradley's Galaxy"). Jekyll 4 + Chirpy theme, migrated from WordPress in Jan 2026. Hosted on Cloudflare Pages, which builds and deploys on every push to `main`. A push to `main` that touches `_posts/**` also emails the post to newsletter subscribers (see below), so treat pushes as publishing.

Fuller background lives in `docs/architecture.md` (how the pieces fit together) and `docs/conversion-history.md` (WordPress migration notes, historical only).

## Commands

- Build: `bundle exec jekyll build`
- Serve locally: `bundle exec jekyll serve`
- Lint/format (runs on commit): `pre-commit run --all-files` (prettier + markdownlint on Markdown, see `.markdownlint.yaml`)
- Python deps for scripts: `requirements.txt`, local venv in `venv/`

## Layout

- `_posts/<year>/YYYY-MM-DD-slug.md` — posts. Front matter: `layout: post`, `title`, `date` (with `-0600`/`-0700` offset), `categories: [A, B]`, optional `tags`, `author: Todd`. Permalinks are `/posts/:slug/`.
- `uploads/<year>/` — post images, referenced as `/uploads/<year>/file.png`.
- `_tabs/` — sidebar pages (about, categories, contact, tags, wishlist).
- `_layouts/post.html`, `_includes/` — overrides of Chirpy theme files (comments widget, footer with Buttondown form, trending tags).
- `docs/` — internal docs, excluded from the build. Anything new at the repo root that shouldn't be public needs adding to `exclude` in `_config.yml`.
- `bit-rot.md` — placeholder page that unrecoverable legacy images/links point to.
- `maintenance-scripts/` — the two Python scripts the GitHub Actions workflows run: `send_buttondown_email.py` and `check_pending_comments.py`. The one-off WordPress conversion scripts were deleted in Nov 2026 (recoverable from git history). `maintenance-scripts/backups/` is gitignored and holds local Comentario data exports.
- `_site/`, `.jekyll-cache/` — build output, gitignored.

## External services

- **Comments:** self-hosted Comentario on Railway (free tier), embedded via `_includes/comments.html`. Railway blocks outbound SMTP, so `.github/workflows/check_comments.yml` runs hourly, queries the Comentario Postgres DB (`cm_comments.is_pending`) and emails Todd via Gmail SMTP.
- **Newsletter:** Buttondown. `.github/workflows/notify_buttondown.yml` runs on pushes touching `_posts/**`, detects newly added posts in the commit range and sends them via the Buttondown API. Can be run manually with a specific post, `draft` status or dry run. This replaced Zapier in Sept 2026.
- Secrets: GitHub repo secrets for the workflows; local `.env` (gitignored) for running scripts locally. Never print or commit `.env` contents.

## Infrastructure and cost rule

Todd wants this site to stay free or close to it. Before suggesting any new tool, service or infrastructure change:

1. Check the free/hobby tier actually supports the specific features needed (e.g. outbound SMTP).
2. Look for known gotchas on those tiers (like Railway's SMTP port block).
3. Check whether templates or Dockerfiles override standard config.
4. Present one "standard" and one "low-friction" option with cost and complexity tradeoffs.
