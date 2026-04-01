import os
import re
import shutil

files_to_move = [
    'assets/wp-content/uploads/2013/03/atlantatraffic.jpg',
    'assets/wp-content/uploads/2013/03/arab-businessman.jpg',
    'assets/wp-content/uploads/2013/03/obama3.jpg',
    'assets/wp-content/uploads/2013/03/obama2.jpg',
    'assets/wp-content/uploads/2013/03/obama1.jpg',
    'assets/wp-content/uploads/2013/03/CNCS_08_0922_MH_024-X2.jpg',
    'assets/wp-content/uploads/2013/03/MTH_08_0520_061-X2.jpg',
    'assets/wp-content/uploads/2015/08/countries-planned.png',
    'assets/wp-content/uploads/2015/12/tilonia-12.jpg',
    'assets/wp-content/uploads/2015/12/amberfort-14.jpg',
    'assets/wp-content/uploads/2021/05/Ernie-Bradley-Obituary.pdf'
]

# Find references and update them
for old_path in files_to_move:
    # Extract year and filename
    parts = old_path.split('/')
    year = parts[3]
    filename = parts[-1]
    
    # Target path
    new_dir = f"uploads/{year}"
    new_path = f"{new_dir}/{filename}"
    new_url = f"/{new_dir}/{filename}"
    
    print(f"Moving {old_path} -> {new_path}")
    
    # Ensure target directory exists
    os.makedirs(new_dir, exist_ok=True)
    
    # Move the file
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
    
    # Update markdown files
    # We will search for any URL ending with the filename and containing 'wp-content'
    cmd = f"grep -rl '{filename}' _posts pages 2>/dev/null"
    referencing_files = os.popen(cmd).read().strip().split('\n')
    
    for md_file in referencing_files:
        if not md_file:
            continue
            
        with open(md_file, 'r') as f:
            content = f.read()
            
        # Regex to find wp-content links to this file
        # Matches: http://.../wp-content/.../filename OR https://i0.wp.com/.../filename OR /assets/wp-content/.../filename
        # We'll replace it with the new local URL.
        # A simpler way: replace any string matching r'\(?[^()]*wp-content[^()]*' + filename + r'\)?' inside the markdown?
        # Actually, let's just do a regex replace for the URL part.
        
        pattern = r'(?:https?://[^/]+/|https?://i\d\.wp\.com/[^/]+/|/assets/)?wp-content/uploads/\d{4}/\d{2}/' + re.escape(filename)
        
        new_content = re.sub(pattern, new_url, content)
        
        if content != new_content:
            with open(md_file, 'w') as f:
                f.write(new_content)
            print(f"  Updated references in {md_file}")

# Clean up empty directories in assets/wp-content
for root, dirs, files in os.walk('assets/wp-content', topdown=False):
    for d in dirs:
        dir_path = os.path.join(root, d)
        try:
            os.rmdir(dir_path)
        except OSError:
            pass
try:
    os.rmdir('assets/wp-content')
except OSError:
    pass

print("Done.")
