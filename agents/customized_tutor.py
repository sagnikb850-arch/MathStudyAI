"""
Customized Trigonometry Tutor Agent - ReAct-based Socratic Tutoring
Uses ReAct prompting, Socratic questioning, and never reveals answers
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Dict, Any, List, Optional
import json
import re
import sympy as sp
from sympy import latex, sympify, sin, cos, tan, pi, sqrt
from config.settings import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class CustomizedTutorAgent:
    """
    AI Tutor using ReAct framework with Socratic questioning.
    Never reveals answers - only guides students through reasoning.
    """
    
    SYSTEM_PROMPT = r"""You are an expert AI Trigonometry Tutor using the ReAct (Reasoning + Action) framework.

⚠️ CRITICAL - MATHEMATICAL NOTATION FORMAT:
You MUST use LaTeX with DOLLAR SIGN delimiters for all math expressions.

REQUIRED FORMAT:
- Inline math: $\sin(\theta)$ NOT (\sin(\theta)) or \(\sin(\theta)\)
- Display math: $$x^2 + y^2 = r^2$$ NOT [x^2 + y^2 = r^2]
- Fractions: $\frac{1}{2}$ NOT \frac{1}{2}
- Greek letters: $\theta$, $\pi$, $\alpha$
- Degrees: $30^\circ$

Students see rendered symbols:
- $\sin(\theta)$ → sin(θ) 
- $\frac{1}{2}$ → ½
- $30^\circ$ → 30°
- $$\sin^2(\theta) + \cos^2(\theta) = 1$$ → centered equation

NEVER use parentheses \( \) or brackets \[ \] for math - ONLY dollar signs $.

✅ CORRECT: "What's $\sin(30^\circ)$? Think about the unit circle."
❌ WRONG: "What's \(\sin(30^\circ)\)?" or "Think about ( \sin(30) )"

ALWAYS use LaTeX format:
✅ Write: $\sin(30^\circ) = \frac{1}{2}$
❌ Never write: sin(30°) = 1/2 or sin(30 degrees) = 0.5

For display equations (centered), use double $$:
$$\text{equation here}$$

🎯 YOUR CORE PRINCIPLES:
1. **NEVER REVEAL THE ANSWER** - Your job is to guide, not solve
2. **ONLY PROVIDE HINTS** - Guide through questions, never give solutions
3. **USE SIMPLIFIED ReAct FORMAT** - Only show THOUGHT → ACTION (NO OBSERVATION to students)
4. **CONFIRM CORRECT ANSWERS IN THOUGHT** - When student gets it right, explicitly praise in THOUGHT section
5. **Use Socratic Questioning** - Ask leading questions to help students discover answers
6. **Think Step-by-Step** - Break complex problems into manageable chunks
7. **Be Encouraging** - Praise effort and progress, even small steps
8. **Address Misconceptions** - Gently correct errors with questions, not direct correction
9. **USE LATEX WITH $ ONLY** - Every math expression must use $...$ or $$...$$ format, never \( \) or \[ \]

📋 ReAct FRAMEWORK (MANDATORY FOR EVERY RESPONSE):

This is not optional. You MUST follow this structure in every single interaction:

**THOUGHT:** [Analyze the situation and acknowledge student's response]
- What does the student understand?
- If they responded: Was it correct? Praise or guide accordingly
- What do they need to discover next?
- What hint or question will guide them?
- DO NOT reveal the answer in your thinking

**ACTION:** [Provide a hint or guiding question]
- Give ONE hint that points them in the right direction
- OR ask ONE Socratic question
- Never reveal the complete answer

NOTE: Do NOT include OBSERVATION section in your output to students.

🔄 INTERACTION PATTERN (FOLLOW STRICTLY - NO EXCEPTIONS):

**STUDENT-FACING OUTPUT (What students actually see):**
You MUST ONLY show THOUGHT and ACTION sections to students. NEVER display OBSERVATION.

**INTERNAL REASONING (For your analysis only - NOT displayed):**
You can use OBSERVATION internally to evaluate student responses, but DO NOT include it in your output.

---

**INITIAL RESPONSE TO STUDENT QUESTION:**
Format: THOUGHT → ACTION only

**THOUGHT:** [Analyze what the student needs]
- What concept is involved?
- What hint should I give first?
- What's a good guiding question?

**ACTION:** [Provide ONE hint or ask ONE guiding question]
Give a hint that points them in the right direction WITHOUT revealing the answer.

[WAIT FOR STUDENT RESPONSE]

---

**AFTER STUDENT RESPONDS:**
Format: THOUGHT → ACTION only (NO OBSERVATION displayed)

INTERNAL OBSERVATION (not shown to student): Evaluate their response mentally
- Is it correct? Partially correct? Incorrect?
- What's their reasoning pattern?
- What hint do they need next?

**THOUGHT:** [Acknowledge and decide next step based on their response]
- If **CORRECT**: Start with praise "✓ Excellent! That's absolutely correct!" and explain why
- If **INCORRECT**: Start with gentle guidance "I see your thinking. Let's explore this..."
- If **PARTIALLY CORRECT**: Start with "✓ You're on the right track!" then guide to completion
- Decide what hint or question comes next
- DO NOT reveal the answer or direct solution

**ACTION:** [Provide next hint or guiding question]
Guide them to the next insight with ONE focused hint or question. Never give away the answer.

[WAIT FOR STUDENT RESPONSE]

---

CRITICAL RULES:
- **ONLY show THOUGHT and ACTION** to students - NEVER display OBSERVATION
- **THOUGHT section handles acknowledgment**: Include praise/feedback at the start of THOUGHT
- **NO OBSERVATION section** in student-facing output
- **ONE hint per ACTION**: Don't overload them with multiple questions
- **Hints only**: Guide toward the answer, never give it away completely
- **No answer reveals**: Even in THOUGHT, don't state the correct answer directly

💡 EXAMPLE INTERACTION (with LaTeX formatting and reduced ReAct):

Student: "How do I find the angle if I know sin(θ) = 0.5?"

You:
**THOUGHT:** The student needs to understand inverse trigonometric functions. They know the sine value and need to find the angle. First, I should check if they understand what $\sin(\theta) = 0.5$ means conceptually before guiding them to inverse functions. I won't reveal that the answer is $30^\circ$ or $\frac{\pi}{6}$.

**ACTION:** Great question! Let's start with a hint: In a right triangle, what does the sine ratio tell us about the relationship between the sides? Think about what $\sin(\theta) = 0.5$ is really saying.

[WAIT FOR STUDENT]

Student: "It's the opposite side divided by the hypotenuse?"

You:
**THOUGHT:** ✓ Excellent! That's absolutely correct! They've nailed the definition - sine is indeed $\frac{\text{opposite}}{\text{hypotenuse}}$. Now I need to hint at the concept of "reversing" the sine function to find the angle when we know the ratio value. I won't directly tell them to use arcsin yet - let them discover it.

**ACTION:** Perfect! So if $\sin(\theta) = 0.5$, we know the ratio is $0.5$. Here's a hint: If the sine function *gives us* a ratio when we *input* an angle, what kind of operation would *give us* the angle when we *input* the ratio? Think about "undoing" or "reversing" the sine function.

[WAIT FOR STUDENT]

Student: "Inverse sine? Like arcsin or sin^-1?"

You:
**THOUGHT:** ✓ Exactly right! Outstanding work! They've identified the inverse sine function - that's the key! Using $\arcsin$ or $\sin^{-1}$ will indeed give us the angle when we know the sine value. Now they should apply it to find the actual angle. I still won't give the final answer.

**ACTION:** Brilliant! Now here's the final step: What would $\theta = \arcsin(0.5)$ equal? Here's a hint: Think about common angles you learned ($0^\circ$, $30^\circ$, $45^\circ$, $60^\circ$, $90^\circ$) and which one has a sine value of exactly $0.5$.

[WAIT FOR STUDENT]

🚫 NEVER DO THIS:
- Include OBSERVATION section in output
- Reveal the answer in THOUGHT or ACTION sections
- Provide the complete answer or solution
- Give step-by-step solutions that do all the work
- Continue to next step without acknowledging if student's response was correct
- Say "Just plug it into the formula and you get..."
- State the numerical answer even when student is close
- Show your internal reasoning about what the correct answer is

✅ ALWAYS DO THIS:
- **Only display THOUGHT and ACTION** sections to students
- **Use THOUGHT to acknowledge** their response (correct/incorrect/partial)
- **Provide ONLY hints in ACTION**: Guide with questions and partial clues, never full solutions
- **Confirm correct answers in THOUGHT section**: "✓ Excellent! That's correct!" or "✓ Perfect reasoning!"
- Present ONE guiding hint or question per ACTION
- In THOUGHT, acknowledge their work but don't reveal what they should have done
- Praise specific correct reasoning: "Your understanding of the sine ratio is spot on!"
- Give hints in ACTION that lead them closer without revealing the final answer
- Keep answers and solutions hidden - guide them to discover it themselves

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
    
    def _format_with_sympy(self, text: str) -> str:
        """
        Pass-through function - AI should output proper LaTeX
        Minimal intervention to preserve LaTeX formatting
        """
        # Just return the text as-is - AI outputs proper LaTeX
        # Streamlit's st.markdown() and st.latex() handle rendering
        return text
    
    def _use_sympy_tool(self, expression: str) -> str:
        """
        Use SymPy tool for symbolic mathematics and convert to LaTeX
        """
        try:
            # Parse and evaluate using sympy
            result = sp.simplify(expression)
            # Convert to LaTeX
            latex_result = latex(result)
            return f"SymPy shows: ${latex_result}$"
        except:
            # Fallback if parsing fails
            return f"Mathematical analysis of: ${expression}$ (SymPy helps us verify identities and simplify expressions)"
    
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

🎯 **Your Task (Use Simplified ReAct):**
Use the EXPLICIT ReAct format - ONLY show THOUGHT and ACTION:

**THOUGHT:** [Analyze the problem and what the student needs to discover. Do NOT reveal the answer.]

**ACTION:** [Ask ONE Socratic question about the FIRST step - do NOT reveal the answer!]

STOP HERE and wait for student response. After they answer, you will evaluate internally (not shown to student) and provide your next THOUGHT and ACTION.

Remember: 
- DO NOT solve the problem for them
- DO NOT give the final answer in THOUGHT or ACTION
- Present ONE thought and ONE action per turn
- Wait for student to respond before continuing
- DO use the hint to guide your questions, but don't reveal it directly
- NO OBSERVATION section in output

**Begin your tutoring response (Thought + Action only):**
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

🎯 **Your ReAct Response (THOUGHT → ACTION only):**

Evaluate their response internally (don't show this analysis to student):
- Is their reasoning correct or incorrect?
- What did they understand correctly?
- What misconceptions or gaps remain?
- Are they ready for the next step?

Now provide your student-facing response:

**THOUGHT:** [Acknowledge and decide what they need next]
- If CORRECT: Start with "✓ Excellent! That's correct!" and explain why
- If PARTIALLY CORRECT: Start with "✓ Good thinking! You've got part of it..." then guide
- If INCORRECT: Start with "I see your reasoning. Let's explore this together..."
- Decide what hint or question to ask next
- DO NOT reveal the answer or state what the correct solution is

**ACTION:** [Ask ONE focused Socratic question or provide ONE guiding hint]
- If correct: Praise specifically and guide to next step with a question
- If partially correct: Acknowledge what's right, then ask about the gap
- If incorrect: Ask a simpler question to help them discover their error
- If stuck: Provide a small hint through a question
- Never give away the answer

STOP HERE and wait for their response before continuing.
Remember: DO NOT include OBSERVATION section. Only show THOUGHT and ACTION.

**Your Response (Thought → Action only):**
"""
            
            self.messages.append({"role": "user", "content": memory_context})
            
            # Get AI response with ReAct reasoning
            response = self.llm.invoke(self.messages[-5:] if len(self.messages) > 5 else self.messages)
            
            # Apply SymPy post-processing to ensure LaTeX formatting
            response_text = self._format_with_sympy(response.content)
            
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
