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
    for p in soup.find_all('p'):
        if p.text and 'Page 1' in p.text and 'Page 2' in p.text:
            p.decompose()
    # Unwrap tables so markdownify doesn't eat the images
    for tag in soup.find_all(['table', 'tbody', 'thead', 'tr', 'td', 'th']):
        tag.unwrap()

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

        if tag.name == 'a' and not val.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            continue

        decoded_val = unquote(val)
        rel_dir = os.path.dirname(filepath)
        abs_src = os.path.normpath(os.path.join(rel_dir, decoded_val))

        if os.path.exists(abs_src):
            filename = os.path.basename(abs_src)
            dest_img_path = os.path.join(img_dir, filename)
            
            if not os.path.exists(dest_img_path):
                shutil.copy2(abs_src, dest_img_path)
            
            tag[attr] = f"/uploads/{year}/{filename}"

    body = soup.find('body')
    if body:
        h1 = body.find('h1')
        if h1:
            h1.decompose()
        return "".join(str(child) for child in body.contents)
    return ""

def reconvert_post(source_files, output_filename, title, date, categories, year):
    if isinstance(source_files, str):
        source_files = [source_files]
        
    print(f"Re-converting: {title}")
    combined_html = ""
    for source_file in source_files:
        full_path = os.path.join(SOURCE_DIR, source_file)
        if os.path.exists(full_path):
            combined_html += process_file_fixed(full_path, year) + "\n\n"

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

posts = [
    ([f"oct2001/oct2001_page{i}.htm" for i in range(1, 7)], "2001-10-11-october-2001-vacation.md", "October 2001 Vacation", "2001-10-11 12:00:00 -0600", "[Travel, Archive]", 2001),
    (["sanjuan.htm"], "2003-05-31-san-juan-river-trip.md", "My San Juan River Trip, May 2003", "2003-05-31 12:00:00 -0600", "[Travel, Archive]", 2003),
    (["suvbacklash.htm"], "2002-10-02-my-suv-backlash.md", "My SUV Backlash", "2002-10-02 12:00:00 -0600", "[Vehicles, Archive]", 2002),
    (["reunion2005.htm"], "2005-08-01-reunion-2005.md", "Reunion 2005", "2005-08-01 12:00:00 -0600", "[Family, Archive]", 2005),
    (["thanksgiving2004.htm"], "2004-11-25-thanksgiving-2004.md", "Thanksgiving 2004", "2004-11-25 12:00:00 -0700", "[Family, Archive]", 2004),
    (["cd.hunter.htm"], "2001-01-01-cd-hunter-review.md", "CD Hunter Review", "2001-01-01 12:00:00 -0700", "[Reviews, Archive]", 2001),
    (["recipes.htm"], "2002-01-01-favorite-recipes.md", "Favorite Recipes", "2002-01-01 12:00:00 -0700", "[Food, Archive]", 2002),
    (["photos/europe1985/europe_1985.htm"], "1985-06-01-europe-1985.md", "Europe 1985 Trip", "1985-06-01 12:00:00 -0700", "[Travel, Archive]", 1985),
    (["photos/kitchen/kitchen.html"], "2004-05-01-kitchen-remodel.md", "Kitchen Remodel", "2004-05-01 12:00:00 -0700", "[Home, Archive]", 2004),
    (["photos/walt_disney_world_2003.htm"], "2003-12-01-walt-disney-world.md", "Walt Disney World 2003", "2003-12-01 12:00:00 -0700", "[Travel, Archive]", 2003),
    (["tfcguide.htm"], "2000-01-01-tfc-guide.md", "Team Fortress Classic Guide", "2000-01-01 12:00:00 -0700", "[Gaming, Archive]", 2000),
    (["history.htm"], "2000-01-01-my-history.md", "My History", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    (["books.htm"], "2000-01-01-books-i-recommend.md", "Books I Recommend", "2000-01-01 12:00:00 -0700", "[Books, Archive]", 2000),
    (["games.htm"], "2000-01-01-games-i-play.md", "Games I Play", "2000-01-01 12:00:00 -0700", "[Gaming, Archive]", 2000),
    (["thingsido.htm"], "2000-01-01-things-i-do.md", "Things I Do", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    (["contact_info.htm"], "2000-01-01-contact-info.md", "Contact Info", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    (["forsale.htm"], "2000-01-01-for-sale.md", "Stuff For Sale", "2000-01-01 12:00:00 -0700", "[Archive]", 2000),
    (["wishlist.htm"], "2000-01-01-my-wishlist.md", "My Wishlist", "2000-01-01 12:00:00 -0700", "[About, Archive]", 2000),
    (["bethbigfoot.htm"], "2002-09-22-beth-bigfoot.md", "Beth is Bigfoot?", "2002-09-22 12:00:00 -0700", "[Archive]", 2002),
    (["squish.htm"], "2000-01-01-squish.md", "Squish", "2000-01-01 12:00:00 -0700", "[Archive]", 2000),
    (["wireless.htm"], "2000-01-01-wireless.md", "Wireless Internet", "2000-01-01 12:00:00 -0700", "[Tech, Archive]", 2000),
    (["wedding.htm"], "2002-08-01-our-wedding.md", "Our Wedding", "2002-08-01 12:00:00 -0700", "[Family, Archive]", 2002),
    (["weddingdetails.htm"], "2002-08-01-wedding-details.md", "Wedding Details", "2002-08-01 12:00:00 -0700", "[Family, Archive]", 2002),
    (["bleeth.htm"], "2000-01-01-bleeth.md", "Yasmine Bleeth", "2000-01-01 12:00:00 -0700", "[Archive]", 2000),
    (["othertoddbradleys.htm"], "2000-01-01-other-todd-bradleys.md", "Other Todd Bradleys", "2000-01-01 12:00:00 -0700", "[Archive]", 2000)
]

for args in posts:
    reconvert_post(*args)
