import os
import sys
import smtplib
import socket
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from backend/.env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
resolved_env_path = os.path.abspath(env_path)
load_dotenv(dotenv_path=resolved_env_path, override=True)

print("==========================================================================")
print("🔍 BREVO SMTP & REST API DIRECT DIAGNOSTIC TEST")
print("==========================================================================\n")
print(f"Loaded .env file path: {resolved_env_path}\n")

smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
smtp_password = raw_pass.replace(" ", "")
smtp_server = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com").strip()

try:
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
except ValueError:
    smtp_port = 587

sender_email = os.getenv("SENDER_EMAIL") or os.getenv("SMTP_FROM_EMAIL") or smtp_user or "akr20101@gmail.com"
test_recipient = os.getenv("TEST_RECIPIENT", "akr20101@gmail.com")
brevo_api_key = os.getenv("BREVO_API_KEY", "").strip().strip('"').strip("'")

print(f"1. ENVIRONMENT CONFIGURATION CHECK:")
print(f" - SMTP_SERVER : '{smtp_server}'")
print(f" - SMTP_PORT   : {smtp_port}")
print(f" - SMTP_USER   : '{smtp_user}'")
print(f" - SMTP_PASS   : '{'*' * len(smtp_password)}' (Length: {len(smtp_password)})")
print(f" - BREVO_API_KEY: '{'*' * len(brevo_api_key)}' (Length: {len(brevo_api_key)})")
print(f" - SENDER_EMAIL: '{sender_email}'")
print(f" - RECIPIENT   : '{test_recipient}'\n")

# Check missing vars
missing = []
if not smtp_user: missing.append("SMTP_USER")
if not smtp_password: missing.append("SMTP_PASSWORD")

if missing:
    print(f"❌ CONFIG ERROR: Missing environment variables: {', '.join(missing)}")
    print("Please set these variables in your environment or Render Dashboard!\n")
else:
    print("✅ Configuration variables present.\n")

# Test 1: Raw SMTP Connection (Port 587 STARTTLS)
print("--------------------------------------------------------------------------")
print("2. TESTING RAW SMTP DISPATCH (smtp-relay.brevo.com:587):")
print("--------------------------------------------------------------------------")
msg = MIMEMultipart("alternative")
msg["Subject"] = "[EduMind Diagnostic] Direct Brevo SMTP Test"
msg["From"] = f"EduMind Security <{sender_email}>"
msg["To"] = test_recipient
msg.attach(MIMEText("<h3>EduMind Brevo Diagnostic Test</h3><p>Testing direct SMTP connection from backend environment.</p>", "html"))

try:
    print(f" -> Attempting socket connection to {smtp_server}:{smtp_port}...")
    with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
        server.set_debuglevel(1)
        print(" -> Connection established. Starting STARTTLS...")
        server.starttls()
        print(" -> TLS handshake successful. Logging in...")
        server.login(smtp_user, smtp_password)
        print(" -> Authentication successful! Sending test mail...")
        server.sendmail(sender_email, test_recipient, msg.as_string())
        print(f"✅ RAW SMTP SUCCESS: Test email dispatched to {test_recipient} via Port {smtp_port}!\n")
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ SMTP AUTH ERROR ({e.smtp_code}): {e.smtp_error.decode('utf-8', errors='ignore') if isinstance(e.smtp_error, bytes) else e.smtp_error}")
    print("   Reason: Invalid SMTP_USER or SMTP_PASSWORD (Brevo Master SMTP Key).\n")
except Exception as e:
    print(f"❌ SMTP CONNECTION ERROR ({type(e).__name__}): {e}\n")


# Test 2: Brevo REST API Dispatch (api.brevo.com)
print("--------------------------------------------------------------------------")
print("3. TESTING BREVO REST API DISPATCH (https://api.brevo.com/v3/smtp/email):")
print("--------------------------------------------------------------------------")

api_key = os.getenv("BREVO_API_KEY") or smtp_password
url = "https://api.brevo.com/v3/smtp/email"
headers = {
    "accept": "application/json",
    "api-key": api_key,
    "content-type": "application/json"
}
payload = {
    "sender": {"name": "EduMind Security", "email": sender_email},
    "to": [{"email": test_recipient}],
    "subject": "[EduMind Diagnostic] Direct Brevo REST API Test",
    "htmlContent": "<h3>EduMind Brevo REST API Test</h3><p>Testing fallback HTTP REST API dispatch.</p>"
}

try:
    print(f" -> Posting request to {url} with api-key header...")
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f" -> Response Status Code: {resp.status_code}")
    print(f" -> Response Content: {resp.text}")
    if resp.status_code in [200, 201, 202]:
        print(f"✅ BREVO REST API SUCCESS: Email dispatched to {test_recipient}!\n")
    else:
        print(f"❌ BREVO REST API FAILED: {resp.status_code} - {resp.text}\n")
except Exception as e:
    print(f"❌ BREVO REST API EXCEPTION ({type(e).__name__}): {e}\n")

print("==========================================================================")
