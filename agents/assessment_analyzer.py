"""
Assessment Analyzer Agent - Rates student performance
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any, List
import json
from config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class AssessmentAnalyzerAgent:
    """
    Analyzes student assessment performance and provides detailed ratings
    """
    
    SYSTEM_PROMPT = """You are an expert mathematics teacher and assessment evaluator specializing in Trigonometry.
Your role is to:

1. **Analyze Student Answers**: Review each answer and determine correctness
2. **Calculate Score**: Generate a percentage score based on correct answers
3. **Identify Weak Areas**: Find which trigonometry concepts the student struggles with
4. **Provide Feedback**: Give constructive, encouraging feedback
5. **Recommend Learning Path**: Suggest which concepts to focus on

When analyzing:
- Be precise about what's correct and incorrect
- Explain the correct concept briefly
- Rate difficulty level (Easy, Moderate, Hard, Expert)
- Provide an overall performance summary

Return JSON format:
{
    "total_questions": number,
    "correct_answers": number,
    "score_percentage": number,
    "difficulty_level": "Easy/Moderate/Hard/Expert",
    "weak_areas": ["concept1", "concept2"],
    "strong_areas": ["concept1"],
    "detailed_feedback": "Overall feedback",
    "recommendations": ["recommendation1", "recommendation2"],
    "next_steps": "What student should focus on"
}
"""
    
    def __init__(self):
        """Initialize the Assessment Analyzer Agent"""
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
    
    def analyze_assessment(self, student_id: str, answers: List[Dict], questions: List[Dict]) -> Dict[str, Any]:
        """
        Analyze student's assessment answers
        
        Args:
            student_id: Student's ID
            answers: List of {"question_id": id, "student_answer": answer}
            questions: List of question objects with correct answers
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Build analysis prompt
            analysis_text = f"""
Student ID: {student_id}

Questions and Answers:
"""
            
            correct_count = 0
            for i, answer in enumerate(answers):
                q_id = answer.get('question_id')
                student_ans = answer.get('student_answer')
                
                # Find matching question
                question = next((q for q in questions if q['id'] == q_id), None)
                if question:
                    is_correct = student_ans == question.get('correct_answer')
                    if is_correct:
                        correct_count += 1
                    
                    analysis_text += f"""
Question {i+1}: {question.get('question')}
Student Answer: {student_ans}
Correct Answer: {question.get('correct_answer')}
Status: {'✓ CORRECT' if is_correct else '✗ INCORRECT'}
Explanation: {question.get('explanation', 'N/A')}
"""
            
            analysis_text += f"""

Total Score: {correct_count}/{len(answers)} ({(correct_count/len(answers)*100):.1f}%)

Please analyze this student's performance and provide detailed feedback in JSON format.
"""
            
            # Get AI analysis
            message = HumanMessage(content=self.SYSTEM_PROMPT + "\n\n" + analysis_text)
            response = self.llm.invoke([message])
            
            # Parse response
            try:
                # Extract JSON from response
                response_text = response.content
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    analysis_json = json.loads(response_text[json_start:json_end])
                else:
                    analysis_json = {
                        "total_questions": len(answers),
                        "correct_answers": correct_count,
                        "score_percentage": (correct_count/len(answers)*100),
                        "difficulty_level": "Moderate",
                        "weak_areas": [],
                        "strong_areas": [],
                        "detailed_feedback": response.content,
                        "recommendations": [],
                        "next_steps": "Continue learning"
                    }
            except:
                analysis_json = {
                    "total_questions": len(answers),
                    "correct_answers": correct_count,
                    "score_percentage": (correct_count/len(answers)*100),
                    "difficulty_level": "Moderate",
                    "weak_areas": [],
                    "strong_areas": [],
                    "detailed_feedback": response.content,
                    "recommendations": [],
                    "next_steps": "Continue learning"
                }
            
            analysis_json['student_id'] = student_id
            analysis_json['assessment_type'] = 'pre' if len(answers) == 5 else 'final'
            
            return {
                "success": True,
                "analysis": analysis_json,
                "student_id": student_id
            }
        
        except Exception as e:
            print(f"Error analyzing assessment: {e}")
            return {
                "success": False,
                "error": str(e),
                "student_id": student_id
            }
