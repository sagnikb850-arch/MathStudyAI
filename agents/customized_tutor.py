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
    Enhanced with adaptive hints and struggle tracking.
    """
    
    SYSTEM_PROMPT = r"""You are an expert AI Trigonometry Tutor using the ReAct (Reasoning + Action) framework.

⚠️ CRITICAL FORMATTING REQUIREMENT - READ FIRST:
🔴 YOU MUST USE LATEX FOR EVERY SINGLE MATHEMATICAL EXPRESSION 🔴
This is NON-NEGOTIABLE. Every number, variable, equation, angle, or mathematical symbol MUST be wrapped in LaTeX.

📐 LATEX FORMATTING RULES (ABSOLUTELY MANDATORY - NO EXCEPTIONS):

✅ CORRECT - Always do this:
- Inline math: $\sin(\theta)$, $x = 5$, $\frac{opposite}{hypotenuse}$, $30^\circ$, $0.5$, $\theta$
- Display equations: $$\sin^2(\theta) + \cos^2(\theta) = 1$$

🎯 ADAPTIVE HINT SYSTEM:
Provide clear mathematical guidance appropriate to student's understanding level.
Use precise mathematical language with helpful explanations when needed.
If student struggles, provide alternative explanations or different perspectives on the concept.

🔍 STRUGGLE DETECTION:
Watch for signs of struggle:
- "I don't understand", "I'm confused", "This is hard"
- Incorrect answers repeated
- Asking for same concept multiple times
- Vague or very short responses
When you detect struggle, become MORE encouraging and provide ALTERNATIVE mathematical perspectives or break the problem into smaller steps.

🚫 ABSOLUTELY FORBIDDEN - NEVER USE:
- Childish analogies (merry-go-rounds, playgrounds, animals, toys)
- Oversimplified stories or narratives
- Emojis (EXCEPT ✓ for marking correct answers)
- Patronizing language or baby talk
- Phrases like "Imagine...", "Think of it like...", "It's just like..."
Keep your language professional, clear, and mathematically precise.

✨ PROGRESS CELEBRATION:
ACTIVELY PRAISE when students:
- Use knowledge from previous hints correctly
- Show understanding of a concept
- Make connections between ideas
- Attempt to solve problems independently
- Ask thoughtful follow-up questions
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
- Internally note your observations but DO NOT write "OBSERVATION" in output

**ACTION:** [Provide a hint or guiding question]
- Give ONE hint that points them in the right direction
- OR ask ONE Socratic question
- Never reveal the complete answer

🚨🚨🚨 CRITICAL OUTPUT FORMAT RULES 🚨🚨🚨

YOU MUST NEVER WRITE THE WORD "OBSERVATION" IN YOUR RESPONSE TO STUDENTS!

FORBIDDEN: Do NOT write "**OBSERVATION:**" or "OBSERVATION:" anywhere!
REQUIRED: Only write "**THOUGHT:**" and "**ACTION:**"

Internal Process (think this, don't write it):
1. Observe/evaluate student's response mentally
2. Use those observations to inform your THOUGHT
3. Output only THOUGHT and ACTION sections

🔄 REQUIRED OUTPUT FORMAT (USE THIS EXACT STRUCTURE):

**INITIAL RESPONSE:**
```
**THOUGHT:** [What the student needs to understand - acknowledge their attempt if any]

**ACTION:** [ONE guiding question or hint]
```

**AFTER STUDENT RESPONDS:**
```
**THOUGHT:** [Evaluate their response and decide next step]
- If CORRECT: Start with "✓ Excellent! That's correct! [specific praise]"
- If INCORRECT: Start with "I see your thinking. Let's explore this..."
- If PARTIAL: Start with "✓ You're on the right track! [acknowledge correct part]"

**ACTION:** [ONE next hint or guiding question]
```

CRITICAL RULES:
- ❌ NEVER write "OBSERVATION" in your output
- ✅ ALWAYS start with "**THOUGHT:**"
- ✅ ALWAYS follow with "**ACTION:**"
- ✅ Include praise/feedback in THOUGHT section
- ✅ ONE hint per ACTION
- ❌ Never give away the complete answer

💡 EXAMPLE INTERACTION (with LaTeX formatting and ReAct):

Student: "How do I find the angle if I know sin(θ) = 0.5?"

You:
**THOUGHT:** The student needs to understand inverse trigonometric functions. They know the sine value and need to find the angle. First, I should check if they understand what $\sin(\theta) = 0.5$ means conceptually before guiding them to inverse functions.

**ACTION:** In a right triangle, what does the sine ratio tell us about the relationship between the sides? Consider what $\sin(\theta) = 0.5$ represents mathematically.

[WAIT FOR STUDENT]

Student: "It's the opposite side divided by the hypotenuse?"

You:
**THOUGHT:** ✓ Correct! They understand the basic ratio. Now I need to guide them toward the concept of inverse functions - "reversing" the sine function to find the angle when we know the ratio value.

**ACTION:** Exactly right - sine is $\frac{\text{opposite}}{\text{hypotenuse}}$. Now, if the sine function gives us a ratio when we input an angle, what operation would give us the angle when we input the ratio? Think about reversing the sine function.

[WAIT FOR STUDENT]

Student: "Inverse sine? Like arcsin or sin^-1?"

You:
**THOUGHT:** ✓ Perfect! They've identified the inverse sine function. Now they should apply it to find the actual angle value.

**ACTION:** Correct! Using $\arcsin$ or $\sin^{-1}$ gives us the angle from the sine value. What would $\theta = \arcsin(0.5)$ equal? Consider the common angle values you know.

[WAIT FOR STUDENT]

🚫 NEVER DO THIS:
- Skip the ReAct format (THOUGHT, ACTION) - it's MANDATORY
- Give multiple questions at once - ONE hint/question per ACTION
- Provide the complete answer or solution
- Give step-by-step solutions that do all the work
- Continue to next step without acknowledging student's response in THOUGHT
- Say "Just plug it into the formula and you get..."
- Use childish analogies (playgrounds, merry-go-rounds, animals, toys)
- Use phrases like "Imagine a...", "Think of it like a...", "It's just like..."
- Overuse emojis (only ✓ is acceptable for confirming correct answers)
- Be patronizing or oversimplify to the point of being insulting

✅ ALWAYS DO THIS:
- **Use ReAct format in EVERY response**: THOUGHT → ACTION only
- **Include feedback in THOUGHT**: Acknowledge and evaluate student's response in your reasoning
- **Provide ONLY hints**: Guide with questions and partial clues, never full solutions
- **Confirm correct answers in THOUGHT**: Use "✓ Correct!", "✓ Exactly right!", "✓ Perfect!" when they succeed
- Present ONE guiding hint or question per ACTION
- Evaluate student's response mentally and incorporate it into your THOUGHT
- Praise specific correct reasoning: "Your understanding of $\frac{\text{opposite}}{\text{hypotenuse}}$ is spot on!"
- Give hints that lead them closer without revealing the final answer
- Maintain a professional, mathematically precise tone

🧰 AVAILABLE TOOLS (Use when helpful, but don't over-rely):
1. **SymPy**: For symbolic manipulation (e.g., "Let's verify this identity using SymPy: $\sin^2(\theta) + \cos^2(\theta)$")
2. **Graphing**: Describe graph properties (e.g., "Consider the graph of $\sin(\theta)$ from $0°$ to $90°$ - how does the value change?")

💾 MEMORY:
- Remember student's weak areas from their assessment
- Track misconceptions mentioned in this session
- Adapt difficulty based on their responses
- Reference previous parts of the conversation

🎓 YOUR TONE:
- Professional, clear, and mathematically precise
- Warm and encouraging, but never patronizing
- Excited about mathematical discovery
- Respectful of student intelligence
- Celebrate progress with specific mathematical praise
- Use phrases like "Excellent reasoning!", "You're making progress!", "That's a good observation!"
- Avoid overly enthusiastic or childish language
- No emojis except ✓ for confirming correctness

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
            "progress_notes": [],
            "struggle_indicators": [],  # Track when student is struggling
            "hint_level_used": "simple",  # Current hint complexity: simple, standard, advanced
            "successful_applications": [],  # Track when student uses knowledge successfully
            "concepts_mastered": [],  # Track which concepts student has understood
            "total_hints_given": 0,
            "successful_problem_solving": 0
        }
        
        # Session-specific memory (current conversation context)
        self.session_memory = {
            "current_problem": None,
            "problem_steps": [],
            "completed_steps": [],
            "current_step": None,
            "student_attempts": [],
            "conversation_history": [],
            "tools_used": [],
            "current_hint_level": "simple",  # Track current hint level for this session
            "hints_given_this_concept": 0,
            "struggle_count_this_session": 0,
            "success_count_this_session": 0,
            "last_student_mood": "neutral",  # Track if student seems frustrated/confident
            "concepts_attempted": []  # Track which concepts tried in this session
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
    
    def _detect_struggle(self, student_input: str) -> bool:
        """
        Detect if student is struggling based on their input
        """
        struggle_phrases = [
            "i don't understand", "i'm confused", "this is hard", "i don't get it",
            "what does this mean", "i'm lost", "this doesn't make sense", "help",
            "i'm stuck", "i can't", "this is difficult", "i don't know"
        ]
        
        # Check for struggle indicators
        student_lower = student_input.lower()
        is_struggling = any(phrase in student_lower for phrase in struggle_phrases)
        
        # Also check for very short responses (less than 5 words) - might indicate confusion
        if len(student_input.split()) < 5 and not is_struggling:
            is_struggling = True
            
        # Track if struggling
        if is_struggling:
            self.session_memory['struggle_count_this_session'] += 1
            self.student_memory['struggle_indicators'].append({
                'input': student_input,
                'concept': self.session_memory.get('current_problem', 'unknown'),
                'timestamp': 'current_session'
            })
            self.session_memory['last_student_mood'] = 'frustrated'
        
        return is_struggling
    
    def _detect_success(self, student_input: str, tutor_response: str) -> bool:
        """
        Detect if student is successfully using knowledge from hints
        """
        success_indicators_in_response = [
            "correct", "excellent", "great", "perfect", "right", "good job", 
            "well done", "exactly", "that's it", "you got it", "brilliant"
        ]
        
        # Check if tutor praised the student
        tutor_praised = any(indicator in tutor_response.lower() for indicator in success_indicators_in_response)
        
        # Check if student is building on previous concepts
        mathematical_terms = ["sin", "cos", "tan", "opposite", "adjacent", "hypotenuse", "angle", "triangle"]
        uses_math_concepts = any(term in student_input.lower() for term in mathematical_terms)
        
        is_successful = tutor_praised or (uses_math_concepts and len(student_input.split()) > 8)
        
        if is_successful:
            self.session_memory['success_count_this_session'] += 1
            self.student_memory['successful_applications'].append({
                'input': student_input,
                'concept': self.session_memory.get('current_problem', 'unknown'),
                'timestamp': 'current_session'
            })
            self.session_memory['last_student_mood'] = 'confident'
            
        return is_successful
    
    def _generate_different_hint(self, concept: str, previous_hints: list) -> str:
        """
        Generate a different approach to explain the same concept
        """
        # Track that we're giving multiple hints for same concept
        self.session_memory['hints_given_this_concept'] += 1
        
        # Different mathematical perspectives for common concepts
        different_approaches = {
            "sine": [
                "Consider $\\sin$ geometrically: in a right triangle, it's the ratio of the opposite side to the hypotenuse.",
                "Think of $\\sin$ on the unit circle: it represents the y-coordinate of a point at angle $\\theta$.",
                "Recall that $\\sin$ is a periodic function that oscillates between $-1$ and $1$."
            ],
            "cosine": [
                "Consider $\\cos$ geometrically: in a right triangle, it's the ratio of the adjacent side to the hypotenuse.",
                "Think of $\\cos$ on the unit circle: it represents the x-coordinate of a point at angle $\\theta$.",
                "Remember that $\\cos$ and $\\sin$ are related: $\\cos(\\theta) = \\sin(90° - \\theta)$."
            ],
            "tangent": [
                "Consider $\\tan$ as the ratio of sine to cosine: $\\tan(\\theta) = \\frac{\\sin(\\theta)}{\\cos(\\theta)}$.",
                "Think of $\\tan$ geometrically: it's the ratio of the opposite to adjacent sides in a right triangle.",
                "Recall that $\\tan$ represents the slope or steepness at angle $\\theta$."
            ]
        }
        
        for key, approaches in different_approaches.items():
            if key in concept.lower():
                # Return the next approach we haven't used
                hint_index = min(len(approaches) - 1, self.session_memory['hints_given_this_concept'] - 1)
                return approaches[hint_index]
        
        return f"🔄 Let's approach {concept} from a different mathematical perspective. Consider how this concept relates to what you already know."
    
    def _provide_guidance_after_hint(self, concept: str, hint_given: str) -> str:
        """
        Provide additional guidance to help student move toward the answer
        """
        guidance_templates = [
            "💡 Now that you have this hint, try to think: what would be your next step?",
            "🎯 Using what I just explained, can you tell me what you think we should do next?",
            "✨ Great! Now with this new understanding, what question should we ask about our triangle?",
            "🚀 Perfect! Now let's use this idea - what part of the problem can we solve first?",
            "🌟 Wonderful! Now that we understand this concept, how might we apply it to our specific problem?"
        ]
        
        # Rotate through different guidance approaches
        guidance_index = self.session_memory['hints_given_this_concept'] % len(guidance_templates)
        return guidance_templates[guidance_index]
    
    def _remove_observation_section(self, text: str) -> str:
        """
        Remove OBSERVATION section from AI response - ULTRA AGGRESSIVE
        Students should only see THOUGHT and ACTION sections
        """
        import re
        
        # Method 1: Find THOUGHT or ACTION and keep from there onwards
        thought_match = re.search(r'\*\*THOUGHT:\*\*', text, re.IGNORECASE)
        action_match = re.search(r'\*\*ACTION:\*\*', text, re.IGNORECASE)
        
        start_pos = None
        if thought_match and action_match:
            start_pos = min(thought_match.start(), action_match.start())
        elif thought_match:
            start_pos = thought_match.start()
        elif action_match:
            start_pos = action_match.start()
        
        # Keep only from THOUGHT/ACTION onwards
        if start_pos is not None:
            text = text[start_pos:]
        
        # Method 2: Remove any line containing OBSERVATION (case insensitive)
        lines = text.split('\n')
        filtered_lines = []
        skip_until_next_section = False
        
        for line in lines:
            # Check if this line starts a new section
            if re.match(r'\*\*(?:THOUGHT|ACTION):', line, re.IGNORECASE):
                skip_until_next_section = False
                filtered_lines.append(line)
            # Check if line contains OBSERVATION
            elif 'observation' in line.lower():
                skip_until_next_section = True
                continue
            # Skip lines if we're in OBSERVATION section
            elif skip_until_next_section:
                # Check if we've reached next section
                if line.strip() and (line.startswith('**') or 'THOUGHT' in line.upper() or 'ACTION' in line.upper()):
                    skip_until_next_section = False
                    filtered_lines.append(line)
                else:
                    continue
            else:
                filtered_lines.append(line)
        
        text = '\n'.join(filtered_lines)
        
        # Method 3: Final regex cleanup for any remaining OBSERVATION
        text = re.sub(
            r'(?i)\*\*observation:?\*\*[^\n]*',
            '',
            text
        )
        text = re.sub(
            r'(?i)^observation:?[^\n]*$',
            '',
            text,
            flags=re.MULTILINE
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
            self.session_memory['concepts_attempted'].append(concept)
            
            # Reset hint tracking for new concept
            self.session_memory['current_hint_level'] = 'simple'
            self.session_memory['hints_given_this_concept'] = 0
            
            # Increment total hints given
            self.student_memory['total_hints_given'] += 1
            
            # Build context-aware prompt with enhanced guidance
            context = f"""
📚 **Current Learning Context:**
- Concept: {concept}
- Student Level: {student_level}
- Weak Areas: {', '.join(self.student_memory['weak_areas']) if self.student_memory['weak_areas'] else 'None identified yet'}
- Difficulty: {self.student_memory['difficulty_level']}
- Previous Struggles: {len(self.student_memory['struggle_indicators'])} instances
- Previous Successes: {len(self.student_memory['successful_applications'])} instances
- Student Mood: {self.session_memory['last_student_mood']}

📝 **Problem/Question:** {problem}
🔑 **Key Hint Available:** {hint}

🎯 **Your Enhanced Teaching Task:**

🚨 CRITICAL: Your response MUST have ONLY two sections:
1. **THOUGHT:** [Your analysis]
2. **ACTION:** [Your guiding question]

❌ DO NOT write "OBSERVATION" anywhere in your response!
❌ DO NOT write "**OBSERVATION:**"!

✨ **Special Instructions for This Student:**
- This student has had {self.session_memory['struggle_count_this_session']} struggles this session
- This student has had {self.session_memory['success_count_this_session']} successes this session
- Current hint level should be: {self.session_memory['current_hint_level']}
- Use clear mathematical explanations appropriate to their level
- If student struggles, provide alternative perspectives or break down concepts
- Acknowledge progress and provide encouragement

Format:
**THOUGHT:** [Analyze the problem and what the student needs to discover. Focus on guiding approach. DO NOT reveal the answer.]

**ACTION:** [Ask ONE focused Socratic question to guide their thinking. Do not reveal the answer!]

After your ACTION, add: "Try to answer that, and I'll guide you to the next step! 🌟"

Remember: 
- DO NOT solve the problem for them
- DO NOT give the final answer  
- Present ONE thought and ONE action per turn
- DO NOT write the word "OBSERVATION"
- ONLY write THOUGHT and ACTION sections
- Use clear mathematical language with helpful explanations
- Include encouragement and guidance

**Begin your enhanced tutoring response now:**
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
            # Detect if student is struggling or succeeding
            is_struggling = self._detect_struggle(student_question)
            
            # Add student question to memory
            self.session_memory['student_attempts'].append({
                "question": student_question,
                "response": student_previous_response,
                "timestamp": "current",
                "struggling": is_struggling
            })
            
            # Determine hint strategy based on struggle
            if is_struggling:
                # If struggling, provide a different perspective or explanation
                different_hint = self._generate_different_hint(
                    self.session_memory.get('current_problem', ''),
                    self.session_memory.get('student_attempts', [])
                )
            
            # Build enhanced ReAct prompt with full context
            memory_context = f"""
🧠 **Enhanced Student Memory:**
- Weak Areas: {', '.join(self.student_memory['weak_areas'])}
- Known Misconceptions: {', '.join(self.student_memory['misconceptions']) if self.student_memory['misconceptions'] else 'None yet'}
- Difficulty Level: {self.student_memory['difficulty_level']}
- Total Struggles This Session: {self.session_memory['struggle_count_this_session']}
- Total Successes This Session: {self.session_memory['success_count_this_session']}
- Current Student Mood: {self.session_memory['last_student_mood']}
- Is Currently Struggling: {is_struggling}

📝 **Current Session:**
- Problem: {self.session_memory.get('current_problem', 'General question')}
- Steps in Problem: {' → '.join(self.session_memory.get('problem_steps', []))}
- Current Step: {self.session_memory.get('current_step', 'Not set')}
- Completed Steps: {' ✓ '.join(self.session_memory.get('completed_steps', [])) if self.session_memory.get('completed_steps') else 'None yet'}
- Hints Given This Concept: {self.session_memory['hints_given_this_concept']}

💬 **Recent Conversation:**
{self._format_recent_history(3)}

🎓 **Student's Current Question/Response:**
"{student_question}"
{f'Previous Response: "{student_previous_response}"' if student_previous_response else ''}

🎯 **Enhanced Response Requirements:**

🚨 CRITICAL: Your response MUST contain ONLY these two sections:
1. **THOUGHT:**
2. **ACTION:**

❌ FORBIDDEN: Do NOT write "OBSERVATION" anywhere!
❌ FORBIDDEN: Do NOT write "**OBSERVATION:**"!

✨ **Special Guidance Based on Student State:**
{'🆘 STRUGGLE DETECTED! Use extra encouragement and provide alternative explanations.' if is_struggling else '🌟 Student seems engaged! Build on their understanding.'}
- Current hint level: {self.session_memory['current_hint_level']}
- Provide clear mathematical explanations
- Use encouraging language
- If student struggling, try different perspectives or break concepts down
- If student succeeding, acknowledge and guide to next step

Format:
**THOUGHT:** [Your analysis of student's response and what they need next. Be encouraging!]

**ACTION:** [ONE guiding question or hint to help them progress. Include guidance toward next step.]

After your ACTION, add this guidance: "{self._provide_guidance_after_hint(self.session_memory.get('current_problem', 'concept'), 'current_hint')}"

Remember your core principles:
- NEVER REVEAL THE ANSWER directly
- Use Socratic questioning with simple analogies
- Be extra encouraging if student is struggling
- Celebrate any progress or understanding shown
- Guide step-by-step toward discovery

**Your Response:**"""
            
            # Get AI response with enhanced memory context
            response = self.llm.invoke([
                SystemMessage(content=self.SYSTEM_PROMPT),
                HumanMessage(content=memory_context)
            ])
            
            response_text = response.content
            
            # Remove OBSERVATION section before displaying to student
            filtered_response = self._remove_observation_section(response_text)
            
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
    
    
    def answer_additional_question(self, question: str, context: str = "") -> Dict[str, Any]:
        """
        Handle additional questions from the separate chatbox
        Provides helpful explanations while maintaining ReAct format
        """
        try:
            # Track this as an additional question
            self.session_memory['student_attempts'].append({
                "question": question,
                "type": "additional_question",
                "context": context,
                "timestamp": "current"
            })
            
            # Detect struggling
            is_struggling = self._detect_struggle(question)
            
            # Build context for additional question
            additional_context = f"""
🤔 **Additional Question Support:**
The student is asking an additional question while learning: "{question}"

🧠 **Current Learning Context:**
- Main Problem: {self.session_memory.get('current_problem', 'None')}
- Student Mood: {self.session_memory['last_student_mood']}
- Struggle Count: {self.session_memory['struggle_count_this_session']}
- Success Count: {self.session_memory['success_count_this_session']}
- Is Currently Struggling: {is_struggling}

🎯 **Your Task for Additional Question:**

🚨 CRITICAL: Your response MUST have ONLY two sections:
1. **THOUGHT:** [Your analysis]
2. **ACTION:** [Your helpful guidance]

❌ DO NOT write "OBSERVATION" anywhere!

✨ **Guidelines for Additional Questions:**
- Provide helpful mathematical guidance without giving away main problem answers
- Use clear explanations appropriate to their level
- Connect their question to the main concept if relevant
- Be extra encouraging if they're struggling with main problem
- Keep them engaged and curious about learning

Format:
**THOUGHT:** [Analyze their additional question and how it relates to their learning.]

**ACTION:** [Provide a helpful, encouraging mathematical response. Don't solve their main problem for them!]

Add this at the end: "Does this help with your understanding? Feel free to ask more questions! 💝"

**Your Response:**"""
            
            # Get AI response
            response = self.llm.invoke([
                SystemMessage(content=self.SYSTEM_PROMPT),
                HumanMessage(content=additional_context)
            ])
            
            response_text = response.content
            filtered_response = self._remove_observation_section(response_text)
            
            # Store in message history
            self.messages.append({"role": "assistant", "content": response_text})
            self.session_memory['conversation_history'].append({
                "type": "additional_question",
                "question": question,
                "tutor_response": filtered_response
            })
            
            return {
                "success": True,
                "question": question,
                "answer": filtered_response,
                "full_response": response_text,
                "type": "additional_question",
                "student_mood": self.session_memory['last_student_mood']
            }
            
        except Exception as e:
            print(f"Error in answer_additional_question: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
    
    def get_student_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of student's learning progress and state
        """
        return {
            "total_concepts_attempted": len(self.session_memory.get('concepts_attempted', [])),
            "struggle_count": self.session_memory['struggle_count_this_session'],
            "success_count": self.session_memory['success_count_this_session'],
            "current_mood": self.session_memory['last_student_mood'],
            "hint_level": self.session_memory['current_hint_level'],
            "total_hints_given": self.student_memory['total_hints_given'],
            "completed_steps": len(self.session_memory.get('completed_steps', [])),
            "total_steps": len(self.session_memory.get('problem_steps', [])),
            "concepts_mastered": self.student_memory.get('concepts_mastered', []),
            "learning_insights": {
                "is_engaged": self.session_memory['success_count_this_session'] > self.session_memory['struggle_count_this_session'],
                "needs_encouragement": self.session_memory['struggle_count_this_session'] > 2,
                "ready_for_next_level": len(self.student_memory.get('concepts_mastered', [])) > 3
            }
        }

    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.session_memory.get('conversation_history', [])
