"""
Simple ChatGPT-like Agent - For Group 2 students
Provides general Q&A without customization
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any, List
import re
import sympy as sp
from sympy import latex
from config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class ChatGPTLikeAgent:
    """
    Simple ChatGPT interface for Group 2
    No customization or pre-assessment analysis
    Just a straightforward Q&A interface
    """
    
    SYSTEM_PROMPT = r"""You are a helpful Trigonometry assistant.

⚠️ LATEX FORMATTING REQUIREMENT:
✅ Use proper LaTeX for ALL mathematical expressions:
- Inline math (use single $): The sine of an angle is $\sin(\theta)$  
- Display equations (use double $$): $$\sin^2(\theta) + \cos^2(\theta) = 1$$
- Fractions: $\frac{1}{2}$ not 1/2
- Powers: $x^2$ not x^2  
- Roots: $\sqrt{x}$ not sqrt(x)
- Trig functions: $\sin(x)$, $\cos(x)$, $\tan(x)$
- Greek letters: $\theta$, $\alpha$, $\pi$
- Angles: $30^\circ$ not 30°
- Equations: $x = 5$ not x = 5

❌ Never use plain text for math: sin(θ), 1/2, sqrt(2), or θ

Answer questions clearly and concisely.
When asked about trigonometry concepts, provide accurate information.
You can show worked examples and solutions.
Be friendly and patient.
"""
    
    def __init__(self):
        """Initialize the ChatGPT-like Agent"""
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        self.chat_history: List[Dict[str, str]] = []
    
    def _format_with_sympy(self, text: str) -> str:
        """
        Post-process text to ensure all mathematical expressions are in LaTeX format
        Converts plain text math to LaTeX that Streamlit can render properly
        """
        import re
        
        # Skip if already has lots of LaTeX formatting
        latex_count = text.count('$')
        if latex_count > 10:  # Already well-formatted
            return text
        
        result = text
        
        # Only convert obvious plain-text math that slipped through
        conversions = [
            # Plain trig functions
            (r'(?<!\$)\bsin\s*\(([^)]+)\)(?!\$)', r'$\\sin(\1)$'),
            (r'(?<!\$)\bcos\s*\(([^)]+)\)(?!\$)', r'$\\cos(\1)$'),
            (r'(?<!\$)\btan\s*\(([^)]+)\)(?!\$)', r'$\\tan(\1)$'),
            # Plain Greek letters
            (r'(?<!\$)\btheta\b(?!\$)', r'$\\theta$'),
            (r'(?<!\$)\balpha\b(?!\$)', r'$\\alpha$'),
            (r'(?<!\$)\bbeta\b(?!\$)', r'$\\beta$'),
            # Degree symbols
            (r'(?<!\$)(\d+)\s*°(?!\$)', r'$\1^\\circ$'),
            (r'(?<!\$)(\d+)\s*degrees(?!\$)', r'$\1^\\circ$'),
            # Plain fractions
            (r'(?<!\$)\b(\d+)/(\d+)\b(?!\$)', r'$\\frac{\1}{\2}$'),
            # Plain sqrt
            (r'(?<!\$)\bsqrt\s*\(([^)]+)\)(?!\$)', r'$\\sqrt{\1}$'),
        ]
        
        for pattern, replacement in conversions:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def ask_question(self, user_question: str) -> Dict[str, Any]:
        """
        Answer a question from the student
        
        Args:
            user_question: The student's question
            
        Returns:
            The answer
        """
        try:
            # Build conversation context
            conversation = self.SYSTEM_PROMPT
            
            # Add previous messages for context
            for msg in self.chat_history[-5:]:  # Keep last 5 messages for context
                if msg['role'] == 'user':
                    conversation += f"\nStudent: {msg['content']}"
                else:
                    conversation += f"\nAssistant: {msg['content']}"
            
            # Add current question
            conversation += f"\nStudent: {user_question}\nAssistant:"
            
            # Get response
            message = HumanMessage(content=conversation)
            response = self.llm.invoke([message])
            
            # Apply SymPy post-processing to ensure LaTeX formatting
            answer_text = self._format_with_sympy(response.content)
            
            # Store in history
            self.chat_history.append({
                "role": "user",
                "content": user_question
            })
            self.chat_history.append({
                "role": "assistant",
                "content": answer_text
            })
            
            return {
                "success": True,
                "question": user_question,
                "answer": answer_text
            }
        
        except Exception as e:
            print(f"Error in chat: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": user_question
            }
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get full conversation history"""
        return self.chat_history
    
    def clear_history(self):
        """Clear conversation history (for new sessions)"""
        self.chat_history = []
