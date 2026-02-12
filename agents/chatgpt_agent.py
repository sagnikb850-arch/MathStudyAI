"""
Simple ChatGPT-like Agent - For Group 2 students
Provides general Q&A without customization
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any, List
from config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class ChatGPTLikeAgent:
    """
    Simple ChatGPT interface for Group 2
    No customization or pre-assessment analysis
    Just a straightforward Q&A interface
    """
    
    SYSTEM_PROMPT = r"""You are a helpful Trigonometry assistant.

⚠️ CRITICAL FORMATTING REQUIREMENT - READ FIRST:
🔴 YOU MUST USE LATEX FOR EVERY SINGLE MATHEMATICAL EXPRESSION 🔴
This is ABSOLUTELY MANDATORY. Every number, variable, equation, angle, or mathematical symbol MUST be wrapped in LaTeX.

📐 LATEX FORMATTING RULES (ABSOLUTELY MANDATORY - NO EXCEPTIONS):

✅ CORRECT - Always do this:
- Inline math: $\sin(\theta)$, $x = 5$, $\frac{opposite}{hypotenuse}$, $30^\circ$, $0.5$
- Display equations: $$\sin^2(\theta) + \cos^2(\theta) = 1$$
- Fractions: $\frac{1}{2}$, $\frac{a}{b}$
- Powers: $x^2$, $\sin^2(\theta)$
- Roots: $\sqrt{x}$, $\sqrt{2}$
- Trig functions: $\sin(x)$, $\cos(x)$, $\tan(x)$, $\arcsin(x)$
- Greek letters: $\theta$, $\alpha$, $\beta$, $\pi$
- Angles: $30^\circ$, $45^\circ$
- All numbers in math: $1$, $2$, $3.14$, $0.5$

❌ WRONG - Never do this:
- Plain text: sin(θ), x = 5, 1/2, sqrt(2)
- Naked numbers: The answer is 5 (should be: The answer is $5$)
- Unformatted fractions: 1/2 (should be: $\frac{1}{2}$)

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
            
            # Store in history
            self.chat_history.append({
                "role": "user",
                "content": user_question
            })
            self.chat_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            return {
                "success": True,
                "question": user_question,
                "answer": response.content
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
