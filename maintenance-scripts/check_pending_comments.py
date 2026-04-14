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
        
        # Keep it simple: Exact query using known columns
        query = "SELECT * FROM cm_comments WHERE is_pending = TRUE AND ts_created >= NOW() - INTERVAL '65 minutes'"
        print(f"Executing: {query}")
        
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
        # Safely extract comment details using standard dictionary lookups
        author = c.get('commenter_name') or c.get('author_name') or 'Unknown'
        text = c.get('markdown') or c.get('body') or 'No content'
        page = c.get('domain_page_id') or c.get('path') or 'Unknown page'
        
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