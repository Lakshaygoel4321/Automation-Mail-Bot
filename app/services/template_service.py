"""
Template Email Generation Service
Fallback email generation using predefined templates
"""
from typing import Dict


class TemplateService:
    """
    Generates emails using predefined templates
    Used as fallback when LLM is unavailable
    """
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate_email(self, topic: str, feedback: str = "") -> str:
        """
        Generate email from templates
        
        Args:
            topic: Email topic
            feedback: User feedback for modifications
            
        Returns:
            Generated email content
        """
        topic_lower = topic.lower()
        
        # Determine template type
        template_key = self._determine_template_type(topic_lower)
        template = self.templates.get(template_key, self.templates['general'])
        
        # Generate email from template
        email_content = template.format(topic=topic)
        
        # Apply feedback modifications
        if feedback:
            email_content = self._apply_feedback(email_content, feedback, topic)
        
        print(f"✅ Generated template email: {template_key}")
        return email_content
    
    def _determine_template_type(self, topic_lower: str) -> str:
        """Determine which template to use based on topic"""
        template_keywords = {
            'meeting': ['meeting', 'schedule', 'appointment', 'call'],
            'followup': ['follow up', 'followup', 'update', 'status'],
            'request': ['request', 'help', 'support', 'assistance'],
            'thank': ['thank', 'appreciation', 'gratitude'],
            'invitation': ['invitation', 'invite', 'event', 'join'],
            'proposal': ['proposal', 'suggestion', 'idea', 'plan']
        }
        
        for template_key, keywords in template_keywords.items():
            if any(keyword in topic_lower for keyword in keywords):
                return template_key
        
        return 'general'
    
    def _apply_feedback(self, email_content: str, feedback: str, topic: str) -> str:
        """Apply feedback modifications to email"""
        feedback_lower = feedback.lower()
        
        # Make email more concise
        if any(word in feedback_lower for word in ['shorter', 'brief', 'concise']):
            email_content = self._make_concise(topic)
        
        # Make more formal
        if any(word in feedback_lower for word in ['formal', 'professional']):
            email_content = email_content.replace('Hi', 'Dear')
            email_content = email_content.replace("Hope you're doing well", 
                                                 'I trust this email finds you in good health')
            email_content = email_content.replace('Best regards', 'Sincerely')
            email_content = email_content.replace('Thanks', 'Thank you')
        
        # Make more casual
        if any(word in feedback_lower for word in ['casual', 'friendly']):
            email_content = email_content.replace('Dear [Recipient]', 'Hi [Recipient]')
            email_content = email_content.replace('Sincerely', 'Best')
            email_content = email_content.replace('I trust this email finds you in good health',
                                                 "Hope you're doing great")
        
        # Mark as urgent
        if any(word in feedback_lower for word in ['urgent', 'important']):
            email_content = email_content.replace('Subject:', 'Subject: [URGENT]')
            email_content = email_content.replace('I hope', 'I urgently need to discuss')
        
        # Add more detail
        if any(word in feedback_lower for word in ['detail', 'elaborate']):
            email_content += """\n\nAdditional Context:
This matter requires careful consideration and I believe your input would be valuable in moving forward effectively.

I'm happy to provide any additional information you might need to help with this request."""
        
        return email_content
    
    def _make_concise(self, topic: str) -> str:
        """Generate concise email version"""
        return f"""Subject: {topic}

Dear [Recipient],

I hope you're well.

I'm writing regarding {topic}. This is an important matter that I'd like to discuss with you.

Please let me know when you're available to connect.

Best regards,
[Your Name]"""
    
    def _load_templates(self) -> Dict[str, str]:
        """Load email templates"""
        return {
            'meeting': """Subject: Meeting Request - {topic}

Dear [Recipient],

I hope this email finds you well.

I would like to schedule a meeting to discuss {topic}. This meeting will help us align on key objectives and ensure we're moving forward effectively.

Proposed Details:
- Purpose: {topic}
- Duration: 30-60 minutes
- Format: In-person/Virtual (as per your preference)

Please let me know your availability for the coming week, and I'll send out a calendar invitation accordingly.

Looking forward to our discussion.

Best regards,
[Your Name]""",
            
            'followup': """Subject: Follow-up on {topic}

Hi [Recipient],

I hope you're doing well.

I'm following up on {topic} to check on the current status and see if there are any updates or next steps we need to address.

If you need any additional information or support from my end, please don't hesitate to let me know.

Thank you for your time, and I look forward to hearing from you soon.

Best regards,
[Your Name]""",
            
            'request': """Subject: Request for Assistance - {topic}

Dear [Recipient],

I hope this message finds you well.

I'm reaching out to request your assistance with {topic}. Your expertise and support would be invaluable in helping us move forward with this matter.

Could you please let me know if you're available to help with this, and what would be the best way to proceed?

I appreciate your time and consideration.

Thank you,
[Your Name]""",
            
            'thank': """Subject: Thank You - {topic}

Dear [Recipient],

I wanted to take a moment to express my sincere gratitude regarding {topic}.

Your support and contribution have been invaluable, and I truly appreciate the time and effort you've invested in this matter.

Thank you once again for your excellent work and collaboration.

Warm regards,
[Your Name]""",
            
            'invitation': """Subject: Invitation - {topic}

Dear [Recipient],

I hope this email finds you in good health and spirits.

I would like to extend an invitation to you for {topic}. This will be a great opportunity for us to connect and collaborate.

Event Details:
- Event: {topic}
- Date: [Date]
- Time: [Time]
- Location: [Location/Virtual Link]

Please let me know if you'll be able to attend so we can make the necessary arrangements.

Looking forward to seeing you there.

Best regards,
[Your Name]""",
            
            'proposal': """Subject: Proposal for Your Consideration - {topic}

Dear [Recipient],

I hope you're having a great day.

I'm writing to present a proposal regarding {topic} for your consideration. I believe this initiative could bring significant value and benefits.

Key Points:
- Objective: {topic}
- Expected Benefits: Improved efficiency and positive outcomes
- Next Steps: I'd welcome the opportunity to discuss this further

Would you be available for a brief meeting to explore this proposal in more detail?

Thank you for your time and consideration.

Sincerely,
[Your Name]""",
            
            'general': """Subject: Regarding {topic}

Dear [Recipient],

I hope this email finds you well.

I'm writing to you about {topic}. I wanted to reach out and share some thoughts on this matter that I believe would be valuable for our ongoing collaboration.

This is an important topic that deserves our attention, and I'd appreciate the opportunity to discuss it further with you.

Please let me know when would be a convenient time for you to connect, either via email or a brief call.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
        }


# Global template service instance
template_service = TemplateService()
