#!/usr/bin/env python3
"""
send_buttondown_email.py

Sends an email broadcast via Buttondown's API when a new Jekyll post is published.
Strips YAML frontmatter, resolves relative image and post URLs, and triggers the email.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import yaml

SITE_URL = "https://toddbradley.com"
BUTTONDOWN_API_URL = "https://api.buttondown.com/v1/emails"


def get_git_added_posts(commit_range=None):
    """
    Finds newly added post files in _posts/ using git diff --diff-filter=A.
    """
    if commit_range:
        cmd = ["git", "diff", "--diff-filter=A", "--name-only", commit_range, "--", "_posts/**/*.md"]
    else:
        # Default to the most recent commit
        cmd = ["git", "diff", "--diff-filter=A", "--name-only", "HEAD~1", "HEAD", "--", "_posts/**/*.md"]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        return files
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e.stderr}", file=sys.stderr)
        return []


def clean_markdown(body):
    """
    Cleans markdown for email delivery:
    - Resolves Jekyll liquid tags: {{ '/path' | relative_url }} -> /path
    - Resolves Jekyll liquid tags: {{ '/path' | absolute_url }} -> https://toddbradley.com/path
    - Transforms relative image URLs to absolute URLs
    - Transforms relative links to absolute URLs
    """
    # Resolve Jekyll relative_url and absolute_url liquid tags
    body = re.sub(r"{{\s*['\"](.*?)['\"]\s*\|\s*relative_url\s*}}", r"\1", body)
    body = re.sub(r"{{\s*['\"](.*?)['\"]\s*\|\s*absolute_url\s*}}", rf"{SITE_URL}\1", body)

    # Fix relative image URLs: ![alt](path) or ![alt](/path)
    def fix_img(m):
        alt = m.group(1)
        raw_url = m.group(2).strip()
        is_bracketed = raw_url.startswith("<") and raw_url.endswith(">")
        url = raw_url.strip("<>")
        if not re.match(r"^(https?://|data:)", url):
            url = f"{SITE_URL}/" + url.lstrip("/")
        return f"![{alt}]({f'<{url}>' if is_bracketed else url})"

    body = re.sub(r"!\[([^\]]*)\]\((<[^>]+>|[^()\s]+(?:\([^()\s]*\)[^()\s]*)*)\)", fix_img, body)

    # Fix relative links: [text](path) or [text](/path)
    def fix_link(m):
        text = m.group(1)
        raw_url = m.group(2).strip()
        is_bracketed = raw_url.startswith("<") and raw_url.endswith(">")
        url = raw_url.strip("<>")
        if not re.match(r"^(https?://|mailto:|#)", url):
            url = f"{SITE_URL}/" + url.lstrip("/")
        return f"[{text}]({f'<{url}>' if is_bracketed else url})"

    body = re.sub(r"(?<!!)\[([^\]]+)\]\((<[^>]+>|[^()\s]+(?:\([^()\s]*\)[^()\s]*)*)\)", fix_link, body)

    return body


def parse_post(file_path):
    """
    Parses frontmatter and body from a Jekyll markdown post file.
    Returns (frontmatter_dict, body_markdown, slug, post_url).
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Post file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {file_path}")

    frontmatter_str, raw_body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_str) or {}

    # Check if post is marked as draft/unpublished
    if frontmatter.get("published") is False:
        return None, None, None, None

    # Derive slug
    slug = frontmatter.get("slug")
    if not slug:
        base = os.path.basename(file_path)
        if base.endswith(".md"):
            base = base[:-3]
        slug_match = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", base)
        slug = slug_match.group(1) if slug_match else base

    # Construct post URL
    post_url = frontmatter.get("permalink")
    if not post_url:
        post_url = f"{SITE_URL}/posts/{slug}/"
    elif not post_url.startswith("http"):
        post_url = f"{SITE_URL}/" + post_url.lstrip("/")

    # Clean body markdown
    body = clean_markdown(raw_body.strip())

    # Append footer link to the web version
    footer = f"\n\n---\n*Read this post on the web: [{post_url}]({post_url})*"
    body += footer

    return frontmatter, body, slug, post_url


def send_to_buttondown(api_key, subject, body, canonical_url, status="about_to_send", dry_run=False):
    """
    Sends the post to Buttondown API.
    """
    payload = {
        "subject": subject,
        "body": body,
        "canonical_url": canonical_url,
        "status": status,
    }

    if dry_run:
        print("\n--- [DRY RUN] Payload to Buttondown ---")
        print(f"URL: {BUTTONDOWN_API_URL}")
        print(f"Status: {status}")
        print(f"Subject: {subject}")
        print(f"Canonical URL: {canonical_url}")
        print(f"Body length: {len(body)} characters")
        print("Body preview (first 300 chars):")
        print(body[:300] + ("..." if len(body) > 300 else ""))
        print("--- [END DRY RUN] ---\n")
        return {"dry_run": True}

    if not api_key:
        raise ValueError("BUTTONDOWN_API_KEY environment variable is not set. Cannot send email.")

    req = urllib.request.Request(
        BUTTONDOWN_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json",
            "X-Buttondown-Live-Dangerously": "true",
            "User-Agent": "ToddBradley-Blog-Publisher/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Successfully sent to Buttondown! ID: {data.get('id')}, Status: {data.get('status')}")
            return data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Buttondown API error ({e.code}): {error_body}", file=sys.stderr)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Send newly published Jekyll post to Buttondown subscribers via API."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific post file(s) to send (e.g. _posts/2026/2026-07-17-passwords.md)",
    )
    parser.add_argument(
        "--commit-range",
        help="Git commit range (e.g. 'HEAD~1..HEAD' or '<before>..<after>') to detect added posts",
    )
    parser.add_argument(
        "--status",
        choices=["about_to_send", "draft"],
        default=os.environ.get("BUTTONDOWN_EMAIL_STATUS", "about_to_send"),
        help="Email status in Buttondown (default: about_to_send)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print payload without making API requests to Buttondown",
    )

    args = parser.parse_args()

    files = args.files
    if not files:
        files = get_git_added_posts(args.commit_range)

    if not files:
        print("No newly added posts found. Nothing to send.")
        return

    api_key = os.environ.get("BUTTONDOWN_API_KEY")
    if not api_key and not args.dry_run:
        print(
            "ERROR: BUTTONDOWN_API_KEY environment variable is not set. Please set it in GitHub Secrets.",
            file=sys.stderr,
        )
        sys.exit(1)

    for file_path in files:
        print(f"Processing: {file_path}")
        try:
            frontmatter, body, slug, post_url = parse_post(file_path)
            if frontmatter is None:
                print(f"Skipping unpublished/draft post: {file_path}")
                continue

            subject = frontmatter.get("title")
            if not subject:
                subject = slug.replace("-", " ").title()

            send_to_buttondown(
                api_key=api_key,
                subject=subject,
                body=body,
                canonical_url=post_url,
                status=args.status,
                dry_run=args.dry_run,
            )
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
