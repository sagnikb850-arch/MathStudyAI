# 🧠 AI Model Selection Guide for Math Study AI

Choose the right AI model for your needs and budget.

## Quick Decision Matrix

```
Need the BEST quality results? → GPT-4 Turbo or Claude 3 Opus
Want to save money? → GPT-3.5 Turbo  
Want it FREE and don't mind slower? → Llama 2 (local)
Have limited compute? → GPT-3.5 or Claude 3 Haiku
Need high privacy? → Run Llama 2 locally
```

---

## Detailed Model Comparison

### 1. OpenAI GPT-4 Turbo ⭐⭐⭐⭐⭐

**Best For:** Best overall quality, complex problems

| Aspect | Details |
|--------|---------|
| **Price** | $0.01/1K input, $0.03/1K output tokens |
| **Speed** | Very fast |
| **Quality** | Excellent |
| **Context** | 128k tokens |
| **Math** | Exceptional |
| **Setup** | Easy |
| **Monthly Cost** | $5-15 (student use) |

**Pros:**
- ✅ Best reasoning for complex math
- ✅ Fastest response time
- ✅ Handles advanced topics well
- ✅ Great explanations
- ✅ Consistent quality

**Cons:**
- ❌ Requires API key (paid)
- ❌ Not free tier

**Setup:**
```bash
# .env
OPENAI_API_KEY=sk-...
AI_MODEL=openai
MODEL_NAME=gpt-4-turbo-preview
```

**Cost Estimate:**
- 100 questions/day, 500 tokens/answer = ~$1.50/day = ~$45/month
- 10 questions/day, 500 tokens/answer = ~$0.15/day = ~$4.50/month

---

### 2. OpenAI GPT-4o (Fast & Good)

**Best For:** Good balance of speed and quality

| Aspect | Details |
|--------|---------|
| **Price** | $0.005/1K input, $0.015/1K output tokens |
| **Speed** | Very fast (faster than GPT-4) |
| **Quality** | Very good |
| **Context** | 128k tokens |
| **Math** | Very good |
| **Cost** | 50% cheaper than GPT-4 Turbo |

**Setup:**
```bash
MODEL_NAME=gpt-4o
```

---

### 3. OpenAI GPT-3.5 Turbo 💰 (Budget Option)

**Best For:** Budget-conscious students

| Aspect | Details |
|--------|---------|
| **Price** | $0.0005/1K input, $0.0015/1K output tokens |
| **Speed** | Fastest |
| **Quality** | Good (not excellent) |
| **Context** | 16k tokens |
| **Math** | Good for basic/intermediate |
| **Cost** | CHEAPEST |

**Pros:**
- ✅ Very cheap ($1-5/month for student use)
- ✅ Fastest response
- ✅ Good for basic math
- ✅ Works well with tutoring

**Cons:**
- ❌ Less capable for advanced topics
- ❌ May struggle with complex proofs
- ❌ Shorter context window

**Setup:**
```bash
MODEL_NAME=gpt-3.5-turbo
```

---

### 4. Claude 3 Models (Alternative to OpenAI)

#### Claude 3 Opus (Powerful)
- **Price:** $0.015/1K input, $0.075/1K output tokens
- **Quality:** Excellent (competes with GPT-4)
- **Speed:** Fast
- **Math:** Very good
- **Best For:** Best alternative to GPT-4

#### Claude 3 Sonnet (Balanced)
- **Price:** $0.003/1K input, $0.015/1K output tokens
- **Quality:** Good
- **Speed:** Very fast
- **Math:** Good for most topics
- **Best For:** Budget + quality balance

#### Claude 3 Haiku (Fast & Cheap)
- **Price:** $0.00025/1K input, $0.00125/1K output tokens
- **Quality:** Basic but decent
- **Speed:** Fastest
- **Math:** Good for simple problems
- **Best For:** Lowest cost, less capable

**Setup:**
```bash
AI_MODEL=claude
CLAUDE_API_KEY=sk-ant-...
MODEL_NAME=claude-3-opus-20240229
```

---

### 5. Google Gemini (Alternative)

#### Gemini 1.5 Pro
- **Price:** Free tier available, paid: $0.0025/1K input, $0.01/1K output
- **Quality:** Good
- **Speed:** Fast
- **Math:** Good
- **Best For:** Students wanting free tier

#### Gemini 2.0 Flash
- **Price:** Similar to Pro
- **Quality:** Very good
- **Speed:** Very fast
- **Math:** Very good
- **Best For:** Speed + quality

**Setup:**
```bash
AI_MODEL=google
GOOGLE_API_KEY=...
MODEL_NAME=gemini-pro
```

---

### 6. Local Models (Free & Private)

#### Llama 2 (via Ollama) - Recommended Free Option

**Best For:** Free, private, no API keys

| Aspect | Details |
|--------|---------|
| **Price** | FREE |
| **Speed** | Slow (depends on your computer) |
| **Quality** | Decent (B grade) |
| **Privacy** | Complete (runs on your machine) |
| **Math** | Okay (struggles with advanced) |
| **Setup** | Moderate |

**Requirements:**
- 8GB+ RAM (16GB recommended)
- Download: 4GB model file
- GPU helps (but not required)

**Setup:**
```bash
# 1. Download and install Ollama
# https://ollama.ai

# 2. Pull Llama 2
ollama pull llama2

# 3. Configure
AI_MODEL=ollama
MODEL_NAME=llama2

# 4. Start Ollama in another terminal
ollama serve
```

**Performance:**
- Response time: 5-30 seconds per answer
- Quality: Good for explanations, okay for complex problems

---

#### Mistral 7B (Alternative Local)

```bash
ollama pull mistral
# Better performance than Llama 2 but still local
```

---

## Cost Comparison (Monthly for Student Use)

### Scenario: 10 questions/day, ~500 tokens per answer

| Model | Daily | Monthly | Annual |
|-------|-------|---------|--------|
| GPT-4 Turbo | $0.15 | $4.50 | $54 |
| GPT-4o | $0.08 | $2.40 | $29 |
| Claude 3 Sonnet | $0.05 | $1.50 | $18 |
| GPT-3.5 Turbo | $0.01 | $0.30 | $3 |
| Claude 3 Haiku | $0.01 | $0.30 | $3 |
| Llama 2 (Local) | $0 | $0 | $0 |

---

## Recommendation by Situation

### I'm a Student with Limited Budget
**Option 1 (EASIEST):** GPT-3.5 Turbo (~$3/month)
```bash
MODEL_NAME=gpt-3.5-turbo
# Simple, cheap, works well
```

**Option 2 (FREE):** Llama 2 local
```bash
AI_MODEL=ollama
# Free but slower (5-30 sec per answer)
```

### I'm a Student Who Wants Quality
**Best Choice:** Claude 3 Sonnet (~$1-2/month)
```bash
AI_MODEL=claude
MODEL_NAME=claude-3-sonnet-20240229
# Great quality, fast, affordable
```

### I'm a Teacher/Tutor Deploying Widely
**Best Choice:** GPT-3.5 Turbo for scale
```bash
# Cheapest while maintaining acceptable quality
# Monitor costs, might be <$1 per student per month
```

### I Need the Absolute Best Quality
**Choice:** GPT-4 Turbo or Claude 3 Opus
```bash
# $4-5/month per user but best explanations
# Worth it if students can share costs
```

### I Need Privacy/Offline Use
**Choice:** Llama 2 (Ollama)
```bash
# Runs locally, no data sent anywhere
# Free but requires good computer
```

---

## Setup Instructions for Different Models

### Setup 1: GPT-3.5 Turbo (Recommended Beginner)

```bash
# 1. Get API key: https://platform.openai.com/api-keys

# 2. Create .env
OPENAI_API_KEY=sk-...
AI_MODEL=openai
MODEL_NAME=gpt-3.5-turbo

# 3. Run, should work immediately
python backend/app.py
```

### Setup 2: Claude (Recommended Quality)

```bash
# 1. Get API key: https://console.anthropic.com/

# 2. Create .env
CLAUDE_API_KEY=sk-ant-...
AI_MODEL=claude
MODEL_NAME=claude-3-sonnet-20240229

# 3. Install additional dependency
pip install anthropic>=0.7.0

# 4. Update agent/math_agent.py to use Claude
# (Will provide updated file)
```

### Setup 3: Llama 2 Local (Free)

```bash
# 1. Download Ollama: https://ollama.ai

# 2. Pull model (takes 5-10 minutes, needs 4GB space)
ollama pull llama2

# 3. Create .env
AI_MODEL=ollama
MODEL_NAME=llama2

# 4. In Terminal 1: Start Ollama
ollama serve

# 5. In Terminal 2: Run app
python backend/app.py

# Note: First response takes 30 seconds, then faster
```

---

## Switching Between Models

To switch models after initial setup:

1. **Edit `.env` file**
2. **Update `MODEL_NAME`**
3. **Restart backend**

That's it! The system is designed to work with multiple models.

---

## Monitoring & Optimizing Costs

### Track API Usage

```python
# Add to app.py
import json
from datetime import datetime

def log_api_call(model, tokens_used, cost):
    with open('usage_log.json', 'a') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'tokens': tokens_used,
            'cost': cost
        }, f)
        f.write('\n')
```

### Cost-Saving Tips

1. **Cache responses:** Don't re-ask same questions
2. **Batch queries:** Group multiple questions
3. **Use cheaper model for simple tasks**
4. **Monitor usage:** Check API dashboards regularly
5. **Set spending limits:** In API dashboard

---

## Quality Comparison for Math Topics

| Topic | GPT-4 | Claude | GPT-3.5 | Llama 2 |
|-------|-------|--------|---------|---------|
| Basic Algebra | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Calculus | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Linear Algebra | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Proofs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Explanations | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Step-by-Step | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## My Final Recommendation

**For most students:** Start with **GPT-3.5 Turbo**
- Cheap ($3/month)
- Good quality
- Fast
- Easy setup

**Then upgrade to:** **Claude 3 Sonnet** if you need better quality
- Still cheap ($18/month)
- Excellent quality
- Very good reasoning

**If money is no object:** **GPT-4 Turbo or Claude 3 Opus**
- Best quality
- Worth it for serious study

---

## Still Unsure?

Run a test:

```bash
# Setup GPT-3.5 (cheapest)
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-3.5-turbo

# Try 10 questions
# If quality is good enough → stick with it
# If you want better → upgrade to GPT-4 or Claude

# The difference in quality might not be worth 10x the cost!
```

---

**Questions? Check the main README.md or SETUP.md!**
