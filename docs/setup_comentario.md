# Comentario Setup via Railway

To self-host Comentario on Railway, follow these steps:

1. **Create a Railway Account:** Go to [railway.app](https://railway.app/) and sign up (or log in).
2. **Deploy the Template:** Railway has a template for Comentario (https://railway.app/template/comentario). **Important:** To get email notifications working, you cannot use the default deployment directly. You must first go to the template's source repository (https://github.com/ThallesP/comentario-on-railway) and **Fork** it to your own GitHub account.
3. **Configure Environment Variables:** In Railway, deploy from your newly forked repository. You will need to modify the `Dockerfile` and `secrets.template.yaml` in your fork to accept SMTP variables. Then, configure these variables in Railway:
   - `BASE_URL`: The URL where your Comentario instance will live (e.g., `https://comments.toddbradley.com`).
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Provisioned automatically by Railway's PostgreSQL plugin.
   - **SMTP Settings:**
     - `SMTP_HOST`: (e.g., `smtp.gmail.com`)
     - `SMTP_PORT`: (usually `587`)
     - `SMTP_USERNAME`: Your full email address.
     - `SMTP_PASSWORD`: Your SMTP password (or Google App Password).
     - `SMTP_FROM_ADDRESS`: (e.g., `todd@toddbradley.com`)4. **Link a Custom Domain (Optional but Recommended):** In the Railway dashboard for your Comentario service, go to "Settings" -> "Environment" -> "Domains" and add a custom domain (like `comments.toddbradley.com`). You will need to add a CNAME record in your Cloudflare DNS settings pointing to the Railway URL.
5. **Initial Setup:** Once deployed, visit your Comentario URL. The first account you create will automatically become the super-administrator.
6. **Register Your Website:** Inside the Comentario admin panel, register your website (`toddbradley.com`).

Once you have your Comentario instance running and have its URL, update the `_includes/comments.html` file to point to your self-hosted instance.

**Update:** The `_includes/comments.html` file has been updated to use the live instance at `https://comentario-production-7369.up.railway.app`.

