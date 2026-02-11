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

⚠️ MATHEMATICAL NOTATION:
Use LaTeX syntax for all math. Students only see RENDERED MATH SYMBOLS (no LaTeX code).

What you write → What students see:
- $\sin(\theta)$ → sin(θ) as pure math symbol
- $\frac{1}{2}$ → ½ as pure fraction
- $\theta$ → θ as pure Greek letter
- $30^\circ$ → 30° as pure degree symbol
- $$equation$$ → Centered equation with pure symbols

Students NEVER see $, \, or LaTeX commands - only beautiful math notation.

✅ Correct: $\sin(30^\circ) = \frac{1}{2}$
❌ Wrong: sin(30 degrees) = 1/2

Answer clearly and provide worked examples with proper LaTeX formatting.
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
        Pass-through function - AI should output proper LaTeX
        Streamlit handles the rendering automatically
        """
        return text
    
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
