import os
import re
import shutil
from bs4 import BeautifulSoup
from markdownify import markdownify as md

SOURCE_DIR = "toddbradley.com before Wordpress"
DEST_UPLOADS = "uploads"
DEST_POSTS = "_posts"

def clean_html(soup):
    # Remove navigation links and styles
    for tag in soup.find_all(['hr', 'style', 'script', 'link']):
        tag.decompose()

    # Remove page navigation links (e.g., "Page 1 Page 2")
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

    # Handle images
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src or src.startswith('http') or src.startswith('mailto:'):
            continue

        rel_dir = os.path.dirname(filepath)
        abs_src = os.path.normpath(os.path.join(rel_dir, src))

        if os.path.exists(abs_src):
            filename = os.path.basename(abs_src)
            # Ensure unique filename if collision happens? Usually ok.
            dest_img_path = os.path.join(img_dir, filename)
            # Copy file (read-only from source)
            if not os.path.exists(dest_img_path):
                shutil.copy2(abs_src, dest_img_path)

            # Update src in HTML
            img['src'] = f"/uploads/{year}/{filename}"
        else:
            print(f"Warning: Image not found: {abs_src}")

    # Extract body content
    body = soup.find('body')
    if body:
        # Remove h1 if it matches the title (we'll add it in front matter)
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

    # Convert to Markdown
    markdown_content = md(combined_html, heading_style="ATX").strip()

    # Front matter
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

# 1. October 2001 Vacation
convert_post(
    source_files=[f"oct2001/oct2001_page{i}.htm" for i in range(1, 7)],
    output_filename="2001-10-11-october-2001-vacation.md",
    title="October 2001 Vacation",
    date="2001-10-11 12:00:00 -0600",
    categories="[Travel, Archive]",
    year=2001
)

# 2. San Juan River Trip
convert_post(
    source_files=["sanjuan.htm"],
    output_filename="2003-05-31-san-juan-river-trip.md",
    title="My San Juan River Trip, May 2003",
    date="2003-05-31 12:00:00 -0600",
    categories="[Travel, Archive]",
    year=2003
)

# 3. SUV Backlash
convert_post(
    source_files=["suvbacklash.htm"],
    output_filename="2002-10-02-my-suv-backlash.md",
    title="My SUV Backlash",
    date="2002-10-02 12:00:00 -0600",
    categories="[Vehicles, Archive]",
    year=2002
)

# 4. Reunion 2005
convert_post(
    source_files=["reunion2005.htm"],
    output_filename="2005-08-01-reunion-2005.md",
    title="Reunion 2005",
    date="2005-08-01 12:00:00 -0600",
    categories="[Family, Archive]",
    year=2005
)

# 5. Thanksgiving 2004
convert_post(
    source_files=["thanksgiving2004.htm"],
    output_filename="2004-11-25-thanksgiving-2004.md",
    title="Thanksgiving 2004",
    date="2004-11-25 12:00:00 -0700",
    categories="[Family, Archive]",
    year=2004
)
