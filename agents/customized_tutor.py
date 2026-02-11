"""
Customized Trigonometry Tutor Agent - Searches web and teaches students
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any, List
import requests
from config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class CustomizedTutorAgent:
    """
    Customized tutor that searches internet resources and provides tailored teaching
    """
    
    SYSTEM_PROMPT = """You are an expert Trigonometry tutor AI with a passion for teaching.

Your teaching approach:
1. **Assess Level**: Understand the student's current knowledge
2. **Break Down Concepts**: Use simple, clear explanations with examples
3. **Step-by-Step**: Walk through problems methodically
4. **Verify Understanding**: Ask questions to check comprehension
5. **Provide Real Examples**: Use real-world applications of trigonometry
6. **Build Confidence**: Be encouraging and patient

When teaching:
- Design explanations for the student's learning level
- Use diagrams descriptions (use text to describe visual concepts)
- Show worked examples with each step explained
- Challenge with practice problems
- Connect concepts to previously learned material
- Always explain WHY, not just HOW

Tone: Friendly, encouraging, expert, patient
"""
    
    def __init__(self, student_pre_assessment: Dict = None):
        """
        Initialize the Customized Tutor
        
        Args:
            student_pre_assessment: The student's previous assessment results
        """
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        self.student_pre_assessment = student_pre_assessment or {}
        self.chat_history: List[Dict[str, str]] = []
    
    def search_concept(self, concept: str) -> str:
        """
        Search for concept information (simulated web search)
        In production, you'd use Google Custom Search or similar
        """
        # For now, return knowledge base - in production use real web search
        knowledge_base = {
            "sine": "Sine is a trigonometric function. In a right triangle, sine of an angle = opposite/hypotenuse. sin(θ) ranges from -1 to 1. Special values: sin(0°)=0, sin(30°)=0.5, sin(45°)=√2/2, sin(60°)=√3/2, sin(90°)=1",
            "cosine": "Cosine is a trigonometric function. In a right triangle, cosine of an angle = adjacent/hypotenuse. cos(θ) ranges from -1 to 1. Special values: cos(0°)=1, cos(30°)=√3/2, cos(45°)=√2/2, cos(60°)=0.5, cos(90°)=0",
            "tangent": "Tangent is a trigonometric function. tan(θ) = sin(θ)/cos(θ) = opposite/adjacent. Special values: tan(0°)=0, tan(30°)=1/√3, tan(45°)=1, tan(60°)=√3",
            "sohcahtoa": "SOHCAHTOA is a mnemonic: Sine=Opposite/Hypotenuse, Cosine=Adjacent/Hypotenuse, Tangent=Opposite/Adjacent. Use this to remember the three main trigonometric ratios",
            "pythagorean identity": "sin²(θ) + cos²(θ) = 1. This fundamental identity is true for all angles θ. It comes from the Pythagorean theorem applied to the unit circle",
            "unit circle": "The unit circle is a circle with radius 1 centered at origin. Used to visualize trigonometric functions. Any point on it has coordinates (cos(θ), sin(θ))",
            "inverse trigonometric": "Inverse functions: arcsin, arccos, arctan. If sin(θ)=x, then θ=arcsin(x). Used to find angles when you know the ratio"
        }
        
        for key, value in knowledge_base.items():
            if key in concept.lower():
                return value
        
        return f"Information about {concept}: This advanced trigonometry topic requires deeper study. Use your textbook or online resources for comprehensive information."
    
    def teach_concept(self, question_id: int, question: Dict, student_level: str = "intermediate") -> Dict[str, Any]:
        """
        Generate a customized teaching explanation for a concept
        
        Args:
            question_id: The question ID
            question: The question dict with concept and hint
            student_level: Student's learning level (beginner, intermediate, advanced)
            
        Returns:
            Teaching explanation
        """
        try:
            concept = question.get('concept', '')
            hint = question.get('hint', '')
            
            # Search concept information
            concept_info = self.search_concept(concept)
            
            # Build teaching prompt
            teaching_prompt = f"""
I need to teach a {student_level} student about: {concept}

Question Focus: {question.get('question', '')}
Key Hint: {hint}

Research/Knowledge: {concept_info}

Based on this, create a comprehensive teaching explanation that:
1. Starts with a simple definition
2. Explains WHY this concept matters
3. Provides visual descriptions (since we can't show real images)
4. Gives 2-3 worked examples
5. Includes a practice question
6. Summarizes key takeaways

Use a friendly, encouraging tone and break down complex ideas into simple steps.
"""
            
            message = HumanMessage(content=self.SYSTEM_PROMPT + "\n\n" + teaching_prompt)
            response = self.llm.invoke([message])
            
            # Store in history
            self.chat_history.append({
                "role": "assistant",
                "content": response.content,
                "question_id": question_id
            })
            
            return {
                "success": True,
                "question_id": question_id,
                "concept": concept,
                "explanation": response.content,
                "hint": hint
            }
        
        except Exception as e:
            print(f"Error teaching concept: {e}")
            return {
                "success": False,
                "error": str(e),
                "question_id": question_id
            }
    
    def answer_student_question(self, student_question: str) -> Dict[str, Any]:
        """
        Answer a student's specific question during learning
        
        Args:
            student_question: The student's question
            
        Returns:
            Answer and explanation
        """
        try:
            # Build context from pre-assessment
            context = ""
            if self.student_pre_assessment:
                weak_areas = self.student_pre_assessment.get('weak_areas', [])
                context = f"Student's weak areas: {', '.join(weak_areas)}. Focus explanation on these areas."
            
            prompt = f"""
Student Question: {student_question}

{context}

Please provide a clear, step-by-step answer that:
1. Addresses the specific question
2. Explains the underlying concept
3. Shows worked examples if applicable
4. Offers a practice problem if relevant
5. Relates to real-world applications when possible
"""
            
            message = HumanMessage(content=self.SYSTEM_PROMPT + "\n\n" + prompt)
            response = self.llm.invoke([message])
            
            # Store in history
            self.chat_history.append({
                "role": "user",
                "content": student_question
            })
            self.chat_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            return {
                "success": True,
                "question": student_question,
                "answer": response.content
            }
        
        except Exception as e:
            print(f"Error answering question: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": student_question
            }
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.chat_history
