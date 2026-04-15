import os
import re
import shutil
from bs4 import BeautifulSoup
from markdownify import markdownify as md

SOURCE_DIR = "toddbradley.com before Wordpress"
DEST_UPLOADS = "uploads"
DEST_POSTS = "_posts"

def clean_html(soup):
    for tag in soup.find_all(['hr', 'style', 'script', 'link']):
        tag.decompose()
    for p in soup.find_all('p'):
        if p.text and 'Page 1' in p.text and 'Page 2' in p.text:
            p.decompose()

def process_file(filepath, year):
    with open(filepath, 'r', encoding='windows-1252', errors='replace') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    clean_html(soup)

    img_dir = os.path.join(DEST_UPLOADS, str(year))
    os.makedirs(img_dir, exist_ok=True)

    for img in soup.find_all('img'):
        src = img.get('src')
        if not src or src.startswith('http') or src.startswith('mailto:'):
            continue

        rel_dir = os.path.dirname(filepath)
        abs_src = os.path.normpath(os.path.join(rel_dir, src))

        if os.path.exists(abs_src):
            filename = os.path.basename(abs_src)
            dest_img_path = os.path.join(img_dir, filename)
            if not os.path.exists(dest_img_path):
                shutil.copy2(abs_src, dest_img_path)
            img['src'] = f"/uploads/{year}/{filename}"
        else:
            pass

    body = soup.find('body')
    if body:
        h1 = body.find('h1')
        if h1:
            h1.decompose()
        return "".join(str(child) for child in body.contents)
    return ""

def convert_post(source_files, output_filename, title, date, categories, year):
    print(f"Converting: {title}")
    combined_html = ""
    for f in source_files:
        full_path = os.path.join(SOURCE_DIR, f)
        if os.path.exists(full_path):
            combined_html += process_file(full_path, year) + "\n\n"
        else:
            print(f"Error: Source file not found: {full_path}")
            return

    markdown_content = md(combined_html, heading_style="ATX").strip()

    front_matter = f"""---
layout: post
title: "{title}"
date: {date}
categories: {categories}
---

"""
    post_dir = os.path.join(DEST_POSTS, str(year))
    os.makedirs(post_dir, exist_ok=True)
    post_path = os.path.join(post_dir, output_filename)

    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + markdown_content)
    print(f"Created: {post_path}")

# 6. CD Hunter
convert_post(
    source_files=["cd.hunter.htm"],
    output_filename="2001-01-01-cd-hunter-review.md",
    title="CD Hunter Review",
    date="2001-01-01 12:00:00 -0700",
    categories="[Reviews, Archive]",
    year=2001
)

# 7. Recipes
convert_post(
    source_files=["recipes.htm"],
    output_filename="2002-01-01-favorite-recipes.md",
    title="Favorite Recipes",
    date="2002-01-01 12:00:00 -0700",
    categories="[Food, Archive]",
    year=2002
)

# 8. Europe 1985
convert_post(
    source_files=["photos/europe1985/europe_1985.htm"],
    output_filename="1985-06-01-europe-1985.md",
    title="Europe 1985 Trip",
    date="1985-06-01 12:00:00 -0700",
    categories="[Travel, Archive]",
    year=1985
)

# 9. Kitchen Remodel
convert_post(
    source_files=["photos/kitchen/kitchen.html"],
    output_filename="2004-05-01-kitchen-remodel.md",
    title="Kitchen Remodel",
    date="2004-05-01 12:00:00 -0700",
    categories="[Home, Archive]",
    year=2004
)

# 10. Walt Disney World 2003
convert_post(
    source_files=["photos/walt_disney_world_2003.htm"],
    output_filename="2003-12-01-walt-disney-world.md",
    title="Walt Disney World 2003",
    date="2003-12-01 12:00:00 -0700",
    categories="[Travel, Archive]",
    year=2003
)
