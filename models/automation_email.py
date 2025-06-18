import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class AIMessageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_email_body(self, user_prompt):
        prompt = (
    "You are an AI assistant that writes professional emails.\n"
    "Follow these instructions carefully:\n\n"
    "1. If the user's input is a task (e.g., 'write', 'draft', 'generate'), create a full, professional email with:\n"
    "   - Greeting (e.g., Dear [Name],)\n"
    "   - Clear, concise main message\n"
    "   - Closing line (e.g., Looking forward to your response)\n"
    "   - Sign-off (e.g., Best regards, [Your Name])\n\n"
    "2. If the message starts with 'Send this:', return the exact message following it—DO NOT rewrite or expand it.\n\n"
    "3. If the message is short and simple (e.g., 'See you at 3 PM'), just send it as-is.\n"
    "   Only generate a full email when explicitly asked.\n\n"
    "===============================\n"
    "📌 Examples:\n"
    "-----------------------------\n"
    "User: Write a thank-you email to my professor for guiding my project.\n"
    "Response:\n"
    "Dear Professor,\n\n"
    "I wanted to extend my heartfelt thanks for your invaluable guidance throughout my project. Your insights and encouragement made a significant difference, and I truly appreciate your support.\n\n"
    "Looking forward to staying in touch.\n\n"
    "Best regards,\n"
    "Srivathsa\n"
    "-----------------------------\n"
    "User: Send this: Let’s meet at 2 PM in the library.\n"
    "Response:\n"
    "Let’s meet at 2 PM in the library.\n"
    "-----------------------------\n"
    "User: Just wanted to check if you're free for a quick sync today.\n"
    "Response:\n"
    "Just wanted to check if you're free for a quick sync today.\n"
    "-----------------------------\n"
    "User: Write an email apologizing to my team for missing the morning stand-up due to an emergency.\n"
    "Response:\n"
    "Dear Team,\n\n"
    "I sincerely apologize for missing this morning’s stand-up meeting. An unexpected emergency came up, and I wasn’t able to inform you in advance. I’ve gone through the updates and will make sure to catch up on my tasks.\n\n"
    "Thank you for your understanding.\n\n"
    "Best regards,\n"
    "Srivathsa\n"
    "===============================\n\n"
    f"Now, here is the user's input:\n"
    f"{user_prompt}\n\n"
    "Your email response:"
)
        
        try:
            response = self.client.chat.completions.create(
                    model="gpt-4o-mini",                          # 🧠 Fast + smart model
                    messages=[{"role": "user", "content": prompt}],  # 🗣️ Single user message
                    temperature=0.7,                              # 🎨 Creative but controlled
                    max_tokens=600,                               # 🧾 Long enough for full email
                    top_p=1.0,                                    # 🎯 Don't restrict randomness
                    frequency_penalty=0.2,                        # ♻️ Reduce repetition
                    presence_penalty=0.3                          # 🆕 Encourage fresh content
                )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
            return user_prompt  

class AutomationEmail:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.server = "smtp.gmail.com"
        self.port = 587
        self.ai_generator = AIMessageGenerator()

    def send_email(self, data):
        recipient_email = data.get("to")
        subject = data.get("subject", "No Subject")
        raw_body = data.get("body", "")

        if not recipient_email:
            raise ValueError("Recipient email address is required.")

        # AI logic to decide generation or direct send
        if raw_body.lower().startswith("write") or "email" in raw_body.lower():
            print("💡 Generating email body using AI...")
            body = self.ai_generator.generate_email_body(raw_body)
        elif raw_body.lower().startswith("send this:"):
            body = raw_body.split("send this:", 1)[1].strip()
        else:
            body = raw_body  # fallback if undecidable

        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.server, self.port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {recipient_email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
