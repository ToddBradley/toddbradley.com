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

    body = soup.find('body')
    if body:
        h1 = body.find('h1')
        if h1:
            h1.decompose()
        return "".join(str(child) for child in body.contents)
    return ""

def convert_post(source_file, output_filename, title, date, categories, year):
    full_path = os.path.join(SOURCE_DIR, source_file)
    if not os.path.exists(full_path):
        return

    print(f"Converting: {title}")
    combined_html = process_file(full_path, year)
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

# Remaining single pages
pages_to_convert = [
    ("tfcguide.htm", "2000-01-01-tfc-guide.md", "Team Fortress Classic Guide", "2000-01-01 12:00:00 -0700", "[Gaming, Archive]", 2000),
    ("history.htm", "2000-01-01-my-history.md", "My History", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    ("books.htm", "2000-01-01-books-i-recommend.md", "Books I Recommend", "2000-01-01 12:00:00 -0700", "[Books, Archive]", 2000),
    ("games.htm", "2000-01-01-games-i-play.md", "Games I Play", "2000-01-01 12:00:00 -0700", "[Gaming, Archive]", 2000),
    ("thingsido.htm", "2000-01-01-things-i-do.md", "Things I Do", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    ("contact_info.htm", "2000-01-01-contact-info.md", "Contact Info", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    ("forsale.htm", "2000-01-01-for-sale.md", "Stuff For Sale", "2000-01-01 12:00:00 -0700", "[Archive]", 2000),
    ("wishlist.htm", "2000-01-01-my-wishlist.md", "My Wishlist", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    ("bethbigfoot.htm", "2002-09-22-beth-bigfoot.md", "Beth is Bigfoot?", "2002-09-22 12:00:00 -0700", "[Archive]", 2002),
    ("squish.htm", "2000-01-01-squish.md", "Squish", "2000-01-01 12:00:00 -0700", "[Archive]", 2000),
    ("wireless.htm", "2000-01-01-wireless.md", "Wireless Internet", "2000-01-01 12:00:00 -0700", "[Tech, Archive]", 2000),
    ("wedding.htm", "2002-08-01-our-wedding.md", "Our Wedding", "2002-08-01 12:00:00 -0700", "[Family, Archive]", 2002),
    ("weddingdetails.htm", "2002-08-01-wedding-details.md", "Wedding Details", "2002-08-01 12:00:00 -0700", "[Family, Archive]", 2002),
    ("bleeth.htm", "2000-01-01-bleeth.md", "Yasmine Bleeth", "2000-01-01 12:00:00 -0700", "[Archive]", 2000),
    ("othertoddbradleys.htm", "2000-01-01-other-todd-bradleys.md", "Other Todd Bradleys", "2000-01-01 12:00:00 -0700", "[Archive]", 2000)
]

for args in pages_to_convert:
    convert_post(*args)
