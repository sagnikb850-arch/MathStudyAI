"""
Customized Trigonometry Tutor Agent - ReAct-based Socratic Tutoring
Uses ReAct prompting, Socratic questioning, and never reveals answers
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Dict, Any, List, Optional
import json
from config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class CustomizedTutorAgent:
    """
    AI Tutor using ReAct framework with Socratic questioning.
    Never reveals answers - only guides students through reasoning.
    """
    
    SYSTEM_PROMPT = """You are an expert AI Trigonometry Tutor using the ReAct (Reasoning + Action) framework.

🎯 YOUR CORE PRINCIPLES:
1. **NEVER REVEAL THE ANSWER** - Your job is to guide, not solve
2. **Use Socratic Questioning** - Ask leading questions to help students discover answers
3. **Think Step-by-Step** - Break complex problems into manageable chunks
4. **Be Encouraging** - Praise effort and progress, even small steps
5. **Address Misconceptions** - Gently correct errors with questions, not direct correction

📋 ReAct FRAMEWORK (Use this for every student question):

**THOUGHT**: Analyze what the student is asking and what they need to learn
- What concept is involved?
- What are the sub-steps to solve this?
- What misconceptions might they have?
- What's their current understanding level?

**ACTION**: Decide what pedagogical action to take
- Break problem into smaller steps
- Ask a guiding question about the first/next step
- Provide a hint or analogy
- Use a tool (if needed): SymPy for symbolic math, or describe a visualization

**OBSERVATION**: After student responds, observe their understanding
- Did they grasp the concept?
- Do they have misconceptions?
- Are they ready for the next step?

🔄 INTERACTION PATTERN:
1. Student asks a question
2. YOU (Thought): "Let me think about how to guide them..."
3. YOU (Action): Ask a Socratic question about the first step
4. Student responds
5. YOU (Observation): Assess their understanding
6. YOU (Thought): Decide next step based on their response
7. YOU (Action): Guide them to the next step
8. Repeat until student discovers the answer themselves

💡 SOCRATIC QUESTION EXAMPLES:
- "What do we know about this triangle? What information is given?"
- "When you see sin(30°), what does that mean in terms of a triangle?"
- "What formula connects these three pieces of information?"
- "If we want to find the angle, what operation reverses sine?"
- "Does your answer make sense? How can you check it?"

🚫 NEVER DO THIS:
- "The answer is 0.5"
- "Here's the complete solution: ..."
- "Just plug it into the formula and you get..."
- Give step-by-step solutions that do all the work

✅ ALWAYS DO THIS:
- "What do you think the first step should be?"
- "Great start! Now, what happens when we apply that principle?"
- "You're on the right track! What relationship exists between sine and opposite/hypotenuse?"
- "Excellent thinking! How can we use that to find θ?"

🧰 AVAILABLE TOOLS (Use when helpful, but don't over-rely):
1. **SymPy**: For symbolic manipulation (e.g., "Let's see what SymPy shows us about sin²(θ) + cos²(θ)")
2. **Graphing**: Describe what a graph would look like (e.g., "Imagine plotting sin(θ) from 0° to 90°...")

💾 MEMORY:
- Remember student's weak areas from their assessment
- Track misconceptions mentioned in this session
- Adapt difficulty based on their responses
- Reference previous parts of the conversation

🎓 YOUR TONE:
- Warm, encouraging, patient
- Excited about mathematical discovery
- Never condescending
- Celebrate small victories
- Use phrases like "Excellent thinking!", "You're getting closer!", "Great observation!"

Remember: Your success is measured by student discovery, not by providing answers!"""
    
    def __init__(self, student_pre_assessment: Dict = None):
        """
        Initialize the ReAct-based Tutor with Memory Management
        
        Args:
            student_pre_assessment: Student's pre-assessment results for personalization
        """
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name="gpt-4o",  # Use GPT-4o for better reasoning
            temperature=0.7,  # Balanced creativity
            max_tokens=MAX_TOKENS
        )
        
        # Student-specific memory (persistent across sessions)
        self.student_memory = {
            "weak_areas": student_pre_assessment.get('weak_areas', []) if student_pre_assessment else [],
            "strong_areas": student_pre_assessment.get('strong_areas', []) if student_pre_assessment else [],
            "difficulty_level": student_pre_assessment.get('difficulty_level', 'intermediate') if student_pre_assessment else 'intermediate',
            "misconceptions": [],  # Track recurring errors
            "learning_style": "visual",  # Can be updated based on interactions
            "progress_notes": []
        }
        
        # Session-specific memory (current conversation context)
        self.session_memory = {
            "current_problem": None,
            "problem_steps": [],
            "completed_steps": [],
            "current_step": None,
            "student_attempts": [],
            "conversation_history": [],
            "tools_used": []
        }
        
        # Full conversation history for context
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
    
    def _use_sympy_tool(self, expression: str) -> str:
        """
        Simulate SymPy tool for symbolic mathematics
        In production, this would actually use sympy library
        """
        try:
            import sympy as sp
            # Parse and evaluate using sympy
            result = sp.simplify(expression)
            return f"SymPy shows: {result}"
        except:
            # Fallback if sympy not available
            return f"Mathematical analysis of: {expression} (SymPy helps us verify identities and simplify expressions)"
    
    def _describe_graph(self, function: str, range_info: str) -> str:
        """
        Describe what a graph would look like
        In production, this could generate actual plots with matplotlib
        """
        descriptions = {
            "sin": "The sine wave starts at 0, rises to 1 at 90°, returns to 0 at 180°, goes to -1 at 270°, and returns to 0 at 360°. It creates a smooth, repeating wave pattern.",
            "cos": "The cosine wave starts at 1, decreases to 0 at 90°, reaches -1 at 180°, returns to 0 at 270°, and completes at 1 at 360°. It's the same shape as sine but shifted.",
            "tan": "The tangent function starts at 0, increases rapidly, and approaches infinity as it nears 90°. It has vertical asymptotes (undefined points) at 90° and 270°."
        }
        
        for key, desc in descriptions.items():
            if key in function.lower():
                return f"📊 Graph visualization: {desc} {range_info}"
        
        return f"📊 If we graph {function} over {range_info}, we can see the pattern of how values change."
    
    def _break_into_steps(self, problem: str, concept: str) -> List[str]:
        """
        Break a problem into logical steps (internal reasoning)
        """
        # Step decomposition based on concept
        step_templates = {
            "sine": ["Identify the triangle parts", "Recall SOH (Sine = Opposite/Hypotenuse)", "Set up the equation", "Solve for the unknown"],
            "cosine": ["Identify the triangle parts", "Recall CAH (Cosine = Adjacent/Hypotenuse)", "Set up the equation", "Solve for the unknown"],
            "tangent": ["Identify the triangle parts", "Recall TOA (Tangent = Opposite/Adjacent)", "Set up the equation", "Solve for the unknown"],
            "inverse": ["Recognize we need an angle", "Choose inverse trig function", "Apply the inverse function", "Verify the result"],
            "identity": ["Write out the identity", "Substitute known values", "Simplify step by step", "Verify the result"]
        }
        
        for key, steps in step_templates.items():
            if key in concept.lower() or key in problem.lower():
                return steps
        
        return ["Understand the question", "Identify what's given", "Choose the right approach", "Work through the solution", "Check your answer"]
    
    def teach_concept(self, question_id: int, question: Dict, student_level: str = "intermediate") -> Dict[str, Any]:
        """
        Teach a concept using ReAct framework with Socratic guidance
        NEVER reveals the answer
        """
        try:
            concept = question.get('concept', '')
            hint = question.get('hint', '')
            problem = question.get('question', '')
            
            # Update session memory
            self.session_memory['current_problem'] = problem
            self.session_memory['problem_steps'] = self._break_into_steps(problem, concept)
            self.session_memory['completed_steps'] = []
            self.session_memory['current_step'] = self.session_memory['problem_steps'][0] if self.session_memory['problem_steps'] else None
            
            # Build context-aware prompt
            context = f"""
📚 **Current Learning Context:**
- Concept: {concept}
- Student Level: {student_level}
- Weak Areas: {', '.join(self.student_memory['weak_areas']) if self.student_memory['weak_areas'] else 'None identified yet'}
- Difficulty: {self.student_memory['difficulty_level']}

📝 **Problem/Question:** {problem}
🔑 **Key Hint Available:** {hint}

🎯 **Your Task (Use ReAct):**
1. **THOUGHT**: Think about how to break this down into steps for the student
2. **ACTION**: Ask a Socratic question about the FIRST step only (don't reveal the answer!)
3. Guide them toward understanding the concept through discovery

Remember: 
- DO NOT solve the problem for them
- DO NOT give the final answer  
- DO ask questions that lead them to figure it out
- DO be encouraging and patient
- DO use the hint to guide your questions, but don't reveal it directly

**Begin your tutoring response:**
"""
            
            self.messages.append({"role": "user", "content": context})
            
            # Get AI response
            response = self.llm.invoke([
                SystemMessage(content=self.SYSTEM_PROMPT),
                HumanMessage(content=context)
            ])
            
            response_text = response.content
            
            # Store in conversation history
            self.messages.append({"role": "assistant", "content": response_text})
            self.session_memory['conversation_history'].append({
                "type": "concept_teaching",
                "problem": problem,
                "concept": concept,
                "tutor_response": response_text
            })
            
            return {
                "success": True,
                "question_id": question_id,
                "concept": concept,
                "explanation": response_text,
                "hint": hint,
                "react_mode": True
            }
        
        except Exception as e:
            print(f"Error in teach_concept: {e}")
            return {
                "success": False,
                "error": str(e),
                "question_id": question_id
            }
    
    def answer_student_question(self, student_question: str, student_previous_response: str = None) -> Dict[str, Any]:
        """
        Answer student's question using ReAct framework
        Continues Socratic dialogue, never reveals the answer
        """
        try:
            # Add student question to memory
            self.session_memory['student_attempts'].append({
                "question": student_question,
                "response": student_previous_response,
                "timestamp": "current"
            })
            
            # Build ReAct prompt with full context
            memory_context = f"""
🧠 **Student Memory:**
- Weak Areas: {', '.join(self.student_memory['weak_areas'])}
- Known Misconceptions: {', '.join(self.student_memory['misconceptions']) if self.student_memory['misconceptions'] else 'None yet'}
- Difficulty Level: {self.student_memory['difficulty_level']}

📝 **Current Session:**
- Problem: {self.session_memory.get('current_problem', 'General question')}
- Steps in Problem: {' → '.join(self.session_memory.get('problem_steps', []))}
- Current Step: {self.session_memory.get('current_step', 'Not set')}
- Completed Steps: {' ✓ '.join(self.session_memory.get('completed_steps', [])) if self.session_memory.get('completed_steps') else 'None yet'}

💬 **Recent Conversation:**
{self._format_recent_history(3)}

🎓 **Student's Current Question/Response:**
"{student_question}"
{f'Previous Response: "{student_previous_response}"' if student_previous_response else ''}

🎯 **Your ReAct Response:**

**THOUGHT**: 
- What is the student trying to understand?
- Do they have any misconceptions here?
- What step are they on in the problem-solving process?
- Are they ready to move to the next step?

**ACTION**: 
- If they're correct: Praise them and ask a question about the NEXT step
- If they're stuck: Give a gentle hint through a question
- If they have a misconception: Use a question to help them see the error
- If they ask for the answer: Redirect with "Let's figure it out together! What do you think about..."

**Remember**: NEVER give the complete answer. Guide them to discover it!

**Your Response:**
"""
            
            self.messages.append({"role": "user", "content": memory_context})
            
            # Get AI response with ReAct reasoning
            response = self.llm.invoke(self.messages[-5:] if len(self.messages) > 5 else self.messages)
            
            response_text = response.content
            
            # Store in history
            self.messages.append({"role": "assistant", "content": response_text})
            self.session_memory['conversation_history'].append({
                "type": "student_question",
                "question": student_question,
                "tutor_response": response_text
            })
            
            # Check if student seems to have completed current step
            if self._detect_step_completion(student_question, response_text):
                if self.session_memory['current_step']:
                    self.session_memory['completed_steps'].append(self.session_memory['current_step'])
                
                # Move to next step
                remaining_steps = [s for s in self.session_memory.get('problem_steps', []) 
                                 if s not in self.session_memory.get('completed_steps', [])]
                if remaining_steps:
                    self.session_memory['current_step'] = remaining_steps[0]
            
            return {
                "success": True,
                "question": student_question,
                "answer": response_text,
                "current_step": self.session_memory.get('current_step'),
                "progress": f"{len(self.session_memory.get('completed_steps', []))}/{len(self.session_memory.get('problem_steps', []))} steps",
                "react_mode": True
            }
        
        except Exception as e:
            print(f"Error answering question: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": student_question
            }
    
    def _format_recent_history(self, n: int = 3) -> str:
        """Format recent conversation for context"""
        history = self.session_memory.get('conversation_history', [])[-n:]
        formatted = []
        for entry in history:
            if entry['type'] == 'student_question':
                formatted.append(f"Student: {entry['question']}")
                formatted.append(f"Tutor: {entry['tutor_response'][:100]}...")
        return "\n".join(formatted) if formatted else "No previous conversation"
    
    def _detect_step_completion(self, student_input: str, tutor_response: str) -> bool:
        """
        Detect if student has successfully completed current step
        Simple heuristic: look for praise words in tutor response
        """
        praise_indicators = ["correct", "excellent", "great", "right", "good job", "well done", "perfect"]
        return any(praise in tutor_response.lower() for praise in praise_indicators)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.session_memory.get('conversation_history', [])
