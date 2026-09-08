import os
import logging
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def send_smtp_otp_email(to_email: str, student_name: str, otp_code: str, context: str = "password_reset") -> bool:
    """
    Sends OTP email using standard Gmail SMTP (smtp.gmail.com:587, STARTTLS).
    Returns True ONLY after sendmail succeeds.
    """
    smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
    # Automatically strip any spaces if Google App Password was copied as 'abcd efgh ijkl mnop'
    smtp_password = raw_pass.replace(" ", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    if not smtp_user or not smtp_password:
        logger.error("[SMTP] Failed: SMTP_USER or SMTP_PASSWORD environment variable is missing.")
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

    try:
        logger.info(f"[SMTP] Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=12) as server:
            server.starttls()
            logger.info("[SMTP] TLS established successfully.")
            server.login(smtp_user, smtp_password)
            logger.info("[SMTP] Authentication successful.")
            server.sendmail(smtp_user, to_email, msg.as_string())
            logger.info(f"[SMTP] OTP email sent successfully to {to_email} ({context}) via port {smtp_port}")
            return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"[SMTP] Authentication failed: {e.smtp_code} - Bad username/App Password.")
        # Attempt fallback to SSL port 465 if TLS failed due to socket issues
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, socket.timeout, TimeoutError, OSError) as e_conn:
        logger.warning(f"[SMTP] TLS Port {smtp_port} connection issue: {e_conn}. Trying SSL port 465 fallback...")
        try:
            with smtplib.SMTP_SSL(smtp_server, 465, timeout=12) as server:
                server.login(smtp_user, smtp_password)
                logger.info("[SMTP] Authentication successful via SSL port 465.")
                server.sendmail(smtp_user, to_email, msg.as_string())
                logger.info(f"[SMTP] OTP email sent successfully to {to_email} ({context}) via SSL port 465")
                return True
        except Exception as e_ssl:
            logger.error(f"[SMTP] Email dispatch failed via SSL port 465: {e_ssl}")
            return False
    except smtplib.SMTPException as e:
        logger.error(f"[SMTP] Email sending failed: {e}")
        return False
    except Exception as e:
        logger.error(f"[SMTP] Unexpected error during email dispatch: {e}")
        return False

    return False


def test_smtp_connection(to_email: str) -> dict:
    """
    Diagnostic tool to test Gmail SMTP connectivity and return non-sensitive status.
    """
    smtp_user = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
    smtp_password = raw_pass.replace(" ", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    if not smtp_user:
        return {"success": False, "error": "SMTP_USER environment variable missing."}
    if not smtp_password:
        return {"success": False, "error": "SMTP_PASSWORD environment variable missing."}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[EduMind Test] Live SMTP Diagnostics Test"
    msg["From"] = f"EduMind Security <{smtp_user}>"
    msg["To"] = to_email
    msg.attach(MIMEText("<p>This is a live test email from EduMind backend SMTP diagnostic module.</p>", "html"))

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
    except Exception as e_tls:
        tls_err = str(e_tls)

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
    except Exception as e_ssl:
        ssl_err = str(e_ssl)

    return {
        "success": False,
        "smtp_user": smtp_user,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "tls_error": tls_err,
        "ssl_error": ssl_err
    }
