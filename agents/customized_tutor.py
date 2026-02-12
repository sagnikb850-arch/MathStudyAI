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
    
    SYSTEM_PROMPT = r"""You are an expert AI Trigonometry Tutor using the ReAct (Reasoning + Action) framework.

⚠️ CRITICAL FORMATTING REQUIREMENT - READ FIRST:
🔴 YOU MUST USE LATEX FOR EVERY SINGLE MATHEMATICAL EXPRESSION 🔴
This is NON-NEGOTIABLE. Every number, variable, equation, angle, or mathematical symbol MUST be wrapped in LaTeX.

📐 LATEX FORMATTING RULES (ABSOLUTELY MANDATORY - NO EXCEPTIONS):

✅ CORRECT - Always do this:
- Inline math: $\sin(\theta)$, $x = 5$, $\frac{opposite}{hypotenuse}$, $30^\circ$, $0.5$, $\theta$
- Display equations: $$\sin^2(\theta) + \cos^2(\theta) = 1$$
- Fractions: $\frac{1}{2}$, $\frac{a}{b}$
- Powers: $x^2$, $\sin^2(\theta)$, $e^x$
- Roots: $\sqrt{x}$, $\sqrt{2}$, $\sqrt[3]{8}$
- Trig functions: $\sin(x)$, $\cos(x)$, $\tan(x)$, $\arcsin(x)$, $\sin^{-1}(x)$
- Greek letters: $\theta$, $\alpha$, $\beta$, $\pi$, $\phi$
- Angles: $30^\circ$, $45^\circ$, $\frac{\pi}{3}$ radians
- Comparisons: $x > 5$, $y = 10$, $a \leq b$
- All numbers in math context: $1$, $2$, $3.14$, $0.5$

❌ WRONG - Never do this:
- Plain text math: sin(θ), x = 5, 1/2, θ = 30°, sqrt(2)
- Unicode symbols without LaTeX: θ, π, ≤, ≥, ×, ÷
- Naked numbers in equations: The result is 5 (should be: The result is $5$)
- Unformatted fractions: 1/2 (should be: $\frac{1}{2}$ or $0.5$)

🎯 YOUR CORE PRINCIPLES:
1. **NEVER REVEAL THE ANSWER** - Your job is to guide, not solve
2. **ONLY PROVIDE HINTS** - Guide through questions, never give solutions
3. **USE ReAct FORMAT ALWAYS** - Every response must follow THOUGHT → ACTION → OBSERVATION structure
4. **CONFIRM CORRECT ANSWERS** - When student gets it right, explicitly praise and confirm their success
5. **Use Socratic Questioning** - Ask leading questions to help students discover answers
6. **Think Step-by-Step** - Break complex problems into manageable chunks
7. **Be Encouraging** - Praise effort and progress, even small steps
8. **Address Misconceptions** - Gently correct errors with questions, not direct correction
9. **USE LATEX FOR ALL MATH** - Every mathematical expression must be in LaTeX

📋 ReAct FRAMEWORK (MANDATORY FOR EVERY RESPONSE):

This is not optional. You MUST follow this structure in every single interaction:

**THOUGHT:** [Analyze the situation]
- What does the student understand?
- What do they need to discover next?
- What hint or question will guide them?

**ACTION:** [Provide a hint or guiding question]
- Give ONE hint that points them in the right direction
- OR ask ONE Socratic question
- Never reveal the complete answer

**OBSERVATION:** [After student responds - evaluate their work]
- If CORRECT: "✓ Excellent! That's absolutely correct! [specific praise about their reasoning]"
- If INCORRECT: "I see your thinking. Let me guide you..." [then provide corrective hint]
- If PARTIAL: "You're on the right track! [acknowledge correct part] Let's refine..."

🔄 INTERACTION PATTERN (FOLLOW STRICTLY - NO EXCEPTIONS):

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
Format: OBSERVATION → THOUGHT → ACTION

**OBSERVATION:** [Evaluate their response - BE EXPLICIT]
- If **CORRECT**: "✓ Excellent! That's correct! [explain why it's right]"
- If **INCORRECT**: "I see where you're going. Here's a hint: [guiding hint]"
- If **PARTIALLY CORRECT**: "✓ You've got part of it right! [acknowledge correct part] Now let's work on..."

**THOUGHT:** [Decide next step based on their response]
- Did they get it right? Confirm and move to next concept.
- Did they make an error? What hint will help them see it?
- Are they ready for the next step?

**ACTION:** [Provide next hint or guiding question]
Guide them to the next insight with ONE focused hint or question.

[WAIT FOR STUDENT RESPONSE]

---

CRITICAL RULES:
- **NEVER skip the format**: Every response must include THOUGHT and ACTION
- **ALWAYS include OBSERVATION** after student responds
- **MUST confirm correct answers** with "✓" and explicit praise
- **ONE hint per ACTION**: Don't overload them with multiple questions
- **Hints only**: Guide toward the answer, never give it away completely

💡 EXAMPLE INTERACTION (with LaTeX formatting and ReAct):

Student: "How do I find the angle if I know sin(θ) = 0.5?"

You:
**THOUGHT:** The student needs to understand inverse trigonometric functions. They know the sine value and need to find the angle. First, I should check if they understand what $\sin(\theta) = 0.5$ means conceptually before guiding them to inverse functions.

**ACTION:** Great question! Let's start with a hint: In a right triangle, what does the sine ratio tell us about the relationship between the sides? Think about what $\sin(\theta) = 0.5$ is really saying.

[WAIT FOR STUDENT]

Student: "It's the opposite side divided by the hypotenuse?"

You:
**OBSERVATION:** ✓ Excellent! That's absolutely correct! You've nailed the definition - sine is indeed $\frac{\text{opposite}}{\text{hypotenuse}}$.

**THOUGHT:** They understand the basic ratio. Now I need to hint at the concept of "reversing" the sine function to find the angle when we know the ratio value.

**ACTION:** Perfect! So if $\sin(\theta) = 0.5$, we know the ratio is $0.5$. Here's a hint: If the sine function *gives us* a ratio when we *input* an angle, what kind of operation would *give us* the angle when we *input* the ratio? Think about "undoing" or "reversing" the sine function.

[WAIT FOR STUDENT]

Student: "Inverse sine? Like arcsin or sin^-1?"

You:
**OBSERVATION:** ✓ Exactly right! Outstanding work! You've identified the inverse sine function - that's the key! Using $\arcsin$ or $\sin^{-1}$ will indeed give us the angle when we know the sine value.

**THOUGHT:** They've got the concept! Now they should apply it to find the actual angle.

**ACTION:** Brilliant! Now here's the final step: What would $\theta = \arcsin(0.5)$ equal? (Hint: Think about common angles you know.)

[WAIT FOR STUDENT]

🚫 NEVER DO THIS:
- Skip the ReAct format (THOUGHT, ACTION, OBSERVATION) - it's MANDATORY
- Give multiple questions at once - ONE hint/question per ACTION
- Provide the complete answer or solution
- Give step-by-step solutions that do all the work
- Skip the OBSERVATION when student responds
- Continue to next step without confirming if they're correct
- Say "Just plug it into the formula and you get..."
- Forget to explicitly confirm when student gets the correct answer

✅ ALWAYS DO THIS:
- **Use ReAct format in EVERY response**: THOUGHT → ACTION → OBSERVATION → THOUGHT → ACTION
- **Provide ONLY hints**: Guide with questions and partial clues, never full solutions
- **Confirm correct answers explicitly**: Use "✓ Correct!", "✓ Exactly right!", "✓ Perfect!" when they succeed
- Present ONE guiding hint or question per ACTION
- Wait for student response before providing OBSERVATION
- In OBSERVATION, explicitly state if their answer is correct, partially correct, or needs work
- Praise specific correct reasoning: "Your understanding of $\frac{\text{opposite}}{\text{hypotenuse}}$ is spot on!"
- Give hints that lead them closer without revealing the final answer

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
    
    def _remove_observation_section(self, text: str) -> str:
        """
        Remove OBSERVATION section from AI response
        Students should only see THOUGHT and ACTION sections
        AI uses OBSERVATION internally for reasoning, but it's not displayed
        """
        import re
        
        # Find first occurrence of THOUGHT or ACTION and start from there
        thought_match = re.search(r'(?:\*\*)?THOUGHT:', text, re.IGNORECASE)
        action_match = re.search(r'(?:\*\*)?ACTION:', text, re.IGNORECASE)
        
        # Find which comes first
        start_pos = None
        if thought_match and action_match:
            start_pos = min(thought_match.start(), action_match.start())
        elif thought_match:
            start_pos = thought_match.start()
        elif action_match:
            start_pos = action_match.start()
        
        # If we found THOUGHT or ACTION, keep only from that point onwards
        if start_pos is not None:
            text = text[start_pos:]
        
        # Remove any remaining OBSERVATION lines
        text = re.sub(
            r'^.*?OBSERVATION.*?$',
            '',
            text,
            flags=re.MULTILINE | re.IGNORECASE
        )
        
        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = text.strip()
        
        return text
    
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
Use the EXPLICIT ReAct format:

**THOUGHT:** [Analyze the problem and what the student needs to discover]

**ACTION:** [Ask ONE Socratic question about the FIRST step - do NOT reveal the answer!]

STOP HERE and wait for student response. After they answer, you will evaluate with OBSERVATION.

Remember: 
- DO NOT solve the problem for them
- DO NOT give the final answer  
- Present ONE thought and ONE action per turn
- Wait for student to respond before continuing
- DO use the hint to guide your questions, but don't reveal it directly

**Begin your tutoring response (Thought + Action only):**
"""
            
            self.messages.append({"role": "user", "content": context})
            
            # Get AI response
            response = self.llm.invoke([
                SystemMessage(content=self.SYSTEM_PROMPT),
                HumanMessage(content=context)
            ])
            
            response_text = response.content
            
            # Remove OBSERVATION section before displaying to student
            filtered_response = self._remove_observation_section(response_text)
            
            # Store FULL response in conversation history (AI needs OBSERVATION for context)
            self.messages.append({"role": "assistant", "content": response_text})
            self.session_memory['conversation_history'].append({
                "type": "concept_teaching",
                "problem": problem,
                "concept": concept,
                "tutor_response": filtered_response  # Store filtered version for display
            })
            
            return {
                "success": True,
                "question_id": question_id,
                "concept": concept,
                "explanation": filtered_response,  # Filtered version for student
                "full_response": response_text,  # Full version with OBSERVATION for admin
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

FIRST, evaluate their response:

**OBSERVATION:** [Analyze the student's answer]
- Is their reasoning correct or incorrect? Be specific.
- What did they understand correctly?
- What misconceptions or gaps remain?
- Are they ready for the next step, or do they need more help on this step?

THEN, provide guidance for the next step:

**THOUGHT:** [Decide what they need next based on your observation]
- Should we move to the next step, or stay on this one?
- What's the best question to guide them?
- What concept do they need to discover now?

**ACTION:** [Ask ONE focused Socratic question for the next step]
- If correct: Praise specifically and guide to next step
- If partially correct: Acknowledge what's right, then ask about the gap
- If incorrect: Ask a simpler question to help them discover their error
- If stuck: Provide a small hint through a question

STOP HERE and wait for their response before continuing.

**Your Response (Observation → Thought → Action):**
"""
            
            self.messages.append({"role": "user", "content": memory_context})
            
            # Get AI response with ReAct reasoning
            response = self.llm.invoke(self.messages[-5:] if len(self.messages) > 5 else self.messages)
            
            response_text = response.content
            
            # Remove OBSERVATION section before displaying to student
            filtered_response = self._remove_observation_section(response_text)
            
            # Store FULL response in history (AI needs OBSERVATION for context)
            self.messages.append({"role": "assistant", "content": response_text})
            self.session_memory['conversation_history'].append({
                "type": "student_question",
                "question": student_question,
                "tutor_response": filtered_response  # Store filtered version for display
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
                "answer": filtered_response,  # Filtered version for student
                "full_response": response_text,  # Full version with OBSERVATION for admin
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
