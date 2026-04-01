import re
import os

file_path = '_posts/2023/2023-10-11-p-3469.md'

with open(file_path, 'r') as f:
    content = f.read()

# CSS for the gallery
gallery_style = """
<style>
  .image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }
  .image-gallery img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
  }
  .image-gallery img:hover {
    transform: scale(1.05);
  }
</style>
"""

# Pattern to match the image blocks: [![](/url)](/url) or [![](cdn_url)](cdn_url)
# Some are just ![](/url) but let's match the common [![](...)] pattern
image_pattern = r'\[!\[\]\((.*?)\)\]\((.*?)\)'
# Also match simple ![](/url)
simple_image_pattern = r'!\[\]\((.*?)\)'

# Find the start and end of the image block
# It starts around line 15 and ends before the last paragraph
lines = content.split('\n')
new_lines = []
image_block_started = False
image_block_ended = False
captured_images = []

for line in lines:
    # Check if line contains an image
    match_linked = re.search(image_pattern, line)
    match_simple = re.search(simple_image_pattern, line)
    
    if match_linked or match_simple:
        if not image_block_started:
            image_block_started = True
            new_lines.append('<div class="image-gallery" markdown="1">')
        
        # We want to extract the image URL. 
        # If it was [![](inner)](outer), we take inner.
        if match_linked:
            img_url = match_linked.group(1)
        else:
            img_url = match_simple.group(1)
            
        # Strip sizing params from CDN URLs for the gallery view if desired, 
        # but Chirpy's lightbox will handle it.
        # Actually, let's keep them as is but simplify to just ![](/url)
        captured_images.append(f"![]({img_url})")
    else:
        if image_block_started and not image_block_ended and line.strip() != "":
            # End of image block
            new_lines.extend(captured_images)
            new_lines.append('</div>')
            image_block_ended = True
            new_lines.append(line)
        else:
            new_lines.append(line)

# If the block never formally ended (e.g. images at end of file)
if image_block_started and not image_block_ended:
    new_lines.extend(captured_images)
    new_lines.append('</div>')

# Add style at the top of the content (after front matter)
final_lines = []
for i, line in enumerate(new_lines):
    final_lines.append(line)
    if line == '---' and i > 0: # End of front matter
        final_lines.append(gallery_style)

# Join and write back
with open(file_path, 'w') as f:
    f.write('\n'.join(final_lines))

print("Gallery created successfully.")
