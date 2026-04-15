import os
import re

POSTS = [
    "_posts/2001/2001-10-11-october-2001-vacation.md",
    "_posts/2003/2003-05-31-san-juan-river-trip.md",
    "_posts/2002/2002-10-02-my-suv-backlash.md",
    "_posts/2005/2005-08-01-reunion-2005.md",
    "_posts/2004/2004-11-25-thanksgiving-2004.md",
    "_posts/2001/2001-01-01-cd-hunter-review.md",
    "_posts/2002/2002-01-01-favorite-recipes.md",
    "_posts/1985/1985-06-01-europe-1985.md",
    "_posts/2004/2004-05-01-kitchen-remodel.md",
    "_posts/2003/2003-12-01-walt-disney-world.md",
    "_posts/2000/2000-01-01-tfc-guide.md",
    "_posts/2000/2000-01-01-my-history.md",
    "_posts/2000/2000-01-01-books-i-recommend.md",
    "_posts/2000/2000-01-01-games-i-play.md",
    "_posts/2000/2000-01-01-things-i-do.md",
    "_posts/2000/2000-01-01-contact-info.md",
    "_posts/2000/2000-01-01-for-sale.md",
    "_posts/2000/2000-01-01-my-wishlist.md",
    "_posts/2002/2002-09-22-beth-bigfoot.md",
    "_posts/2000/2000-01-01-squish.md",
    "_posts/2000/2000-01-01-wireless.md",
    "_posts/2002/2002-08-01-our-wedding.md",
    "_posts/2002/2002-08-01-wedding-details.md",
    "_posts/2000/2000-01-01-bleeth.md",
    "_posts/2000/2000-01-01-other-todd-bradleys.md"
]

BIT_ROT_IMG = "![ (Bit Rot)](/assets/img/bit-rot.svg)"
BIT_ROT_LINK = "[![ (Bit Rot)](/assets/img/bit-rot.svg)](/bit-rot/)"

missing_count = 0

for post_path in POSTS:
    if not os.path.exists(post_path):
        continue

    with open(post_path, "r", encoding="utf-8") as f:
        content = f.read()

    def repl_linked_img(m):
        global missing_count
        alt_text = m.group(1)
        img_src = m.group(2)
        link_href = m.group(3)

        local_img = img_src.lstrip("/")
        local_link = link_href.lstrip("/")

        img_missing = img_src.startswith("/uploads") and not os.path.exists(local_img)
        link_missing = link_href.startswith("/uploads") and not os.path.exists(local_link)

        if img_missing or link_missing:
            print(f"Missing image/link: {img_src} or {link_href} in {post_path}")
            missing_count += 1
            return BIT_ROT_LINK
        return m.group(0)

    def repl_plain_img(m):
        global missing_count
        alt_text = m.group(1)
        img_src = m.group(2)

        local_path = img_src.lstrip("/")
        if img_src.startswith("/uploads") and not os.path.exists(local_path):
            print(f"Missing image: {img_src} in {post_path}")
            missing_count += 1
            return BIT_ROT_IMG
        return m.group(0)

    linked_pattern = re.compile(r'\[!\[(.*?)\]\((.*?)\)\]\((.*?)\)')
    new_content = linked_pattern.sub(repl_linked_img, content)

    plain_pattern = re.compile(r'(?<!\[)!\[(.*?)\]\((.*?)\)')
    new_content = plain_pattern.sub(repl_plain_img, new_content)

    if new_content != content:
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(new_content)

print(f"Total missing images replaced with bit rot: {missing_count}")
