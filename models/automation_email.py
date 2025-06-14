import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file



class AutomationEmail:
    
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.server = "smtp.gmail.com"
        self.port = 587  # For starttls
    
    def send_email(self, data):
        recipient_email = data.get("to")
        subject = data.get("subject", "No Subject")
        body = data.get("body", "")
        
        if not recipient_email:
            raise ValueError("Recipient email address is required.")
        
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.server, self.port)
            server.starttls()  
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent successfully to {recipient_email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            