import logging
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails."""

    @staticmethod
    async def send_otp_email(email: str, otp_code: str, username: str) -> bool:
        
        # Send OTP email to the user.
        try:
            subject = "Library Management System - Email Verification"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2>Email Verification</h2>
                        <p>Hi {username},</p>
                        <p>Your One-Time Password (OTP) for email verification is:</p>
                        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
                            <h3 style="letter-spacing: 2px; color: #333;">{otp_code}</h3>
                        </div>
                        <p>This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
                        <p>If you didn't request this verification, please ignore this email.</p>
                        <hr>
                        <p style="color: #999; font-size: 12px;">
                            Library Management System<br>
                            This is an automated email, please do not reply.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            text_body = f"""
            Email Verification
            
            Hi {username},
            
            Your One-Time Password (OTP) for email verification is:
            
            {otp_code}
            
            This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.
            
            If you didn't request this verification, please ignore this email.
            
            Library Management System
            """
            
            logger.info(f"Sending OTP email to {email} (Code: {otp_code})")
            
            # Call actual SMTP sending
            return await EmailService._send_smtp(email, subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Failed to send OTP email to {email}: {str(e)}")
            return False

    @staticmethod
    async def send_approval_email(email: str, username: str, is_approved: bool, 
                                  rejection_reason: str | None = None) -> bool:
       
        # Send approval/rejection email
        try:
            if is_approved:
                subject = "Library Management System - Account Approved"
                status_msg = "Your account has been approved!"
                action_msg = "You can now log in to the library management system."
            else:
                subject = "Library Management System - Account Pending Review"
                status_msg = "Your account is still pending admin approval."
                action_msg = f"Reason: {rejection_reason or 'Administrator review required.'}"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2>Account Status</h2>
                        <p>Hi {username},</p>
                        <p>{status_msg}</p>
                        <p>{action_msg}</p>
                        <hr>
                        <p style="color: #999; font-size: 12px;">
                            Library Management System<br>
                            This is an automated email, please do not reply.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            text_body = f"""
            Account Status
            
            Hi {username},
            
            {status_msg}
            
            {action_msg}
            
            Library Management System
            """
            
            logger.info(f"Sending status update email to {email} (Approved: {is_approved})")
            return await EmailService._send_smtp(email, subject, text_body, html_body)
            
        except Exception as e:
            logger.error(f"Failed to send approval email to {email}: {str(e)}")
            return False

    @staticmethod
    def _send_smtp_blocking(to_email: str, subject: str, text_body: str, html_body: str) -> bool:
        """Synchronous/blocking SMTP sending function run in a separate thread."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg["To"] = to_email
            
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Select connection type based on port
            if settings.SMTP_PORT == 465:
                server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10)
            else:
                server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10)
                # Call starttls for port 587 (or similar TLS ports)
                if settings.SMTP_PORT == 587:
                    server.starttls()
            
            with server:
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"SMTP Error while sending to {to_email}: {str(e)}")
            return False

    @staticmethod
    async def _send_smtp(to_email: str, subject: str, text_body: str, html_body: str) -> bool:
        """Send email via SMTP (non-blocking async wrapper)."""
        return await asyncio.to_thread(
            EmailService._send_smtp_blocking,
            to_email,
            subject,
            text_body,
            html_body
        )
