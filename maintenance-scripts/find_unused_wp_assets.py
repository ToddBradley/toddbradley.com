import os
import re

def find_references(filename):
    """
    Search for filename in all _posts, pages, _tabs, _includes, _layouts.
    """
    cmd = f"grep -r '{filename}' _posts pages _tabs _includes _layouts index.html 2>/dev/null"
    res = os.popen(cmd).read()
    return res

def check_exists_elsewhere(filename, relative_path):
    """
    Check if the filename exists in other standard locations.
    """
    search_dirs = ['uploads', 'assets/images', 'assets/img']
    found_at = []

    for d in search_dirs:
        if not os.path.exists(d):
            continue

        # Check root of the search dir
        candidate = os.path.join(d, filename)
        if os.path.exists(candidate):
            found_at.append(candidate)

        # Recursive search for the filename in these directories
        find_cmd = f"find {d} -name '{filename}' 2>/dev/null"
        find_res = os.popen(find_cmd).read().strip().split('\n')
        for path in find_res:
            if path and path not in found_at:
                found_at.append(path)

    return found_at

def main():
    base_dir = 'assets/wp-content'
    all_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f == '.DS_Store': continue
            full_path = os.path.join(root, f)
            all_files.append(full_path)

    print(f"Checking {len(all_files)} files in {base_dir}...")

    unused = []
    used = []
    duplicated = []

    for f_path in all_files:
        filename = os.path.basename(f_path)

        refs = find_references(filename)
        others = check_exists_elsewhere(filename, f_path)

        if not refs:
            unused.append(f_path)
            if others:
                duplicated.append((f_path, others))
        else:
            # Referenced somewhere
            # Check if any reference actually points to this path
            # (e.g., contains 'wp-content')
            if 'wp-content' in refs:
                used.append(f_path)
            else:
                unused.append(f_path)
                if others:
                    duplicated.append((f_path, others))

    print("\n--- Summary ---")
    print(f"Total files checked: {len(all_files)}")
    print(f"Used (referenced with 'wp-content'): {len(used)}")
    print(f"Unused: {len(unused)}")
    print(f"  of which are duplicated elsewhere: {len(duplicated)}")

    print("\n--- Used Files ---")
    for f in used:
        print(f)

    print("\n--- Unused Files Duplicated Elsewhere ---")
    for f_path, others in duplicated:
        print(f"{f_path} -> exists at {', '.join(others)}")

if __name__ == "__main__":
    main()
