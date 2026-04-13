import os
import re

POSTS_DIR = "_posts"
boilerplate_pattern = re.compile(r'^\[.*?\]\(\.\./cat-\d+/\)\s+Todd Bradley on.*$', re.MULTILINE)
cat_link_pattern = re.compile(r'\[(.*?)\]\(\.\./cat-\d+/\)')

for root, _, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            if '../cat-' not in content:
                continue

            new_content = boilerplate_pattern.sub('', content)
            matches = cat_link_pattern.findall(new_content)
            if matches:
                print(f"{filepath}: {matches}")
