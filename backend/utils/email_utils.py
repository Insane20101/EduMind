import os
import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_smtp_otp_email(to_email: str, student_name: str, otp_code: str, context: str = "password_reset") -> bool:

    """
    Sends OTP email using standard SMTP (e.g. Gmail App Password) without requiring custom DNS domain setup.
    """
    smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
    # Remove any spaces automatically if user copied Google App Password format (e.g. 'abcd efgh ijkl mnop')
    smtp_password = raw_pass.replace(" ", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    if not smtp_user or not smtp_password:
        logger.warning("[SMTP EMAIL] SMTP_USER or SMTP_PASSWORD missing.")
        return False

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

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject_line
    msg["From"] = f"EduMind Security <{smtp_user}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    # Try STARTTLS on specified port (default 587)
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=12) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
        logger.info(f"[SMTP EMAIL SUCCESS] Dispatched OTP code ({context}) to {to_email} via TLS port {smtp_port}")
        return True
    except Exception as e_tls:
        logger.warning(f"[SMTP TLS FAILED] Port {smtp_port} failed: {e_tls}. Retrying via SSL port 465...")
        # Fallback to SSL on port 465
        try:
            with smtplib.SMTP_SSL(smtp_server, 465, timeout=12) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, to_email, msg.as_string())
            logger.info(f"[SMTP EMAIL SUCCESS] Dispatched OTP code ({context}) to {to_email} via SSL port 465")
            return True
        except Exception as e_ssl:
            logger.error(f"[SMTP EMAIL FAILED] Failed via TLS ({e_tls}) and SSL ({e_ssl})")
            return False


def send_resend_otp_email(to_email: str, student_name: str, otp_code: str, context: str = "password_reset") -> bool:
    """
    Sends a beautifully formatted HTML OTP email using Gmail SMTP or Resend REST API.
    """
    # 1. Try Gmail SMTP first if configured (No DNS required!)
    if os.getenv("SMTP_USER") and os.getenv("SMTP_PASSWORD"):
        if send_smtp_otp_email(to_email, student_name, otp_code, context):
            return True

    # 2. Fallback to Resend REST API
    raw_key = os.getenv("RESEND_API_KEY") or RESEND_API_KEY or ""
    resend_key = raw_key.strip().strip('"').strip("'")
    if not resend_key:
        logger.warning("[RESEND EMAIL] RESEND_API_KEY not configured in environment.")
        return False

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {resend_key}",
        "Content-Type": "application/json"
    }

    from_email = os.getenv("RESEND_FROM_EMAIL", "EduMind Security <onboarding@resend.dev>")

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

    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": subject_line,
        "html": html_content
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code in [200, 201]:
            logger.info(f"[RESEND EMAIL SUCCESS] Dispatched OTP code ({context}) to {to_email}")
            return True
        else:
            logger.error(f"[RESEND EMAIL FAILED] Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"[RESEND EMAIL EXCEPTION] Failed to dispatch via Resend: {e}")
        return False


def test_smtp_connection(to_email: str) -> dict:
    smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
    smtp_password = raw_pass.replace(" ", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    if not smtp_user:
        return {"success": False, "error": "SMTP_USER environment variable missing in Render dashboard."}
    if not smtp_password:
        return {"success": False, "error": "SMTP_PASSWORD environment variable missing in Render dashboard."}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[EduMind Test] Live SMTP Diagnostics Test"
    msg["From"] = f"EduMind Security <{smtp_user}>"
    msg["To"] = to_email
    msg.attach(MIMEText("<p>This is a live test email from EduMind backend SMTP diagnostic module.</p>", "html"))

    tls_err = None
    ssl_err = None

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
        return {
            "success": True,
            "method": f"TLS Port {smtp_port}",
            "smtp_user": smtp_user,
            "smtp_server": smtp_server,
            "recipient": to_email
        }
    except Exception as e:
        tls_err = str(e)

    try:
        with smtplib.SMTP_SSL(smtp_server, 465, timeout=10) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
        return {
            "success": True,
            "method": "SSL Port 465",
            "smtp_user": smtp_user,
            "smtp_server": smtp_server,
            "recipient": to_email
        }
    except Exception as e:
        ssl_err = str(e)

    return {
        "success": False,
        "smtp_user": smtp_user,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "tls_error": tls_err,
        "ssl_error": ssl_err
    }


