# 📐 Math Study AI - Interactive AI Tutor for Mathematics

A comprehensive Python application that uses AI to help students learn mathematics. The system features an intelligent AI agent that explains concepts, solves problems, and recommends learning resources. Built with Flask backend, modern web UI, and LangChain for AI agent management.

## 🎯 Features

✅ **AI Math Tutoring** - Ask questions and get instant explanations  
✅ **Problem Solving** - Get step-by-step solutions with detailed explanations  
✅ **Concept Explanations** - Break down complex mathematical concepts  
✅ **Resource Finder** - Search and access curated math learning websites  
✅ **Conversational Learning** - Natural back-and-forth dialogue with the AI tutor  
✅ **Multi-Topic Support** - Covers Algebra, Calculus, Geometry, Linear Algebra, and more  
✅ **Clean Web Interface** - Modern, responsive UI for easy interaction  

## 🏗️ Project Structure

```
MathStudyAI/
├── config/
│   └── settings.py              # Configuration settings
├── backend/
│   ├── app.py                   # Flask API server
│   └── data_handler.py          # XLSX file handler
├── agent/
│   └── math_agent.py            # AI agent implementation with LangChain
├── frontend/
│   ├── index.html               # Web interface
│   ├── styles.css               # Styling
│   └── script.js                # Frontend JavaScript
├── data/
│   └── math_websites.xlsx       # Resource database
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🤖 AI Model Recommendations & Setup

### Recommended Models (Ranked by Performance)

#### 1. **GPT-4 Turbo (Recommended - Best Quality)**
- **Provider**: OpenAI
- **Model**: `gpt-4-turbo-preview`
- **Cost**: $0.01/1K input tokens, $0.03/1K output tokens
- **Pros**: Most capable, best for complex math, best reasoning
- **Cons**: Higher cost, requires API key

```bash
# Setup
export OPENAI_API_KEY="your-api-key-here"
# In .env
AI_MODEL=openai
MODEL_NAME=gpt-4-turbo-preview
```

#### 2. **GPT-4o (Good Alternative)**
- **Model**: `gpt-4o`
- **Cost**: Lower than GPT-4 Turbo
- **Pros**: Good reasoning, faster responses
- **Cons**: Still requires API key

#### 3. **Claude 3 Opus (Excellent Alternative)**
- **Provider**: Anthropic
- **Model**: `claude-3-opus-20240229`
- **Cost**: Similar to GPT-4
- **Pros**: Excellent reasoning, good explanations
- **Cons**: Requires Anthropic API key

```bash
# Setup
export CLAUDE_API_KEY="your-api-key-here"
# In .env
AI_MODEL=claude
```

#### 4. **Llama 2 (Free Local Alternative)**
- **Provider**: Meta (via Ollama or HuggingFace)
- **Model**: `llama2`
- **Cost**: Free (runs locally)
- **Pros**: Free, no API keys needed, privacy-focused
- **Cons**: Slower, requires more compute, less capable than GPT-4

```bash
# Setup with Ollama
ollama pull llama2
# In config/settings.py
AI_MODEL=ollama
MODEL_NAME=llama2
```

#### 5. **Google Gemini (Good Option)**
- **Provider**: Google
- **Model**: `gemini-pro`
- **Cost**: Free tier available
- **Pros**: Good performance, free tier
- **Cons**: Limited by Google's policies

### Quick Comparison Table

| Model | Cost | Quality | Speed | Setup |
|-------|------|---------|-------|-------|
| GPT-4 Turbo | $$$ | ⭐⭐⭐⭐⭐ | Fast | Easy |
| Claude 3 Opus | $$$ | ⭐⭐⭐⭐⭐ | Fast | Easy |
| GPT-3.5 Turbo | $ | ⭐⭐⭐⭐ | Very Fast | Easy |
| Llama 2 | Free | ⭐⭐⭐ | Slow | Moderate |
| Gemini Pro | $-Free | ⭐⭐⭐⭐ | Fast | Easy |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- OpenAI API key (or alternative model API key)
- Modern web browser

### Step 1: Clone/Download the Project
```bash
cd c:\Users\soura\OneDrive\Documents\APRStudy\MathStudyAI
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the template
cp .env.example .env

# Edit .env with your settings
# For OpenAI:
# OPENAI_API_KEY=sk-...your-key...
# AI_MODEL=openai
# MODEL_NAME=gpt-4-turbo-preview
```

### Step 5: Prepare Data
The application will automatically create a sample `math_websites.xlsx` file on first run. You can customize it:

```python
# In backend/data_handler.py
python -c "
from backend.data_handler import create_sample_excel
df = create_sample_excel()
df.to_excel('data/math_websites.xlsx', sheet_name='Websites', index=False)
"
```

### Step 6: Run the Application

**Terminal 1 - Start Backend Server:**
```bash
cd backend
python app.py
# Server runs on http://localhost:5000
```

**Terminal 2 - Open Frontend:**
```bash
# Simple way: Open frontend/index.html in browser
# Or use Python's built-in server:
cd frontend
python -m http.server 8000
# Open http://localhost:8000 in browser
```

## 💻 Usage

### Chat Mode
- Ask any math question
- Get instant AI-powered responses
- Maintains conversation context

### Explain Mode
- Enter a math concept (e.g., "Derivatives", "Quadratic Equations")
- Get comprehensive explanation with examples

### Solve Mode
- Paste your math problem
- Get step-by-step solution with reasoning

### Resources Mode
- Search for learning resources
- Find websites and tools for specific topics
- Links to Khan Academy, MIT OCW, Brilliant.org, etc.

## 🔧 Agent Configuration & System Prompt

### How the Agent Works

The AI agent is built with **LangChain** and uses the following architecture:

```
User Query
    ↓
Agent receives query
    ↓
Selects appropriate tool (Explain, Solve, FindResources, etc.)
    ↓
Executes tool with LLM context
    ↓
Returns formatted response
    ↓
Maintains conversation memory
```

### System Prompt (Multi-Tool Orchestration)

The agent uses this core system prompt:

```
You are an expert mathematics tutor AI assistant designed to help students learn and understand mathematical concepts. Your role is to:

1. **Explain Concepts**: Break down complex mathematical topics into simple, understandable steps
2. **Solve Problems**: Walk through problem-solving step-by-step, explaining the reasoning
3. **Provide Resources**: Suggest relevant learning resources from the provided list
4. **Encourage Learning**: Be supportive and encouraging, adapting to the student's level
5. **Check Understanding**: Ask clarifying questions to ensure the student understands

Your teaching approach:
- Start with the fundamentals if the student seems confused
- Use real-world examples when possible
- Show multiple ways to solve problems
- Identify common mistakes and help students avoid them
- Encourage students to try solving problems themselves
- Adapt your explanation complexity based on their responses
```

### Agent Type: REACT (Reasoning + Action)

The agent uses the **REACT** pattern:
- **Reasoning**: Thinks through the problem
- **Action**: Chooses a tool/approach
- **Observation**: Sees the result
- **Thought**: Iterates as needed

### Customizing the Agent

Edit `agent/math_agent.py` to customize:

```python
# Change system prompt
SYSTEM_PROMPT = """Your custom prompt here"""

# Modify tools
def _create_tools(self) -> List[Tool]:
    # Add your custom tools here
    
# Adjust agent parameters
self.agent = initialize_agent(
    tools=self.tools,
    llm=self.llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=self.memory,
    max_iterations=5,  # Increase if agent needs more thinking time
    handle_parsing_errors=True
)
```

## 📊 API Endpoints

### Core Endpoints

**GET** `/` - Health check
```bash
curl http://localhost:5000/
```

**POST** `/api/chat` - Send message to tutor
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I solve 2x + 5 = 13?"}'
```

**POST** `/api/explain` - Explain a concept
```bash
curl -X POST http://localhost:5000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"concept": "Quadratic Equations"}'
```

**POST** `/api/solve` - Solve a problem
```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"problem": "Solve: 3x² + 2x - 5 = 0"}'
```

**GET** `/api/resources` - Get all resources
```bash
curl http://localhost:5000/api/resources
```

**POST** `/api/resources/search` - Search resources
```bash
curl -X POST http://localhost:5000/api/resources/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculus"}'
```

**POST** `/api/chat/reset` - Reset conversation
```bash
curl -X POST http://localhost:5000/api/chat/reset
```

## 📚 Resource File Format

The `math_websites.xlsx` should have these columns:

| Column | Type | Example |
|--------|------|---------|
| Title | String | Khan Academy - Calculus |
| Topic | String | Calculus |
| URL | String | https://www.khanacademy.org/math/... |
| Description | String | Comprehensive calculus lessons |
| Difficulty | String | Intermediate |
| Type | String | Video Lessons |

## 🐛 Troubleshooting

### Backend Not Starting
```
Error: API key not configured
→ Check OPENAI_API_KEY in .env file

Error: Port 5000 already in use
→ Change PORT in .env or kill process: lsof -ti:5000 | xargs kill -9
```

### Frontend Can't Connect
```
Error: Failed to connect to server
→ Make sure backend is running on http://localhost:5000
→ Check CORS is enabled
→ Check firewall settings
```

### AI Not Generating Good Responses
```
→ Try increasing MAX_TOKENS in config/settings.py
→ Adjust TEMPERATURE (0=deterministic, 1=creative)
→ Use a more capable model (GPT-4 > GPT-3.5)
```

## 🎓 Advanced Features

### Custom Teaching Styles

Modify the system prompt for different styles:

```python
# Socratic Method
SYSTEM_PROMPT = """Guide students by asking questions rather than giving answers..."""

# Formal Academic
SYSTEM_PROMPT = """Use rigorous mathematical terminology and formal proofs..."""

# Casual Friendly
SYSTEM_PROMPT = """Use simple language and relatable examples..."""
```

### Multi-Language Support

Extend the prompt to support multiple languages:

```python
prompt = f"""
System: {self.SYSTEM_PROMPT}
Language: {user_language}
"""
```

### Performance Monitoring

Add tracking for common issues:

```python
def log_query(query, response_time, model_cost):
    # Log to database or file
    pass
```

## 📈 Improving Quality

### 1. Fine-tune Prompts
- Test different prompt variations
- Collect feedback on responses
- Iteratively improve

### 2. Add Context
- Pre-upload textbooks/notes
- Include problem databases
- Reference official standards

### 3. Use Prompt Engineering
- Chain-of-thought: "Let's break this down..."
- Few-shot examples: "Here's how you would solve..."
- Structured output: "Provide: (1) Concept (2) Steps (3) Examples"

### 4. Implement Caching
```python
from langchain.cache import SQLiteCache
import langchain

langchain.llm_cache = SQLiteCache(database_path="cache.db")
```

## 📝 License

MIT License - Feel free to use and modify for your needs

## 🤝 Contributing

Suggestions and improvements are welcome! Areas to enhance:

1. **More Resources** - Add more learning website links
2. **Better Explanations** - Improve system prompts
3. **Advanced Features** - Add visualization, video generation
4. **Mobile App** - React Native version
5. **Offline Support** - Local LLM integration

## 📞 Support

Issues with setup? Check:
1. Python version (3.8+)
2. API keys configuration
3. Internet connectivity
4. Port availability
5. Dependencies installed correctly

## 🚀 Next Steps

1. ✅ Get an API key from OpenAI/Claude/Google
2. ✅ Configure .env file
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Start backend: `python backend/app.py`
5. ✅ Open frontend: `frontend/index.html`
6. ✅ Start learning!

---

**Happy Learning! 📚✨**

For issues or questions, refer to the troubleshooting section or check the API documentation.
