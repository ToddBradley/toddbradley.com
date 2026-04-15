import os
import re

POSTS_DIR = "_posts"

boilerplate_pattern = re.compile(r'^\[.*?\]\(\.\./cat-\d+/\)\s+Todd Bradley on.*?\n', re.MULTILINE)
cat_link_pattern = re.compile(r'\[(.*?)\]\(\.\./cat-\d+/\)')

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def extract_categories(content):
    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx != -1:
            front_matter = content[3:end_idx]
            match = re.search(r'^categories:\s*\[(.*?)\]', front_matter, re.MULTILINE)
            if match:
                return [c.strip().strip("'\"") for c in match.group(1).split(',')]
    return []

GENERIC_LINK_TEXT = {'here', 'this link', 'here are all the blog articles', 'http'}

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if '../cat-' not in content:
        return

    # 1. Remove boilerplate
    new_content = boilerplate_pattern.sub('', content)

    # 2. Fix in-text links
    categories = extract_categories(content)
    front_matter_cat = categories[0] if categories else ""

    def repl_link(match):
        link_text = match.group(1)
        lower_link = link_text.lower()

        # Logic to determine category
        if lower_link in GENERIC_LINK_TEXT or lower_link.startswith('http') or 'blog article' in lower_link:
            cat_to_use = front_matter_cat
        else:
            cat_to_use = link_text if link_text else front_matter_cat

        if cat_to_use and cat_to_use.lower() != 'uncategorized':
            slug = slugify(cat_to_use)
            return f"[{link_text}](/categories/{slug}/)"
        else:
            return f"[{link_text}](/categories/)"

    new_content = cat_link_pattern.sub(repl_link, new_content)

    # Cleanup any extra newlines left around
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

updates = 0
for root, _, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            process_file(filepath)
            updates += 1
print("Done processing.")
