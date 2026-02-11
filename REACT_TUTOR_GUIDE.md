# 🤖 ReAct Tutor Agent - Technical Documentation

## Overview

The Customized Tutor Agent has been redesigned to use **ReAct (Reasoning + Action)** prompting combined with **Socratic questioning** to guide students through problems without revealing answers.

---

## Architecture

### 1. ReAct Framework

**ReAct = Reasoning + Action**

For every student interaction, the agent follows this pattern:

```
THOUGHT → ACTION → OBSERVATION → (repeat)
```

#### THOUGHT Phase
- Analyze the student's question/response
- Identify what concept is involved
- Determine what sub-steps exist
- Assess student's current understanding level
- Check for misconceptions

#### ACTION Phase
- Break problem into smaller steps
- Ask Socratic questions to guide discovery
- Provide hints (without revealing answers)
- Use tools if needed (SymPy, graphing descriptions)
- Adjust approach based on student level

#### OBSERVATION Phase
- Assess student's response
- Check if they understood the current step
- Detect misconceptions
- Decide if ready for next step
- Update memory accordingly

---

## Memory Management

### Student Memory (Persistent)
Stores student-specific information across sessions:

```python
{
    "weak_areas": ["sine", "inverse functions"],
    "strong_areas": ["basic angles", "unit circle"],
    "difficulty_level": "intermediate",
    "misconceptions": ["confuses sin⁻¹ with 1/sin"],
    "learning_style": "visual",
    "progress_notes": []
}
```

### Session Memory (Current Context)
Tracks the current problem-solving session:

```python
{
    "current_problem": "Find the angle when sin(θ) = 0.5",
    "problem_steps": [
        "Recognize we need inverse sine",
        "Apply arcsin to both sides",
        "Calculate arcsin(0.5)",
        "Convert to degrees if needed"
    ],
    "completed_steps": ["Recognize we need inverse sine"],
    "current_step": "Apply arcsin to both sides",
    "student_attempts": [...],
    "conversation_history": [...],
    "tools_used": []
}
```

---

## Socratic Questioning Examples

### ❌ Old Approach (Direct Answer):
```
Student: "How do I find the angle when sin(θ) = 0.5?"
Tutor: "Use inverse sine! arcsin(0.5) = 30°. Here's the step-by-step solution..."
```

### ✅ New Approach (Socratic Guidance):
```
Student: "How do I find the angle when sin(θ) = 0.5?"

Tutor [THOUGHT]: They need to discover inverse functions. 
                  Start with what they know about sine.

Tutor [ACTION]: "Great question! Let's think about this together. 
                 When we know the sine value is 0.5, what do we 
                 want to find? What part of the triangle or angle 
                 are we looking for?"

Student: "We want to find the angleθ?"

Tutor [OBSERVATION]: Good, they understand the goal.

Tutor [ACTION]: "Exactly! Now, if sine gives us 0.5 when we input 
                 the angle, what operation might 'reverse' that to 
                 get the angle back? Think about how we reverse 
                 other operations in math..."

Student: "Maybe the inverse?"

Tutor [OBSERVATION]: Excellent progress!

Tutor [ACTION]: "Perfect thinking! We use inverse sine, written as 
                 sin⁻¹ or arcsin. Now, what do you think we should 
                 do with arcsin(0.5)?"
```

---

## Key Features

### 1. Never Reveals Answers
- All responses are questions or hints
- Guides students to discover solutions themselves
- Redirects direct answer requests

### 2. Step-by-Step Problem Decomposition
```python
Problem: "Find sin(45°) in a right triangle"

Auto-decomposed steps:
1. Identify triangle parts
2. Recall SOH (Sine = Opposite/Hypotenuse)
3. Set up equation
4. Solve for unknown
```

### 3. Tools Integration

#### SymPy (Symbolic Math)
```python
# When student struggles with identities
response = agent._use_sympy_tool("sin(x)**2 + cos(x)**2")
# Returns: "SymPy shows: 1"
```

#### Graph Visualization
```python
# Describe what graphs look like
response = agent._describe_graph("sin(x)", "0° to 360°")
# Returns: "The sine wave starts at 0, rises to 1 at 90°..."
```

### 4. Misconception Detection

The agent tracks common misconceptions:

```python
# If student confuses sin⁻¹(x) with 1/sin(x)
if "1/sin" in student_response:
    agent.student_memory['misconceptions'].append("confuses inverse with reciprocal")
    # Tutor uses question to clarify without saying "wrong"
```

### 5. Progress Tracking

```python
# Shows student their progress
"You've completed 2/4 steps! Keep going!"

# Internally tracks:
completed_steps: ["Identify triangle", "Recall SOH"]
current_step: "Set up equation"
remaining: ["Solve for unknown"]
```

---

## Configuration

### Model Selection

The tutor uses **GPT-4o** for:
- Better reasoning capabilities
- Superior Socratic questioning
- More reliable ReAct framework adherence

```python
self.llm = ChatOpenAI(
    model_name="gpt-4o",  # Not gpt-4o-mini
    temperature=0.7,      # Balanced creativity
    max_tokens=1024
)
```

### Temperature Setting

- **0.7** = Balanced between consistency and creativity
- Higher → More varied questions
- Lower → More predictable responses

---

## Usage Example

### In app.py (Group 1 Learning):

```python
tutor = get_customized_tutor()

# Initial concept teaching
response = tutor.teach_concept(
    question_id=1,
    question={
        'question': 'What is sin(30°)?',
        'concept': 'Basic Trigonometric Ratios',
        'hint': 'Use SOH-CAH-TOA and special angles'
    },
    student_level="intermediate"
)

# Display the Socratic question
st.write(response['explanation'])

# Student responds
student_answer = st.text_input("Your response:")

# Continue dialogue
follow_up = tutor.answer_student_question(
    student_question=student_answer
)

st.write(follow_up['answer'])
```

---

## Comparison: Old vs New

| Feature | Old Tutor | New ReAct Tutor |
|---------|-----------|-----------------|
| **Approach** | Direct teaching | Socratic questioning |
| **Answers** | Provides full solutions | Never reveals answers |
| **Problem Solving** | Shows complete steps | Guides step-by-step discovery |
| **Memory** | Basic chat history | Dual memory system |
| **Tools** | None | SymPy, graph descriptions |
| **Reasoning** | Single-turn responses | Multi-turn ReAct cycles |
| **Misconceptions** | Not tracked | Actively tracked & addressed |
| **Progress** | Not visible | Step-by-step tracking |

---

## Benefits for Students

### 1. Deep Understanding
Students discover answers themselves → better retention

### 2. Critical Thinking
Socratic questions force analytical thinking

### 3. Confidence Building
Praise at every step → positive reinforcement

### 4. Personalized Learning
Adapts to weak areas and misconceptions

### 5. Active Learning
Students engage, not passively receive information

---

## Benefits for Research Study

### Measurable Differences

Group 1 (ReAct Tutor) vs Group 2 (ChatGPT) comparison:

| Metric | Group 1 (ReAct) | Group 2 (ChatGPT) |
|--------|-----------------|-------------------|
| **Learning Depth** | Socratic discovery | Direct Q&A |
| **Engagement** | High (multi-turn) | Variable |
| **Retention** | Higher (active learning) | Lower (passive) |
| **Misconceptions** | Addressed proactively | May persist |
| **Answer Dependency** | None (never given) | High (always given) |

---

## Troubleshooting

### Agent Reveals Answers

**Problem**: Agent gives away solutions

**Fix**: Check system prompt is properly loaded
```python
# Verify prompt includes:
"NEVER REVEAL THE ANSWER"
"Use Socratic Questioning"
```

### Tools Not Working

**Problem**: SymPy errors

**Fix**: Install sympy
```bash
pip install sympy
```

### Memory Not Persisting

**Problem**: Student context lost between questions

**Fix**: Ensure tutor instance is cached
```python
@st.cache_resource
def get_customized_tutor():
    return CustomizedTutorAgent()
```

---

## Future Enhancements

### 1. Real-Time Graph Generation
```python
import matplotlib.pyplot as plt
# Generate actual plots instead of descriptions
```

### 2. Advanced Tools
- WolframAlpha API integration
- GeoGebra embedding
- Interactive triangle diagrams

### 3. Emotion Detection
```python
# Detect frustration, adjust encouragement level
if student_frustration_high:
    provide_easier_hint()
```

### 4. Adaptive Difficulty
```python
# Automatically adjust based on success rate
if success_rate < 0.4:
    simplify_questions()
```

---

## References

- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Synergizing Reasoning and Acting in Language Models
- Socratic Method in AI Education
- GPT-4o Capabilities Documentation

---

**The tutor now embodies the Socratic ideal: "I cannot teach anybody anything. I can only make them think."**
