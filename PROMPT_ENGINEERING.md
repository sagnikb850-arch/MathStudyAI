# 🎯 AI Prompt Engineering Guide for Math Study AI

This guide covers how to optimize prompts for teaching mathematics with AI.

## Table of Contents
1. [System Prompt Structure](#system-prompt-structure)
2. [Prompt Engineering Techniques](#prompt-engineering-techniques)
3. [Examples & Templates](#examples--templates)
4. [Evaluation Metrics](#evaluation-metrics)

---

## System Prompt Structure

### Good System Prompt Template

```
You are [ROLE] specialized in [DOMAIN].

Your responsibilities:
1. [Task 1]
2. [Task 2]
3. [Task 3]

Your approach:
- [Approach 1]
- [Approach 2]
- [Approach 3]

When answering:
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]
```

### Current Math Tutor Prompt

Located in `agent/math_agent.py`:

```python
SYSTEM_PROMPT = """You are an expert mathematics tutor AI assistant designed 
to help students learn and understand mathematical concepts...
```

---

## Prompt Engineering Techniques

### 1. Chain-of-Thought Prompting
Makes the AI show its reasoning step-by-step.

**Poor:**
```
Solve 3x + 5 = 14
```

**Better:**
```
Solve 3x + 5 = 14.
First, identify what we're solving for.
Then, work through each step.
Finally, verify the answer.
```

### 2. Few-Shot Prompting
Provide examples of desired output.

```
I will give you math problems to solve. Here's an example:

Problem: Solve 2x + 3 = 7
Solution: 
- Subtract 3 from both sides: 2x = 4
- Divide by 2: x = 2
- Check: 2(2) + 3 = 7 ✓

Now solve this: 3x - 5 = 10
```

### 3. Structured Output
Request specific format.

```
Explain derivatives using this structure:
1. **Definition**: [One sentence definition]
2. **Intuition**: [Why it matters]
3. **Formula**: [Mathematical notation]
4. **Example**: [Concrete example]
5. **Application**: [Real-world use]
```

### 4. Role-Playing
Give the AI a specific persona.

```
You are a patient high school math tutor who has taught 
thousands of students. You know common misconceptions and 
how to overcome them. Explain derivatives to a confused student.
```

### 5. Constraint-Based Prompting
Set boundaries for the response.

```
Explain calculus in exactly 3 paragraphs.
Use no more than 5 mathematical symbols.
Avoid using the word "integration" or "derivation".
```

---

## Examples & Templates

### Template 1: Explain Domain (for "What is X?" questions)

```
Explain [CONCEPT] for [LEVEL] students.

Structure:
1. Start with a simple analogy or real-world example
2. Give the formal definition
3. Show 2-3 worked examples
4. Common mistakes to avoid
5. How this connects to other concepts

Keep it simple but mathematically accurate.
```

**Usage:**
```python
prompt = f"""
Explain derivatives for intermediate students.

Structure:
1. Start with a simple analogy or real-world example
2. Give the formal definition
3. Show 2-3 worked examples
4. Common mistakes to avoid
5. How this connects to other concepts

Keep it simple but mathematically accurate.
"""
```

### Template 2: Problem Solving

```
Solve this problem step-by-step: [PROBLEM]

Before solving:
- Identify what's given
- Identify what we need to find
- Check for relevant formulas or concepts

Solution:
- Work through each algebraic step
- Show all work
- Explain WHY each step makes sense

After solving:
- Verify the answer
- Check if it's reasonable
- Show an alternative approach if possible
```

### Template 3: Concept Comparison

```
Compare and contrast [CONCEPT_A] and [CONCEPT_B].

For each concept:
- Definition
- Key properties
- Visual representation
- Example
- When to use it

Then explain:
- Similarities
- Differences
- Which one should I use when?
```

### Template 4: Progressive Difficulty

```
Teach me about [CONCEPT] at multiple difficulty levels.

Level 1 (Intuition): Explain using simple language and analogies
Level 2 (Understanding): Add formal definitions and basic examples
Level 3 (Application): Show how to use this in problems
Level 4 (Advanced): Include edge cases and advanced applications

Adjust depth based on my answers.
```

---

## Advanced Techniques

### Multi-Shot Prompting with Feedback

```
I'll show you examples of good and bad explanations.

[GOOD EXAMPLE]

[BAD EXAMPLE]

Now explain [CONCEPT] following the good example style.
```

### Constraint Satisfaction

```
Explain quadratic equations with these constraints:
- Use at least one visual description
- Include exactly 2 numerical examples
- Avoid using the term "parabola"
- Keep explanation under 300 words
- Start with the most common use case
```

### Generation with Verification

```
Solve 3x² + 2x - 5 = 0

Requirements:
1. Show all algebraic steps
2. After solving, substitute answer back to verify
3. If verification fails, debug and fix
4. Provide alternative solving method
```

---

## Prompt Templates by Use Case

### Understanding Check
```
I want to check my understanding of [CONCEPT].
Describe it in your own words, then ask me a question
to see if I understand the key idea.
```

### Mistake Diagnosis
```
I got [ANSWER] but the answer should be [CORRECT_ANSWER].
Where did I go wrong? Show me:
1. Where my logic broke down
2. The correct approach
3. Why my approach was wrong
```

### Conceptual Bridge
```
I understand [CONCEPT_A] but I'm struggling with [CONCEPT_B].
Show me how these are related and how mastering [A] helps with [B].
```

### Practice Problem Generation
```
Generate 3 practice problems about [CONCEPT] at [DIFFICULTY] level.
For each problem:
- Problem statement
- Key concepts needed
- Solution approach (hint, don't solve)
- Full solution
```

---

## Evaluation Metrics

### How to Measure Prompt Quality

#### 1. Clarity
- Is explanation easy to follow?
- Are steps logical?
- Can a beginner understand it?

#### 2. Accuracy  
- Are calculations correct?
- Is mathematics rigorous?
- Are definitions precise?

#### 3. Completeness
- Does it answer the question fully?
- Are edge cases covered?
- Are examples sufficient?

#### 4. Engagement
- Does it maintain interest?
- Are explanations relatable?
- Does it encourage further learning?

### Testing Your Prompts

```python
def evaluate_response(response):
    """Evaluate AI response quality"""
    checks = {
        'has_steps': 'step' in response.lower() or '1.' in response,
        'has_examples': 'example' in response.lower(),
        'has_verification': 'check' in response.lower() or 'verify' in response.lower(),
        'length_ok': 200 < len(response) < 2000,
        'no_jargon': not too_much_technical_language(response),
        'clear': passes_readability_test(response)
    }
    return sum(checks.values()) / len(checks)
```

---

## Best Practices

### ✅ DO
- Be specific about the level (beginner/intermediate/advanced)
- Ask for examples
- Request verification of answers
- Use structured formats
- Give context about learner's background
- Ask for multiple approaches

### ❌ DON'T
- Use vague questions
- Assume prior knowledge
- Ask for "simple" explanations (define simple)
- Overload with constraints
- Mix multiple unrelated concepts
- Ask for understanding without examples

---

## Tips for Math Teaching

### For Explanations
```
"Explain [CONCEPT] as if teaching to a student who:
- Already understands [PREREQUISITE]
- Struggles with [COMMON_MISCONCEPTION]
- Learns best through [LEARNING_STYLE]
- Wants to understand the 'why', not just the 'how'"
```

### For Problem Solving
```
"Solve [PROBLEM] using:
- The [METHOD] approach
- Show all work
- At each step, explain why that operation is valid
- Highlight the key insight
- Show common mistakes at this step"
```

### For Conceptual Understanding
```
"Compare [CONCEPT_A] and [CONCEPT_B]:
- How are they similar?
- How are they fundamentally different?
- When do we use one vs the other?
- What's a common misconception about the difference?"
```

---

## Customizing for Your Needs

### Change Teaching Style in System Prompt

**Socratic Method:**
```python
SYSTEM_PROMPT = """Guide students by asking strategic questions
that help them discover the answer themselves, rather than
telling them the answer directly."""
```

**Formal Academic:**
```python
SYSTEM_PROMPT = """Provide mathematically rigorous explanations
using formal definitions, theorems, and proofs. Assume calculus-level
mathematical maturity."""
```

**Intuitive Visual:**
```python
SYSTEM_PROMPT = """Explain concepts primarily through visual 
descriptions, analogies, and intuitive examples before introducing
formal definitions."""
```

**Applied Practical:**
```python
SYSTEM_PROMPT = """Focus on practical applications and real-world
problems. Show how this mathematics is used in engineering, 
finance, science, and industry."""
```

---

## Resources for Further Learning

- OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- Few-shot Prompting: https://github.com/dair-ai/Prompt-Engineering-Guide
- Chain-of-Thought Prompting Paper: https://arxiv.org/abs/2201.11903
- Persona-based Prompting: https://arxiv.org/abs/2305.10317

---

**Pro Tip:** Test your prompts with multiple models to see which produces the best results for your specific use case!
