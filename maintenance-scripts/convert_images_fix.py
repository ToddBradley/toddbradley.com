import os
import shutil
from urllib.parse import unquote
from bs4 import BeautifulSoup
from markdownify import markdownify as md

SOURCE_DIR = "toddbradley.com before Wordpress"
DEST_UPLOADS = "uploads"
DEST_POSTS = "_posts"

def clean_html(soup):
    for tag in soup.find_all(['hr', 'style', 'script', 'link']):
        tag.decompose()

def process_file_fixed(filepath, year):
    with open(filepath, 'r', encoding='windows-1252', errors='replace') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    clean_html(soup)

    img_dir = os.path.join(DEST_UPLOADS, str(year))
    os.makedirs(img_dir, exist_ok=True)

    # Find all images and their wrapping links
    for tag in soup.find_all(['img', 'a']):
        attr = 'src' if tag.name == 'img' else 'href'
        val = tag.get(attr)

        if not val or val.startswith('http') or val.startswith('mailto:') or val.startswith('#'):
            continue

        # Exclude typical non-image links for <a>
        if tag.name == 'a' and not val.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            continue

        # Decode the URL (e.g. %20 -> space)
        decoded_val = unquote(val)
        rel_dir = os.path.dirname(filepath)
        abs_src = os.path.normpath(os.path.join(rel_dir, decoded_val))

        if os.path.exists(abs_src):
            filename = os.path.basename(abs_src)
            dest_img_path = os.path.join(img_dir, filename)

            if not os.path.exists(dest_img_path):
                shutil.copy2(abs_src, dest_img_path)

            # Update the HTML tag using the un-encoded name or re-encode it?
            # Jekyll/Markdown works better with spaces encoded or just let Markdownify handle it
            tag[attr] = f"/uploads/{year}/{filename}"

    body = soup.find('body')
    if body:
        h1 = body.find('h1')
        if h1:
            h1.decompose()
        return "".join(str(child) for child in body.contents)
    return ""

def reconvert_post(source_file, output_filename, title, date, categories, year):
    full_path = os.path.join(SOURCE_DIR, source_file)
    if not os.path.exists(full_path):
        return

    print(f"Re-converting: {title}")
    combined_html = process_file_fixed(full_path, year)
    markdown_content = md(combined_html, heading_style="ATX").strip()

    front_matter = f"""---
layout: post
title: "{title}"
date: {date}
categories: {categories}
---

"""
    post_path = os.path.join(DEST_POSTS, str(year), output_filename)

    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + markdown_content)
    print(f"Updated: {post_path}")

reconvert_post("photos/walt_disney_world_2003.htm", "2003-12-01-walt-disney-world.md", "Walt Disney World 2003", "2003-12-01 12:00:00 -0700", "[Travel, Archive]", 2003)
reconvert_post("photos/kitchen/kitchen.html", "2004-05-01-kitchen-remodel.md", "Kitchen Remodel", "2004-05-01 12:00:00 -0700", "[Home, Archive]", 2004)
reconvert_post("photos/europe1985/europe_1985.htm", "1985-06-01-europe-1985.md", "Europe 1985 Trip", "1985-06-01 12:00:00 -0700", "[Travel, Archive]", 1985)
