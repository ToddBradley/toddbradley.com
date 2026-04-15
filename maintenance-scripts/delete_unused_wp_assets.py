import os

def find_references(filename):
    cmd = f"grep -r '{filename}' _posts pages _tabs _includes _layouts index.html 2>/dev/null"
    return os.popen(cmd).read()

def main():
    base_dir = 'assets/wp-content'
    deleted_count = 0
    kept_count = 0

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            f_path = os.path.join(root, f)
            if f == '.DS_Store':
                os.remove(f_path)
                continue

            filename = os.path.basename(f_path)
            refs = find_references(filename)

            if refs and 'wp-content' in refs:
                kept_count += 1
            else:
                os.remove(f_path)
                deleted_count += 1

    # Clean up empty directories
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                os.rmdir(dir_path)
            except OSError:
                pass

    print(f"Deleted {deleted_count} unused files (plus .DS_Store files).")
    print(f"Kept {kept_count} used files.")

if __name__ == "__main__":
    main()
