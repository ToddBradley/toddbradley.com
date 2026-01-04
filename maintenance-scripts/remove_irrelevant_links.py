import os
import re

def clean_markdown_links(directory):
    # Pattern 1: [text](/) or [text]() -> remove link, keep text
    # Pattern 2: [![] (img)](/) or [![] (img)]() -> remove link, keep image
    # Pattern 3: [](/) or []() -> remove entirely

    # This regex matches [content](url)
    # Group 1: content (between [])
    # Group 2: url (between ())
    link_pattern = re.compile(r'(?<!!Source: )\[([^\]]*)\]\(([^)]*)\)')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                def replace_link(match):
                    link_text = match.group(1).strip()
                    url = match.group(2).strip()

                    # Irrelevant URLs: empty, just a slash, or just a hash
                    if url in ['', '/', '#']:
                        if not link_text:
                            # Both empty: []() or [](/) -> Remove entirely
                            return ''
                        else:
                            # Link text exists: [Text](/) -> Keep 'Text'
                            return link_text

                    # Keep valid links
                    return match.group(0)

                new_content = link_pattern.sub(replace_link, content)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Cleaned links in: {file_path}")

if __name__ == "__main__":
    print("Cleaning irrelevant links in _posts...")
    clean_markdown_links('_posts')
    print("Cleaning irrelevant links in pages...")
    clean_markdown_links('pages')
