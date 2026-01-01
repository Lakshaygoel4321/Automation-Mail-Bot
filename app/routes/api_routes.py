"""
API Routes
Handles all API endpoints for email generation
"""
from flask import Blueprint, request, jsonify, current_app
from app.services.llm_service import llm_service
from app.services.email_service import email_service
from app.services.session_service import session_service
from app.models.state import EmailContent
from app.utils.validators import (
    validate_topic, 
    validate_feedback, 
    is_valid_email,
    require_json
)
from app.utils.helpers import format_error_response, format_success_response

api_bp = Blueprint('api', __name__)


@api_bp.route('/generate', methods=['POST'])
@require_json('topic')
def generate_draft():
    """
    Generate initial email draft
    
    Request JSON:
        {
            "topic": "Email topic or purpose"
        }
    
    Response JSON:
        {
            "success": true,
            "session_id": "uuid",
            "content": "generated email content"
        }
    """
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        # Validate topic
        is_valid, error_msg = validate_topic(topic)
        if not is_valid:
            return format_error_response(error_msg)
        
        # Generate email content
        generated_content = llm_service.generate_email(topic)
        
        # Create session
        session = session_service.create_session(topic, generated_content)
        
        return jsonify(format_success_response({
            'session_id': session.session_id,
            'content': generated_content
        }))
    
    except Exception as e:
        current_app.logger.error(f"Error in generate_draft: {e}", exc_info=True)
        return format_error_response(str(e), 500)


@api_bp.route('/feedback', methods=['POST'])
@require_json('session_id', 'feedback')
def process_feedback():
    """
    Process user feedback and regenerate email
    
    Request JSON:
        {
            "session_id": "uuid",
            "feedback": "user feedback text"
        }
    
    Response JSON:
        {
            "success": true,
            "content": "updated email content",
            "feedback_history": ["feedback1", "feedback2"]
        }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        feedback = data.get('feedback', '').strip()
        
        # Get session
        session = session_service.get_session(session_id)
        if not session:
            return format_error_response('Invalid or expired session')
        
        # Validate feedback
        if feedback:
            is_valid, error_msg = validate_feedback(feedback)
            if not is_valid:
                return format_error_response(error_msg)
            
            # Add feedback to history
            session_service.add_feedback(session_id, feedback)
        
        # Regenerate content with feedback
        all_feedback = ' | '.join(session.feedback_history)
        new_content = llm_service.generate_email(
            session.topic,
            all_feedback,
            session.generated_content
        )
        
        # Update session
        session_service.update_session(session_id, generated_content=new_content)
        
        return jsonify(format_success_response({
            'content': new_content,
            'feedback_history': session.feedback_history
        }))
    
    except Exception as e:
        current_app.logger.error(f"Error in process_feedback: {e}", exc_info=True)
        return format_error_response(str(e), 500)


@api_bp.route('/finalize', methods=['POST'])
@require_json('session_id')
def finalize_draft():
    """
    Finalize email draft
    
    Request JSON:
        {
            "session_id": "uuid"
        }
    
    Response JSON:
        {
            "success": true,
            "final_content": "finalized email content"
        }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        # Get session
        session = session_service.get_session(session_id)
        if not session:
            return format_error_response('Invalid or expired session')
        
        # Finalize content
        session_service.update_session(
            session_id,
            final_data=session.generated_content
        )
        
        return jsonify(format_success_response({
            'final_content': session.final_data
        }))
    
    except Exception as e:
        current_app.logger.error(f"Error in finalize_draft: {e}", exc_info=True)
        return format_error_response(str(e), 500)


@api_bp.route('/send-email', methods=['POST'])
@require_json('session_id', 'email')
def send_email():
    """
    Send finalized email to recipient
    
    Request JSON:
        {
            "session_id": "uuid",
            "email": "recipient@example.com"
        }
    
    Response JSON:
        {
            "success": true,
            "message": "Email sent successfully to recipient@example.com"
        }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        recipient_email = data.get('email', '').strip()
        
        # Validate email
        if not is_valid_email(recipient_email):
            return format_error_response('Invalid email format')
        
        # Get session
        session = session_service.get_session(session_id)
        if not session:
            return format_error_response('Invalid or expired session')
        
        if not session.final_data:
            return format_error_response('Email must be finalized before sending')
        
        # Parse email content
        email_content = EmailContent.parse_from_content(
            session.final_data,
            session.topic
        )
        
        # Send email
        email_service.send_email(
            email_content.subject,
            email_content.body,
            recipient_email
        )
        
        # Update session
        session_service.update_session(session_id, receiver_mail=recipient_email)
        
        return jsonify(format_success_response(
            {},
            f'Email sent successfully to {recipient_email}'
        ))
    
    except ValueError as e:
        return format_error_response(str(e))
    except RuntimeError as e:
        return format_error_response(str(e), 500)
    except Exception as e:
        current_app.logger.error(f"Error in send_email: {e}", exc_info=True)
        return format_error_response(f'Failed to send email: {str(e)}', 500)


@api_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """
    Retrieve session information
    
    Response JSON:
        {
            "session_id": "uuid",
            "topic": "email topic",
            "generated_content": "content",
            "feedback_history": [],
            "final_data": "",
            "receiver_mail": ""
        }
    """
    try:
        session = session_service.get_session(session_id)
        
        if not session:
            return format_error_response('Session not found', 404)
        
        return jsonify(session.to_dict())
    
    except Exception as e:
        current_app.logger.error(f"Error in get_session: {e}", exc_info=True)
        return format_error_response(str(e), 500)
