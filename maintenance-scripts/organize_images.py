import os
import re
import shutil
import glob
from datetime import datetime

# Configuration
POSTS_DIR = '_posts'
UPLOADS_DIR = 'uploads'
ASSETS_DIRS = [
    'assets/wp-content/uploads',
    'assets/images',
    'assets/img',
    'assets/wp-content' # Catch loose files
]

# Regex to find markdown image links: ![alt](url)
# Also handles HTML img tags if needed, but standardizing on markdown first.
# Focusing on the link part `(url)`
LINK_REGEX = re.compile(r'!\[.*?\]\((.*?)\)')
HTML_IMG_REGEX = re.compile(r'<img.*?src=["\'](.*?)["\']')

def get_post_year(filename):
    # Filename format: YYYY-MM-DD-title.md
    match = re.match(r'(\d{4})-\d{2}-\d{2}-', os.path.basename(filename))
    if match:
        return match.group(1)
    return 'uncategorized'

def find_source_file(url_path):
    # Url path might be absolute or relative, local or remote (wp.com)
    # We strip domain and query params
    clean_path = url_path.split('?')[0].split('#')[0]

    # Common legacy patterns
    # https://i0.wp.com/toddbradley.com/wp-content/uploads/2015/10/img.jpg
    # http://toddbradley.com/wp-content/uploads/2015/10/img.jpg
    # /assets/img/converted/img.jpg

    filename = os.path.basename(clean_path)

    # Search in known asset dirs
    # 1. Try to guess structure from URL if it contains 'wp-content/uploads/YYYY/MM'
    match_wp = re.search(r'wp-content/uploads/(\d{4})/(\d{2})/(.*)', clean_path)
    if match_wp:
        year, month, name = match_wp.groups()
        # Check specific path
        candidate = os.path.join('assets/wp-content/uploads', year, month, name)
        if os.path.exists(candidate):
            return candidate

    # 2. Brute force search by filename in asset dirs
    for root_dir in ASSETS_DIRS:
        for root, dirs, files in os.walk(root_dir):
            if filename in files:
                return os.path.join(root, filename)

    return None

def process_content():
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    # Content sources: (directory, target_subfolder_logic)
    sources = [
        (POSTS_DIR, lambda fp: get_post_year(fp)),
        ('pages', lambda fp: 'pages'),
        ('_tabs', lambda fp: 'site'),
        ('_drafts', lambda fp: 'drafts')
    ]

    for content_dir, subfolder_func in sources:
        if not os.path.exists(content_dir):
            continue

        files = glob.glob(os.path.join(content_dir, '**', '*.md'), recursive=True)
        files += glob.glob(os.path.join(content_dir, '**', '*.html'), recursive=True)

        for filepath in files:
            subfolder = subfolder_func(filepath)
            target_dir = os.path.join(UPLOADS_DIR, subfolder)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            modified = False

            # Find all links
            links = LINK_REGEX.findall(content) + HTML_IMG_REGEX.findall(content)

            for link in links:
                # Skip if already in correct uploads dir
                if link.startswith(f'/uploads/{subfolder}/'):
                    continue

                source_file = find_source_file(link)

                if source_file:
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)

                    filename = os.path.basename(source_file)
                    target_path = os.path.join(target_dir, filename)

                    if os.path.exists(target_path) and not os.path.samefile(source_file, target_path):
                        if os.path.getsize(source_file) != os.path.getsize(target_path):
                            name, ext = os.path.splitext(filename)
                            filename = f"{name}_{subfolder}{ext}"
                            target_path = os.path.join(target_dir, filename)

                    if not os.path.exists(target_path):
                        print(f"Moving {source_file} -> {target_path}")
                        shutil.move(source_file, target_path)

                    # Update URL
                    new_url = f"/uploads/{subfolder}/{filename}"
                    new_content = new_content.replace(link, new_url)
                    modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    print(f"Updated {filepath}")

if __name__ == "__main__":
    process_content()
