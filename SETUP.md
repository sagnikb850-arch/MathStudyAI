# 🚀 Quick Start Guide - Math Study AI

## 5-Minute Setup

### Option 1: Using OpenAI GPT-4 (Recommended)

#### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (save it securely)
5. Cost: ~$0.01 per 1000 input tokens

#### Step 2: Setup Project
```bash
cd c:\Users\soura\OneDrive\Documents\APRStudy\MathStudyAI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 3: Configure API Key
Create `.env` file in the project root:
```
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=5000

AI_MODEL=openai
OPENAI_API_KEY=sk-...your-key-here...
MODEL_NAME=gpt-4-turbo-preview
```

#### Step 4: Get Resources File
The `math_websites.xlsx` will be created automatically. To customize:

```python
# Run this command to see/edit resources
python -c "
import pandas as pd
from backend.data_handler import create_sample_excel
df = create_sample_excel()
print(df)
df.to_excel('data/math_websites.xlsx', sheet_name='Websites', index=False)
"
```

#### Step 5: Start Server
```bash
cd backend
python app.py
# Output: Starting Math Study AI Server on 0.0.0.0:5000
```

#### Step 6: Open UI
Open `frontend/index.html` in your web browser
- Click "Chat" tab
- Type your question: "Explain quadratic equations"
- Click Send and wait for the response!

---

## Option 2: Using Claude (Anthropic) - Alternative

### Setup
1. Get API key: https://console.anthropic.com/
2. Create `.env`:
```
CLAUDE_API_KEY=sk-ant-...your-key...
AI_MODEL=claude
MODEL_NAME=claude-3-opus-20240229
```
3. Run backend as above

---

## Option 3: Free Local Model (Llama 2)

### Prerequisites
1. Download Ollama: https://ollama.ai
2. Install it

### Setup
```bash
# Pull Llama2 model (first time takes a few minutes)
ollama pull llama2

# Create .env
FLASK_ENV=development
AI_MODEL=ollama
MODEL_NAME=llama2
```

### Start servers
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start backend
cd backend
python app.py
```

---

## Common Issues & Solutions

### "ModuleNotFoundError: No module named 'openai'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
```bash
# Solution: Create .env file with your API key
# See Step 3 above
```

### "Port 5000 already in use"
```bash
# Solution 1: Change port in .env
PORT=5001

# Solution 2: Kill the process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Frontend can't connect to backend
```bash
# Solution 1: Check backend is running
# Open browser to http://localhost:5000/api/health

# Solution 2: Check CORS
# Backend has CORS enabled, frontend should work

# Solution 3: Check firewall
# Windows: Allow Python through firewall
```

### AI giving weird responses
```bash
# Solutions:
# 1. Check API key is correct
# 2. Try different model: gpt-4 instead of gpt-3.5
# 3. Increase MAX_TOKENS in config/settings.py (e.g., 3000)
# 4. Lower TEMPERATURE for more consistent answers
```

---

## Understanding the Project Structure

```
MathStudyAI/
│
├── backend/
│   ├── app.py              ← Flask server (run this first!)
│   └── data_handler.py     ← Reads Excel file
│
├── agent/
│   └── math_agent.py       ← AI logic (LangChain)
│
├── frontend/
│   ├── index.html          ← Open this in browser
│   ├── styles.css
│   └── script.js
│
├── config/
│   └── settings.py         ← Configuration
│
└── data/
    └── math_websites.xlsx  ← Resources database (auto-created)
```

---

## How It Works

1. **You ask a question** in the web interface
2. **Frontend sends it** to Backend API
3. **Backend asks AI Agent** using LangChain
4. **AI processes** with system prompt
5. **AI uses tools** (Explain, Solve, FindResources)
6. **Backend returns** the AI response
7. **Frontend displays** the answer

---

## Customizing the AI

### Change System Prompt
Edit `agent/math_agent.py`:
```python
SYSTEM_PROMPT = """
You are a math tutor who...
[Your custom prompt]
"""
```

### Add More Resources
Edit `data/math_websites.xlsx` and add rows:
- Title: Name of resource
- Topic: What it teaches
- URL: Link to resource
- Description: Details
- Difficulty: Beginner/Intermediate/Advanced
- Type: Video/Interactive/Text/etc

### Use Different AI Model
In `.env`:
```
# For GPT-4
AI_MODEL=openai
MODEL_NAME=gpt-4-turbo-preview

# For Claude
AI_MODEL=claude
MODEL_NAME=claude-3-opus-20240229

# For Local Llama
AI_MODEL=ollama
MODEL_NAME=llama2
```

---

## Testing the API

Use curl or Postman to test:

```bash
# Test health
curl http://localhost:5000/

# Send a chat message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is a derivative?\"}"

# Search resources
curl -X POST http://localhost:5000/api/resources/search \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Calculus\"}"
```

---

## Tips for Best Results

### Good Questions
✅ "Explain quadratic equations"
✅ "How do I solve 3x + 5 = 14?"
✅ "What's the difference between permutation and combination?"
✅ "Show me step-by-step how to integrate x²"

### Bad Questions
❌ "Math"
❌ "Help"
❌ "?" (too vague)
❌ Just a long formula (add context)

### For Best AI Responses
- Be specific: "Explain derivatives for a beginner" not just "derivatives"
- Give context: "I'm learning calculus" vs just asking random questions
- Ask follow-ups: "I don't understand step 2, can you explain more?"

---

## Next Steps

1. ✅ Follow setup above
2. ✅ Ask 5-10 questions to test
3. ✅ Customize system prompt for your style
4. ✅ Add more resources to Excel
5. ✅ Deploy to make it web-accessible

---

## Costs Per Model (Monthly Estimate for Student Use)

- **GPT-4 Turbo**: $5-15/month (heavy use)
- **Claude 3 Opus**: $5-15/month  
- **GPT-3.5 Turbo**: $1-5/month (budget)
- **Llama 2 Local**: $0 (free, slower)

---

## Video Tutorial (Coming Soon)

[Short setup video will be added]

---

**Still stuck? Check the main README.md for more details!**
