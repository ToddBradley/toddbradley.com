import os
import smtplib
from email.message import EmailMessage
import psycopg2
import psycopg2.extras

def check_pending_comments():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL not set. Skipping.")
        return

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Get all columns for the comments table
        table_name = 'cm_comments'
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = [row['column_name'] for row in cur.fetchall()]
        
        if not columns:
            print(f"Error: Table '{table_name}' not found or has no columns.")
            return

        print(f"Confirmed columns in {table_name}: {columns}")

        # 2. Identify the timestamp column dynamically from the existing columns
        # Comentario 3.x typically uses 'created_ts' or 'created_at'
        time_col = None
        for candidate in ['created_ts', 'created_at', 'creation_date', 'creationdate']:
            if candidate in columns:
                time_col = candidate
                break
        
        if not time_col:
            print(f"Error: Could not find a timestamp column in {columns}")
            return

        # 3. Identify the pending status column
        # Based on your hint, it is 'is_pending'
        status_col = 'is_pending' if 'is_pending' in columns else None
        if not status_col:
            print(f"Error: Could not find 'is_pending' column in {columns}")
            return

        # 4. Construct the query using only known-good columns
        query = f"SELECT * FROM {table_name} WHERE {status_col} = TRUE AND {time_col} >= NOW() - INTERVAL '65 minutes'"
        print(f"Executing: {query}")
        
        cur.execute(query)
        pending = cur.fetchall()
        
        if not pending:
            print("No new pending comments found.")
            return
        
        print(f"Found {len(pending)} pending comment(s). Sending email...")
        send_email(pending, columns)
        
    except Exception as e:
        print(f"Error checking comments: {e}")

def send_email(comments, available_columns):
    sender = os.environ.get('SMTP_USERNAME')
    password = os.environ.get('SMTP_PASSWORD')
    receiver = 'todd@toddbradley.com'
    
    if not sender or not password:
        print("SMTP credentials not set. Cannot send email.")
        return

    msg = EmailMessage()
    msg['Subject'] = f"Action Required: {len(comments)} New Pending Comment(s)"
    msg['From'] = sender
    msg['To'] = receiver
    
    body = "You have new comments awaiting moderation on toddbradley.com:\n\n"
    for c in comments:
        # Only reference columns that we know exist
        author = 'Unknown'
        for col in ['commenter_name', 'author_name', 'author_id']:
            if col in available_columns and c.get(col):
                author = c[col]
                break
        
        text = 'No content'
        for col in ['markdown', 'html', 'body']:
            if col in available_columns and c.get(col):
                text = c[col]
                break

        page = 'Unknown page'
        for col in ['path', 'url', 'domain_page_id']:
            if col in available_columns and c.get(col):
                page = c[col]
                break
        
        body += f"Post/Page: {page}\nAuthor: {author}\nComment:\n{text}\n"
        body += "-" * 40 + "\n"
        
    body += "\nManage them here: https://comentario-production-7369.up.railway.app/"
    msg.set_content(body)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    check_pending_comments()