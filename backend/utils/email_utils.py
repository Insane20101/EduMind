import os
import logging
import smtplib
import socket
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def send_smtp_otp_email(to_email: str, student_name: str, otp_code: str, context: str = "password_reset") -> bool:
    """
    Sends OTP email using standard SMTP (Brevo/Gmail/Custom) with automatic Brevo REST API fallback.
    Returns True ONLY after delivery handoff succeeds.
    """
    smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
    smtp_password = raw_pass.replace(" ", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com").strip()
    
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    from_email = os.getenv("SENDER_EMAIL") or os.getenv("SMTP_FROM_EMAIL") or smtp_user or "akr20101@gmail.com"

    if context == "signup":
        badge_text = "Account Verification Request"
        subject_line = f"[{otp_code}] EduMind Account Verification Code"
        intro_text = "Welcome to EduMind! Please enter the 6-digit verification code below to verify your email address and complete registration:"
    else:
        badge_text = "Password Reset Request"
        subject_line = f"[{otp_code}] EduMind Password Reset Security Code"
        intro_text = "We received a request to reset the password for your EduMind student account. Enter the 6-digit verification code below to proceed:"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; color: #0f172a; }}
            .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 32px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
            .logo {{ font-size: 22px; font-weight: 800; color: #2563eb; letter-spacing: -0.5px; margin-bottom: 24px; text-align: center; }}
            .title {{ font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }}
            .text {{ font-size: 14px; color: #475569; line-height: 1.6; margin-bottom: 24px; }}
            .otp-box {{ background: #f1f5f9; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0; }}
            .otp-code {{ font-size: 34px; font-weight: 800; letter-spacing: 8px; color: #2563eb; font-family: monospace; }}
            .badge {{ display: inline-block; padding: 4px 12px; background: #dbeafe; color: #1e40af; border-radius: 9999px; font-size: 12px; font-weight: 600; margin-bottom: 16px; }}
            .footer {{ font-size: 11px; color: #94a3b8; text-align: center; margin-top: 32px; border-top: 1px solid #f1f5f9; padding-top: 16px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🎓 EduMind AI Platform</div>
            <div style="text-align: center;"><span class="badge">{badge_text}</span></div>
            <div class="title">Verify Your Security Code</div>
            <div class="text">
                Hello <strong>{student_name}</strong>,<br>
                {intro_text}
            </div>
            <div class="otp-box">
                <div class="otp-code">{otp_code}</div>
            </div>
            <div class="text">
                This verification code will expire in <strong>10 minutes</strong>. If you did not initiate this request, your account remains secure and no action is required.
            </div>
            <div class="footer">
                &copy; 2026 EduMind University Learning Ecosystem. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """

    # Check credentials
    if not smtp_user or not smtp_password:
        logger.error("[SMTP CONFIG ERROR] Missing SMTP_USER or SMTP_PASSWORD environment variables.")
        return False

    # 1. Attempt Raw SMTP (Port 587 STARTTLS)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject_line
    msg["From"] = f"EduMind Security <{from_email}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        logger.info(f"[SMTP] Connecting to {smtp_server}:{smtp_port} with user {smtp_user}...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            logger.info("[SMTP] TLS established. Authenticating...")
            server.login(smtp_user, smtp_password)
            logger.info("[SMTP] Authentication successful. Sending mail...")
            server.sendmail(from_email, to_email, msg.as_string())
            logger.info(f"[SMTP SUCCESS] Dispatched OTP email to {to_email} via Port {smtp_port}")
            return True

    except smtplib.SMTPAuthenticationError as e_auth:
        logger.error(f"[SMTP AUTH ERROR] Code {e_auth.smtp_code}: {e_auth.smtp_error} - Check SMTP_USER / SMTP_PASSWORD.")
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, socket.timeout, TimeoutError, OSError) as e_conn:
        logger.warning(f"[SMTP CONNECT ERROR] TLS Port {smtp_port} error ({type(e_conn).__name__}): {e_conn}. Trying SSL 465...")
        try:
            with smtplib.SMTP_SSL(smtp_server, 465, timeout=10) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_email, msg.as_string())
                logger.info(f"[SMTP SUCCESS] Dispatched OTP email to {to_email} via SSL Port 465")
                return True
        except Exception as e_ssl:
            logger.error(f"[SMTP SSL ERROR] SSL Port 465 failed: {e_ssl}")

    except Exception as e_gen:
        logger.error(f"[SMTP GENERAL ERROR] Raw SMTP dispatch failed ({type(e_gen).__name__}): {e_gen}")

    # 2. Brevo Transactional REST API Fallback (Port 443 HTTPS — Immune to Port Blocking)
    api_key = os.getenv("BREVO_API_KEY") or smtp_password
    if api_key:
        logger.info("[BREVO REST API] Attempting fallback HTTP REST API dispatch (https://api.brevo.com/v3/smtp/email)...")
        try:
            url = "https://api.brevo.com/v3/smtp/email"
            headers = {
                "accept": "application/json",
                "api-key": api_key,
                "content-type": "application/json"
            }
            payload = {
                "sender": {"name": "EduMind Security", "email": from_email},
                "to": [{"email": to_email}],
                "subject": subject_line,
                "htmlContent": html_content
            }
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            if res.status_code in [200, 201, 202]:
                logger.info(f"[BREVO REST API SUCCESS] Dispatched OTP email to {to_email} (Status {res.status_code})")
                return True
            else:
                logger.error(f"[BREVO REST API ERROR] Status {res.status_code}: {res.text}")
        except Exception as e_api:
            logger.error(f"[BREVO REST API EXCEPTION] REST API fallback failed: {e_api}")

    return False


def test_smtp_connection(to_email: str) -> dict:
    """
    Diagnostic tool to test Brevo/Gmail SMTP & REST API connectivity and return non-sensitive status.
    """
    smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
    smtp_password = raw_pass.replace(" ", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com").strip()
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    from_email = os.getenv("SENDER_EMAIL") or os.getenv("SMTP_FROM_EMAIL") or smtp_user or "akr20101@gmail.com"

    diagnostics = {
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "smtp_user": smtp_user,
        "from_email": from_email,
        "recipient": to_email,
        "has_password": bool(smtp_password)
    }

    if not smtp_user:
        diagnostics["error"] = "SMTP_USER environment variable missing."
        return diagnostics
    if not smtp_password:
        diagnostics["error"] = "SMTP_PASSWORD environment variable missing."
        return diagnostics

    # 1. Test Raw SMTP
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "[EduMind Test] Live Diagnostics"
        msg["From"] = f"EduMind Security <{from_email}>"
        msg["To"] = to_email
        msg.attach(MIMEText("<p>Diagnostic email test.</p>", "html"))

        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        diagnostics["success"] = True
        diagnostics["method"] = f"Raw SMTP TLS Port {smtp_port}"
        return diagnostics
    except Exception as e:
        diagnostics["smtp_error"] = f"{type(e).__name__}: {str(e)}"

    # 2. Test Brevo REST API
    api_key = os.getenv("BREVO_API_KEY") or smtp_password
    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }
        payload = {
            "sender": {"name": "EduMind Security", "email": from_email},
            "to": [{"email": to_email}],
            "subject": "[EduMind Test] Live REST API Diagnostics",
            "htmlContent": "<p>Diagnostic REST API test.</p>"
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201, 202]:
            diagnostics["success"] = True
            diagnostics["method"] = f"Brevo REST API (HTTP {res.status_code})"
            return diagnostics
        else:
            diagnostics["api_error"] = f"Status {res.status_code}: {res.text}"
    except Exception as e_api:
        diagnostics["api_error"] = f"{type(e_api).__name__}: {str(e_api)}"

    diagnostics["success"] = False
    return diagnostics
