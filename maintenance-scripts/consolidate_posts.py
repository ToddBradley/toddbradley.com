import os
import shutil
import filecmp
from pathlib import Path

def consolidate():
    posts_dir = Path('_posts')
    if not posts_dir.exists():
        print("Error: _posts directory not found.")
        return

    # Find all directories that have a space (e.g., "2024 2")
    messy_dirs = [d for d in posts_dir.iterdir() if d.is_dir() and ' ' in d.name]

    print(f"Found {len(messy_dirs)} messy directories to consolidate.")

    for messy_dir in messy_dirs:
        # Determine the target directory (the first part of the name, e.g., "2024")
        target_name = messy_dir.name.split(' ')[0]
        target_dir = posts_dir / target_name

        if not target_dir.exists():
            print(f"Creating missing target directory: {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Consolidating {messy_dir} -> {target_dir}")

        for file_path in messy_dir.iterdir():
            if not file_path.is_file():
                continue

            dest_path = target_dir / file_path.name

            if dest_path.exists():
                # Compare files
                if filecmp.cmp(file_path, dest_path, shallow=False):
                    # They are identical, safe to delete the messy one
                    file_path.unlink()
                else:
                    # They are different! Rename and move to avoid loss
                    conflict_name = f"CONFLICT_{messy_dir.name}_{file_path.name}"
                    print(f"  [CONFLICT] {file_path.name} is different. Saving as {conflict_name}")
                    shutil.move(str(file_path), str(target_dir / conflict_name))
            else:
                # File doesn't exist in target, just move it
                shutil.move(str(file_path), str(dest_path))

        # Remove the messy directory if it's now empty
        try:
            messy_dir.rmdir()
            print(f"  Successfully removed empty directory: {messy_dir}")
        except OSError:
            print(f"  Warning: Directory not empty, could not remove: {messy_dir}")

if __name__ == "__main__":
    consolidate()
