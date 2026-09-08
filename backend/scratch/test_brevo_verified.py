import os
import sys
import smtplib
import requests
from email.mime.text import MIMEText

sys.stdout.reconfigure(encoding='utf-8')

smtp_user = os.getenv("SMTP_USER", "a72cb8001@smtp-brevo.com").strip()
smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
brevo_api_key = os.getenv("BREVO_API_KEY", "").strip()
smtp_server = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com").strip()
sender_email = os.getenv("SENDER_EMAIL", "akr20101@gmail.com").strip()
recipient = os.getenv("TEST_RECIPIENT", "akr20101@gmail.com").strip()

print("==========================================================================")
print("RAW SMTP HANDSHAKE TEST")
print("==========================================================================")
print(f"SMTP Server: {smtp_server}:587")
print(f"SMTP User:   {smtp_user}")
print(f"Sender:      {sender_email}")
print(f"Recipient:   {recipient}")

if smtp_password:
    msg = MIMEText("<p>EduMind Production Test Email</p>", "html")
    msg["Subject"] = "EduMind SMTP Live Verification Test"
    msg["From"] = f"EduMind Security <{sender_email}>"
    msg["To"] = recipient

    try:
        with smtplib.SMTP(smtp_server, 587, timeout=10) as s:
            s.set_debuglevel(1)
            s.starttls()
            s.login(smtp_user, smtp_password)
            s.sendmail(sender_email, recipient, msg.as_string())
            print("\nSUCCESS: 235 Authentication Succeeded & Email Accepted!")
    except Exception as e:
        print("\nSMTP ERROR:", type(e).__name__, e)
else:
    print("\nNote: SMTP_PASSWORD is not set in local .env")

print("\n==========================================================================")
print("BREVO REST API TEST (HTTPS PORT 443)")
print("==========================================================================")
api_key = brevo_api_key or (smtp_password if smtp_password.startswith("xkeysib-") else None)
if api_key:
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {"accept": "application/json", "api-key": api_key, "content-type": "application/json"}
    payload = {
        "sender": {"name": "EduMind Security", "email": sender_email},
        "to": [{"email": recipient}],
        "subject": "EduMind REST API Verification Test",
        "htmlContent": "<p>Testing Brevo REST API fallback</p>"
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print("REST API ERROR:", e)
else:
    print("Note: BREVO_API_KEY (xkeysib-...) is not set in local .env")
