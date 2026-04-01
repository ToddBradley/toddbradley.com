import os
import glob
import re

post_file = '_posts/2023/2023-07-29-bradley-powers-wedding.md'
uploads_dir = 'uploads/2023'

# 1. Grab all the wedding photos and sort them
images = glob.glob(f'{uploads_dir}/best-wedding-photos - *.png')
images.sort(key=lambda x: int(re.search(r'best-wedding-photos - (\d+)\.png', x).group(1)))

# 2. Read the post content
with open(post_file, 'r') as f:
    content = f.read()

# 3. Clean up the signpost link (it's hardcoded as https://i0.wp.com/.../signpost.png)
# Replace it with simple ![](/uploads/2023/signpost.png)
content = re.sub(r'!\[.*?\]\(https?://.*?wp-content/uploads/\d{4}/\d{2}/signpost\.png.*?\)', r'![](/uploads/2023/signpost.png)', content)

# 4. Remove all the old best-wedding-photos links
# They are block of links at the top just after the front matter
# We will split at the front matter end "---" (the second one)
parts = content.split('---\n', 2)

if len(parts) == 3:
    front_matter = parts[0] + "---\n" + parts[1] + "---\n\n"
    body = parts[2]
    
    # Strip out the old image block (everything before "BROOKE POWERS")
    body_parts = body.split('BROOKE POWERSandTODD BRADLEY', 1)
    
    if len(body_parts) == 2:
        # Build the gallery HTML
        gallery_html = """<style>
  .image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 2rem;
  }
  .image-gallery img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
    margin: 0 !important;
  }
  .image-gallery img:hover {
    transform: scale(1.05);
  }
</style>

<div class="image-gallery">
"""
        for img_path in images:
            # URL encode the spaces in the filename
            img_url = "/" + img_path.replace(" ", "%20")
            gallery_html += f'  <img src="{img_url}" alt="Wedding Photo" />\n'
            
        gallery_html += "</div>\n\n"
        
        # Add the remaining text back (fix the spacing issue in BROOKE POWERSandTODD BRADLEY while we're at it)
        remaining_body = "BROOKE POWERS and TODD BRADLEY" + body_parts[1]
        
        # Write back to file
        with open(post_file, 'w') as f:
            f.write(front_matter + gallery_html + remaining_body)
            
        print(f"Successfully updated post with {len(images)} gallery images and fixed signpost.")
    else:
        print("Error: Could not find 'BROOKE POWERSandTODD BRADLEY' text.")
else:
    print("Error: Could not parse front matter.")
