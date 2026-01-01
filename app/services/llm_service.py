"""
LLM Service
Handles AI-powered email content generation using LangChain and Groq
"""
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os


class LLMService:
    """
    Manages LLM interactions for email generation
    """
    
    def __init__(self):
        self.llm = None
        self._initialized = False
    
    def _initialize_llm(self):
        """Initialize LLM with error handling (lazy initialization)"""
        if self._initialized:
            return
        
        try:
            api_key = os.environ.get('GROQ_API_KEY')
            model = os.environ.get('LLM_MODEL', 'llama-3.1-8b-instant')
            
            if api_key:
                self.llm = ChatGroq(
                    model=model,
                    groq_api_key=api_key
                )
                print(f"✅ LLM initialized successfully: {model}")
            else:
                print("⚠️  GROQ_API_KEY not set, using template fallback")
        except Exception as e:
            print(f"❌ Failed to initialize LLM: {e}")
            self.llm = None
        
        self._initialized = True
    
    def generate_email(self, topic: str, feedback: str = "", previous_content: str = "") -> str:
        """
        Generate email content using LLM or fallback to templates
        
        Args:
            topic: Email topic/purpose
            feedback: User feedback for refinement
            previous_content: Previous draft content
            
        Returns:
            Generated email content
        """
        # Lazy initialization
        if not self._initialized:
            self._initialize_llm()
        
        if self.llm is None:
            print("ℹ️  LLM not available, using template generation")
            from app.services.template_service import template_service
            return template_service.generate_email(topic, feedback)
        
        try:
            prompt = self._build_prompt()
            
            chat_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=prompt),
                HumanMessage(content=self._build_user_message(topic, feedback, previous_content))
            ])
            
            final_prompt = chat_prompt.format_messages()
            response = self.llm.invoke(final_prompt)
            
            content = response.content if hasattr(response, "content") else str(response)
            
            print(f"✅ Email generated successfully for topic: {topic[:50]}...")
            return content
        
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            from app.services.template_service import template_service
            return template_service.generate_email(topic, feedback)
    
    def _build_prompt(self) -> str:
        """Build system prompt for email generation"""
        return """
        You are an Expert Email Writer Assistant specialized in creating professional, clear, and engaging emails.
        Your job is to write or rewrite emails based on the given topic and human feedback.

        Instructions:
        - Write in proper email format with appropriate greeting, body, and closing
        - Use a professional yet friendly tone that's suitable for business communication
        - Keep the email concise, clear, and actionable
        - Include appropriate subject line suggestions when relevant
        - Apply any human feedback to improve the email's effectiveness
        - Ensure the email serves its intended purpose (request, update, invitation, etc.)
        - Use proper email etiquette and formatting

        Email Structure Guidelines:
        - Start with appropriate greeting (Dear [Name], Hi [Name], Hello, etc.)
        - Clear and engaging opening line
        - Well-organized body paragraphs with clear purpose
        - Professional closing with call-to-action if needed
        - Appropriate sign-off (Best regards, Sincerely, etc.)

        Tone Guidelines:
        - Professional yet approachable
        - Clear and direct communication
        - Respectful and courteous
        - Action-oriented when applicable

        Output Rule:
        Return only the email content in proper email format — no extra explanations, notes, or commentary.
        """
    
    def _build_user_message(self, topic: str, feedback: str, previous_content: str) -> str:
        """Build user message with context"""
        return f"""Email Topic/Purpose: {topic}

Human Feedback for Improvement: {feedback or 'No specific feedback'}

Previous Email Draft: {previous_content or 'No previous draft - create new email'}"""


# Global LLM service instance (lazy initialization)
llm_service = LLMService()
