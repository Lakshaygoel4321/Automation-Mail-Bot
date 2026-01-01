"""
Email Sending Service
Handles SMTP email transmission
"""
import smtplib
from email.message import EmailMessage
from app.utils.validators import is_valid_email


def _safe_log(message: str, level: str = 'info'):
    """Safe logging that works both inside and outside app context"""
    try:
        from flask import current_app
        if level == 'error':
            current_app.logger.error(message)
        else:
            current_app.logger.info(message)
    except RuntimeError:
        # Outside app context, use print
        emoji = "❌" if level == 'error' else "✅"
        print(f"{emoji} {message}")


class EmailService:
    """
    Manages email sending via SMTP
    """
    
    def send_email(self, subject: str, body: str, recipient_email: str) -> bool:
        """
        Send email via SMTP
        
        Args:
            subject: Email subject
            body: Email body content
            recipient_email: Recipient email address
            
        Returns:
            True if successful, raises exception otherwise
        """
        import os
        
        # Get configuration from environment
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_pass = os.environ.get('SMTP_PASSWORD')
        
        if not smtp_user or not smtp_pass:
            raise RuntimeError("SMTP_USER and SMTP_PASSWORD must be set in environment")
        
        # Validate emails
        if not is_valid_email(smtp_user):
            raise ValueError(f"Invalid sender email: {smtp_user}")
        
        if not is_valid_email(recipient_email):
            raise ValueError(f"Invalid recipient email: {recipient_email}")
        
        # Create email message
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = recipient_email
        msg.set_content(body)
        
        # Send email
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_user, smtp_pass)
                smtp.send_message(msg)
            
            _safe_log(f"Email sent successfully to {recipient_email}")
            return True
        
        except smtplib.SMTPAuthenticationError as e:
            _safe_log(f"SMTP authentication failed: {e}", 'error')
            raise RuntimeError("Email authentication failed. Please check SMTP credentials.")
        
        except smtplib.SMTPException as e:
            _safe_log(f"SMTP error: {e}", 'error')
            raise RuntimeError(f"Failed to send email: {str(e)}")
        
        except Exception as e:
            _safe_log(f"Unexpected error sending email: {e}", 'error')
            raise RuntimeError(f"Unexpected error: {str(e)}")


# Global email service instance
email_service = EmailService()
