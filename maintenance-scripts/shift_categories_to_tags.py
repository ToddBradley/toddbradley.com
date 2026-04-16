import os
import re

count = 0
for root, _, files in os.walk('_posts'):
    for f in files:
        if not f.endswith('.md'):
            continue

        filepath = os.path.join(root, f)
        with open(filepath, 'r') as fp:
            content = fp.read()

        # Find categories line
        cat_match = re.search(r'^categories:\s*\[(.*?)\]', content, re.MULTILINE)
        if not cat_match:
            continue

        cats = [c.strip() for c in cat_match.group(1).split(',') if c.strip()]
        if len(cats) <= 1:
            continue

        primary = cats[0]
        secondary = cats[1:]

        # Replace categories line with just primary
        new_content = content[:cat_match.start()] + f'categories: [{primary}]' + content[cat_match.end():]

        # Find tags line
        tag_match = re.search(r'^tags:\s*\[(.*?)\]', new_content, re.MULTILINE)
        if tag_match:
            tags = [t.strip() for t in tag_match.group(1).split(',') if t.strip()]
        else:
            tags = []

        # Append secondary cats to tags, keeping them lowercase
        for s in secondary:
            s_tag = s.lower()
            if s_tag not in tags:
                tags.append(s_tag)

        tags_str = ', '.join(tags)

        if tag_match:
            # Replace tags line
            tag_match2 = re.search(r'^tags:\s*\[(.*?)\]', new_content, re.MULTILINE)
            new_content = new_content[:tag_match2.start()] + f'tags: [{tags_str}]' + new_content[tag_match2.end():]
        else:
            # Insert tags line below categories
            cat_match2 = re.search(r'^categories:\s*\[.*?\]\n', new_content, re.MULTILINE)
            insert_pos = cat_match2.end()
            new_content = new_content[:insert_pos] + f'tags: [{tags_str}]\n' + new_content[insert_pos:]

        with open(filepath, 'w') as fp:
            fp.write(new_content)
        count += 1
        # print(f'Updated {filepath}: categories -> [{primary}], tags -> [{tags_str}]')

print(f'Total files updated: {count}')
