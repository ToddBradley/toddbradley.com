# Site Architecture & Memory Jogger

*Target Audience: Todd Bradley (2 years from now)*

This document outlines how `toddbradley.com` works under the hood. It was migrated from WordPress to Jekyll in early 2026 to simplify hosting, improve performance, and reduce maintenance overhead.

## The Core Stack

1. **Jekyll (Static Site Generator)**
   - The site uses the **Chirpy** theme.
   - Content is written in Markdown and lives in `_posts/`.
   - Building the site converts everything to static HTML/CSS/JS.

2. **GitHub (Source Control)**
   - The repository hosts all source files, drafts, and configuration.
   - **Trigger:** Any push to the `main` branch automatically triggers a build.

3. **Cloudflare Pages (Hosting)**
   - Cloudflare Pages is connected to the GitHub repository.
   - When a commit hits `main`, Cloudflare runs `jekyll build` and serves the resulting `_site/` directory globally on its CDN.
   - **Cost:** Free tier.

## Commenting System (Comentario)

Because Jekyll is static, we needed an external system to handle comments. We chose **Comentario** (a modern, open-source fork of Commento). We initially considered using Utterances (which stores comments as GitHub issues), but since that requires every commenter to have a GitHub account, it wasn't a good fit for a general audience blog.

1. **Hosting:** Self-hosted on **Railway** (using their Postgres plugin and Comentario Docker image).
2. **Frontend Integration:** A Javascript snippet is embedded in `_includes/comments.html` to display the widget at the bottom of posts.
3. **Legacy Comments:** Old WordPress comments were exported into YAML files (in `_data/comments/`) and are statically rendered on the pages using Jekyll logic.

## Automation & Notifications

Handling comment notifications requires a somewhat complex setup because **Railway's free/hobby tier strictly blocks outbound SMTP (port 587/465)** to prevent spam. Comentario natively uses SMTP to send moderation alerts, and Railway *can* support this directly, but only if you upgrade to a paid tier. Since we wanted to keep costs at zero, that feature is broken out-of-the-box on our current host.

Here is how we bypassed it:

### 1. New Comment (Pending/Moderation) Alerts
When someone submits a comment, it defaults to a "Pending" state (`is_pending = TRUE` in the DB) awaiting your approval.
- **How it works:** A Python script (`maintenance-scripts/check_pending_comments.py`) runs every hour via a **GitHub Actions Cron Job** (`.github/workflows/check_comments.yml`).
- **The mechanism:** The script connects *directly* to the Railway PostgreSQL database, queries the `cm_comments` table for any comments pending in the last 65 minutes, and uses Google's standard SMTP (via an App Password) to email you.
- **Why:** GitHub Actions does not block outbound SMTP like Railway does.

### 2. General Newsletter & Subscriber Updates
For handling user subscriptions and general site updates, we use **Buttondown**.
- **Integration:** A form is located in the site's footer.
- **Automation:** **Zapier** monitors the site's main RSS feed. When a new blog post goes live, Zapier detects it and triggers Buttondown to email your subscribers.

## Key "Gotchas" to Remember

*   **Railway Port Blocks:** Never try to configure standard SMTP directly inside the Railway Comentario app unless you upgrade to a paid tier that explicitly allows outbound mail.
*   **Comentario RSS Feeds:** Comentario *does* have an RSS feed for comments (`/api/rss/comments?domain=...`), but it **only shows approved comments**. It cannot be used to trigger moderation alerts for pending comments.
*   **Database Schema:** Comentario prefixes its tables with `cm_` (e.g., `cm_comments`). The approval state is stored as a boolean column named `is_pending`, not an integer `state` column.
