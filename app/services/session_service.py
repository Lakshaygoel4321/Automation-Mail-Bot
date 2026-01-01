"""
Session Management Service
Handles email session creation, storage, and retrieval
"""
from datetime import datetime
from typing import Optional, Dict
from app.models.state import EmailSession
from app.utils.helpers import generate_session_id, is_session_expired


def _safe_log(message: str):
    """Safe logging that works both inside and outside app context"""
    try:
        from flask import current_app
        current_app.logger.info(message)
    except RuntimeError:
        # Outside app context, use print
        print(f"ℹ️  {message}")


class SessionService:
    """
    Manages email generation sessions
    
    Note: Currently using in-memory storage.
    For production, replace with Redis or database.
    """
    
    def __init__(self):
        self._sessions: Dict[str, EmailSession] = {}
    
    def create_session(self, topic: str, generated_content: str) -> EmailSession:
        """
        Create new email session
        
        Args:
            topic: Email topic
            generated_content: Initial generated content
            
        Returns:
            EmailSession object
        """
        session_id = generate_session_id()
        
        session = EmailSession(
            session_id=session_id,
            topic=topic,
            generated_content=generated_content,
            feedback_history=[],
            final_data='',
            receiver_mail='',
            created_at=datetime.utcnow()
        )
        
        self._sessions[session_id] = session
        _safe_log(f"Created session: {session_id}")
        
        return session
    
    def get_session(self, session_id: str) -> Optional[EmailSession]:
        """
        Retrieve session by ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            EmailSession if found, None otherwise
        """
        session = self._sessions.get(session_id)
        
        if session:
            # Check if session expired
            try:
                from flask import current_app
                timeout = current_app.config.get('SESSION_TIMEOUT', 3600)
            except RuntimeError:
                timeout = 3600  # Default timeout
            
            if is_session_expired(session.created_at, timeout):
                self.delete_session(session_id)
                return None
        
        return session
    
    def update_session(self, session_id: str, **kwargs) -> Optional[EmailSession]:
        """
        Update session attributes
        
        Args:
            session_id: Session identifier
            **kwargs: Attributes to update
            
        Returns:
            Updated EmailSession if found, None otherwise
        """
        session = self.get_session(session_id)
        
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            
            _safe_log(f"Updated session: {session_id}")
        
        return session
    
    def add_feedback(self, session_id: str, feedback: str) -> Optional[EmailSession]:
        """
        Add feedback to session history
        
        Args:
            session_id: Session identifier
            feedback: Feedback text
            
        Returns:
            Updated EmailSession if found, None otherwise
        """
        session = self.get_session(session_id)
        
        if session:
            session.feedback_history.append(feedback)
            _safe_log(f"Added feedback to session: {session_id}")
        
        return session
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete session
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            _safe_log(f"Deleted session: {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions from storage"""
        try:
            from flask import current_app
            timeout = current_app.config.get('SESSION_TIMEOUT', 3600)
        except RuntimeError:
            timeout = 3600
        
        expired_sessions = [
            sid for sid, session in self._sessions.items()
            if is_session_expired(session.created_at, timeout)
        ]
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        if expired_sessions:
            _safe_log(f"Cleaned up {len(expired_sessions)} expired sessions")


# Global session service instance
session_service = SessionService()
