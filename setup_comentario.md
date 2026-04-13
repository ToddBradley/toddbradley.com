# Comentario Setup via Railway

To self-host Comentario on Railway, follow these steps:

1. **Create a Railway Account:** Go to [railway.app](https://railway.app/) and sign up (or log in).
2. **Deploy the Template:** Railway has a 1-click template for Comentario. You can find it by searching their template gallery or using this link: https://railway.app/template/comentario
3. **Configure Environment Variables:** During the deployment process, Railway will ask you to fill in some environment variables. The most critical ones are:
   - `BASE_URL`: The URL where your Comentario instance will live (e.g., `https://comments.toddbradley.com`). Railway will provide a temporary URL, but you can configure a custom domain later.
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Railway's template should automatically provision a PostgreSQL database and fill these in for you.
   - **SMTP Settings:** To get email notifications working (which is why we started this!), you *must* configure these:
     - `SMTP_HOST`: (e.g., `smtp.mailgun.org` or your provider)
     - `SMTP_PORT`: (usually 587)
     - `SMTP_USERNAME`: Your SMTP username.
     - `SMTP_PASSWORD`: Your SMTP password.
     - `SMTP_FROM_ADDRESS`: (e.g., `comments@toddbradley.com`)
4. **Link a Custom Domain (Optional but Recommended):** In the Railway dashboard for your Comentario service, go to "Settings" -> "Environment" -> "Domains" and add a custom domain (like `comments.toddbradley.com`). You will need to add a CNAME record in your Cloudflare DNS settings pointing to the Railway URL.
5. **Initial Setup:** Once deployed, visit your Comentario URL. The first account you create will automatically become the super-administrator.
6. **Register Your Website:** Inside the Comentario admin panel, register your website (`toddbradley.com`).

Once you have your Comentario instance running and have its URL, update the `_includes/comments.html` file to point to your self-hosted instance.

**Update:** The `_includes/comments.html` file has been updated to use the live instance at `https://comentario-production-7369.up.railway.app`.

