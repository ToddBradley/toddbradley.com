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
        
        # Dynamically determine the exact column names to avoid schema errors
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'comments'")
        columns = [row['column_name'] for row in cur.fetchall()]
        
        time_col = 'created_at' if 'created_at' in columns else 'creation_date' if 'creation_date' in columns else 'creationdate'
        
        query = f"SELECT * FROM comments WHERE state = 1 AND {time_col} >= NOW() - INTERVAL '65 minutes'"
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
        author = c.get('commenter_name') or c.get('author_name') or c.get('author') or 'Unknown'
        text = c.get('markdown') or c.get('html') or c.get('body') or 'No text'
        path = c.get('path') or c.get('url') or 'Unknown page'
        
        body += f"Post: {path}\nAuthor: {author}\nComment:\n{text}\n"
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