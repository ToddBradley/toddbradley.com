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
        
        comment_table = 'cm_comments'
        
        # Dynamically determine the exact column names
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{comment_table}'")
        columns = [row['column_name'] for row in cur.fetchall()]
        
        if not columns:
            print(f"No columns found for {comment_table}. Exiting.")
            return

        # Determine the correct column for creation time
        time_col = 'creationdate' # default fallback
        if 'created_at' in columns:
            time_col = 'created_at'
        elif 'creation_date' in columns:
            time_col = 'creation_date'
        elif 'created_ts' in columns:
            time_col = 'created_ts'
            
        print(f"Using timestamp column: {time_col}")
            
        # Instead of 'state = 1', we use the boolean 'is_pending' or similar based on your hint
        status_condition = "is_pending = TRUE"
        if 'is_pending' not in columns:
            # Fallback if the user hint didn't exact match the column name
            if 'pending' in columns:
                status_condition = "pending = TRUE"
            elif 'approved' in columns:
                status_condition = "approved = FALSE"
            else:
                 print(f"Could not find a clear pending/approval column in {columns}")
                 return
            
        # Ensure the interval is compatible with the timestamp format (usually timestamptz)
        query = f"SELECT * FROM {comment_table} WHERE {status_condition} AND {time_col} >= NOW() - INTERVAL '65 minutes'"
        print(f"Executing query: {query}")
        
        cur.execute(query)
        pending = cur.fetchall()
        
        if not pending:
            print("No new pending comments found.")
            return
        
        print(f"Found {len(pending)} pending comment(s). Sending email...")
        send_email(pending)
        
    except Exception as e:
        print(f"Error checking comments: {e}")

def send_email(comments):
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
        # Safely extract fields regardless of exact column names in Comentario version
        author = c.get('commenter_name') or c.get('author_name') or c.get('author') or c.get('commenterhex') or c.get('author_id') or 'Unknown'
        text = c.get('markdown') or c.get('html') or c.get('body') or 'No text'
        path = c.get('path') or c.get('url') or c.get('domain_page_id') or 'Unknown page'
        
        body += f"Post/Page ID: {path}\nAuthor: {author}\nComment:\n{text}\n"
        body += "-" * 40 + "\n"
        
    body += "\nManage them here: https://comentario-production-7369.up.railway.app/"
    msg.set_content(body)
    
    try:
        # Standard Gmail SMTP configuration
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    check_pending_comments()