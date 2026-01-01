"""
Helper Utilities
Miscellaneous utility functions
"""
import uuid
from datetime import datetime, timedelta


def generate_session_id() -> str:
    """Generate unique session ID"""
    return str(uuid.uuid4())


def is_session_expired(created_at: datetime, timeout_seconds: int) -> bool:
    """
    Check if session has expired
    
    Args:
        created_at: Session creation timestamp
        timeout_seconds: Timeout duration in seconds
        
    Returns:
        True if expired, False otherwise
    """
    expiry_time = created_at + timedelta(seconds=timeout_seconds)
    return datetime.utcnow() > expiry_time


def sanitize_email_content(content: str) -> str:
    """
    Sanitize email content (remove potentially harmful content)
    
    Args:
        content: Email content to sanitize
        
    Returns:
        Sanitized content
    """
    # Basic sanitization - expand as needed
    sanitized = content.strip()
    
    # Remove any script tags (basic protection)
    sanitized = sanitized.replace('<script>', '').replace('</script>', '')
    
    return sanitized


def format_error_response(error_message: str, status_code: int = 400) -> tuple:
    """
    Format error response consistently
    
    Args:
        error_message: Error message
        status_code: HTTP status code
        
    Returns:
        Tuple of (response_dict, status_code)
    """
    return {'error': error_message, 'success': False}, status_code


def format_success_response(data: dict, message: str = None) -> dict:
    """
    Format success response consistently
    
    Args:
        data: Response data
        message: Optional success message
        
    Returns:
        Formatted response dictionary
    """
    response = {'success': True, **data}
    if message:
        response['message'] = message
    return response
