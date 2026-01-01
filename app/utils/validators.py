"""
Validation Utilities
Input validation and sanitization functions
"""
import re
from functools import wraps
from flask import request, jsonify


def is_valid_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_topic(topic: str) -> tuple[bool, str]:
    """
    Validate email topic
    
    Args:
        topic: Topic string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic or not isinstance(topic, str):
        return False, "Topic is required"
    
    topic = topic.strip()
    
    if len(topic) < 3:
        return False, "Topic must be at least 3 characters"
    
    if len(topic) > 500:
        return False, "Topic must not exceed 500 characters"
    
    return True, ""


def validate_feedback(feedback: str) -> tuple[bool, str]:
    """
    Validate feedback content
    
    Args:
        feedback: Feedback string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not feedback or not isinstance(feedback, str):
        return False, "Feedback is required"
    
    feedback = feedback.strip()
    
    if len(feedback) > 1000:
        return False, "Feedback must not exceed 1000 characters"
    
    return True, ""


def require_json(*required_fields):
    """
    Decorator to validate required JSON fields in request
    
    Usage:
        @require_json('topic', 'email')
        def my_route():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
