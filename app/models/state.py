"""
Data Models and Type Definitions
Defines data structures used across the application
"""
from typing import TypedDict, List
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage
from dataclasses import dataclass
from datetime import datetime


class AgentState(TypedDict):
    """LangGraph agent state definition (for future use)"""
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    final_data: str
    topic: str
    feedback: str
    receiver_mail: str
    generated_content: str


@dataclass
class EmailSession:
    """Email session data structure"""
    session_id: str
    topic: str
    generated_content: str
    feedback_history: List[str]
    final_data: str
    receiver_mail: str
    created_at: datetime
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'session_id': self.session_id,
            'topic': self.topic,
            'generated_content': self.generated_content,
            'feedback_history': self.feedback_history,
            'final_data': self.final_data,
            'receiver_mail': self.receiver_mail,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class EmailContent:
    """Email content structure"""
    subject: str
    body: str
    
    @classmethod
    def parse_from_content(cls, content: str, topic: str):
        """Parse email content to extract subject and body"""
        if content.startswith('Subject:'):
            lines = content.split('\n', 2)
            subject = lines[0].replace('Subject:', '').strip()
            body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content
        else:
            subject = f"Email: {topic}"
            body = content
        
        return cls(subject=subject, body=body)
