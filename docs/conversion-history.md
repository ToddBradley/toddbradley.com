# WordPress to Jekyll Conversion History

This file contains the historical project memory from the conversion phase of toddbradley.com (Jan 2026).

## Gemini Added Memories

- The user is converting a static WordPress site to Jekyll. We have switched to the Chirpy theme and addressed Sass warnings. The user identified issues with pages p-1206.html and p-629.html where WordPress-specific content (front matter, 'Posted on...' line, 'Share this:' and 'Like this:' sections) was not being properly removed. The converter.py script has been updated in two rounds to handle different WordPress theme structures and to more aggressively remove unwanted sections. The last action was running converter.py, which completed successfully, but then a 429 API error occurred, preventing further immediate action. The next steps are to re-run link_fixer.py, rebuild the Jekyll site, and then check p-629.html to confirm fixes.
- Future tasks for toddbradley.com migration:

1. Fix broken image links (likely path issues).
2. Clean up sidebar pages (move unsuitable ones to posts or remove).
3. Investigate and fix suspicious filenames (e.g., ending in ' 4.md').
4. Implement a strategy for retaining/migrating comments (consider data files or static comment system).
5. Audit unconverted HTML files to ensure no content is lost.
6. Organize `_posts` by year for better management.

- The migration scripts have been refactored: 'converter.py' now handles year-based subdirectory organization directly, rendering 'organize_posts.py' obsolete (which has been deleted). The Jekyll site's homepage has been fixed by enabling 'jekyll-paginate' in '\_config.yml' and renaming 'index.markdown' to 'index.html', successfully displaying a paginated list of posts.
- 'converter.py' has been updated with an 'IGNORED_PAGES' list to permanently exclude specific legacy pages (Exploding Corpse, Heidi's Deli, Digital Film Sound, Page Not Found) from being converted and appearing in the site navigation.
