import os
import logging
import google.generativeai as genai
from typing import Optional

class GeminiService:
    """Service for handling Google Gemini AI model interactions"""
    
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.is_loading = False
        self.error = None
        self.model_name = "SQUAD ONE - BERYL AGENTIC BUILDER (Gemini)"
        
        try:
            self._initialize_gemini()
        except Exception as e:
            logging.error(f"Failed to initialize Gemini service: {e}")
            self.error = str(e)
    
    def _initialize_gemini(self):
        """Initialize Gemini AI with API key"""
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not found")
        
        self.is_loading = True
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_loaded = True
            self.is_loading = False
            logging.info("Gemini service initialized successfully")
        except Exception as e:
            self.is_loading = False
            self.error = f"Failed to initialize Gemini: {str(e)}"
            raise e
    
    def generate_response(self, message: str, conversation_history: Optional[list] = None) -> str:
        """Generate a response using Gemini"""
        if not self.is_loaded:
            raise RuntimeError("Gemini service not loaded")
        
        try:
            # Format the conversation history for context
            context = ""
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages for context
                    role = "Human" if msg['role'] == 'user' else "Assistant"
                    context += f"{role}: {msg['content']}\n"
            
            # Create the prompt with context and current message
            prompt = f"""You are SQUAD ONE, a BERYL AGENTIC BUILDER AI assistant. Please respond naturally and helpfully to the user's message.

{context}Human: {message}
Assistant: """
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                raise RuntimeError("Gemini returned empty response")
                
        except Exception as e:
            logging.error(f"Gemini generation error: {e}")
            raise RuntimeError(f"Failed to generate response: {str(e)}")

    def get_status(self) -> dict:
        """Get service status"""
        return {
            'is_loaded': self.is_loaded,
            'is_loading': self.is_loading,
            'error': self.error,
            'model_name': self.model_name
        }