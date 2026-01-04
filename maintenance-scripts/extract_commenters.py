import csv
import html
import re

input_file = 'wp_comments.csv'
output_file = 'cleaned_commenters.csv'
my_email = 'todd@toddbradley.com'

# List of defunct or unwanted domains
blocklist_domains = {
    'facebook.com',
    'geocities.com',
    'myspace.com',
    'alumni.univ.edu',
    'man-diploms-srednee24.com',
    '1win-aviator-casino.store',
    '1234techland.info',
    'loancalculator.world',
    'egurobetbr.com',
}

# Regex for strict email validation
# Matches: string@string.string (basic but effective for filtering out User-Agents)
email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

commenters = set()

with open(input_file, mode='r', encoding='utf-8') as f:
    # Use quotes correctly if possible, but handle loose CSVs carefully
    reader = csv.reader(f, delimiter=';')
    try:
        header = next(reader) # Skip header
    except StopIteration:
        pass # Empty file

    for row in reader:
        if len(row) < 2:
            continue

        email = row[1].strip().lower()

        # 1. Regex Validation
        if not email_pattern.match(email):
            continue

        domain = email.split('@')[-1]

        # 2. Blocklist and Logic Filters
        if (email == my_email or
            domain.endswith('.ru') or
            domain in blocklist_domains):
            continue

        commenters.add(email)

# Sort alphabetically
sorted_emails = sorted(list(commenters))

with open(output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # No header, just the email column
    for email in sorted_emails:
        writer.writerow([email])

print(f"Extracted {len(sorted_emails)} unique emails to {output_file}")
