# 🏗️ Architecture & System Design

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     WEB BROWSER                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         FRONTEND (HTML/CSS/JavaScript)                │ │
│  │  • Chat Interface                                      │ │
│  │  • Explain Mode                                        │ │
│  │  • Problem Solver                                      │ │
│  │  • Resources Search                                    │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP/REST API
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (Flask Server)                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            API Routes (app.py)                         │ │
│  │  • /api/chat - Chat endpoint                           │ │
│  │  • /api/explain - Explain concept                      │ │
│  │  • /api/solve - Solve problem                          │ │
│  │  • /api/resources - Get resources                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           AI Agent (LangChain)                         │ │
│  │  • MathTutorAgent                                      │ │
│  │  • System Prompt                                       │ │
│  │  • Memory (Conversation Context)                       │ │
│  │  • Tools (Explain, Solve, Resources)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│          ┌──────────────┼──────────────┐                    │
│          ↓              ↓              ↓                    │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│    │ Data     │  │ OpenAI/  │  │ Config   │              │
│    │ Handler  │  │ Claude/  │  │ Settings │              │
│    │ (Excel)  │  │ Llama    │  │          │              │
│    └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────────┘
         │                  │                 │
         ↓                  ↓                 ↓
    ┌──────────┐      ┌──────────┐     ┌──────────┐
    │ XLSX     │      │ AI Model │     │ .env     │
    │ File     │      │ API      │     │ File     │
    │ (Local)  │      │ (Cloud)  │     │ (Local)  │
    └──────────┘      └──────────┘     └──────────┘
```

---

## Component Details

### 1. Frontend Layer
**Files:** `frontend/index.html`, `styles.css`, `script.js`

**Responsibilities:**
- Display user interface
- Handle user input
- Make API calls to backend
- Display AI responses
- Manage conversation history

**Technologies:**
- HTML5 for structure
- CSS3 for responsive design
- Vanilla JavaScript (no framework)

**Key Features:**
- Chat interface with message history
- Multiple modes (chat, explain, solve, resources)
- Loading states
- Toast notifications
- Responsive design (mobile-friendly)

---

### 2. Backend API (Flask)
**Files:** `backend/app.py`

**Responsibilities:**
- Receive HTTP requests from frontend
- Route requests to appropriate handlers
- Initialize and manage AI agent
- Load resource data
- Return JSON responses

**Endpoints:**
```
POST   /api/chat - Main chat interaction
POST   /api/explain - Explain concept
POST   /api/solve - Solve problem
GET    /api/resources - List all resources
POST   /api/resources/search - Search resources
GET    /api/resources/<topic> - Get resources by topic
POST   /api/chat/reset - Reset conversation
GET    /api/health - Health check
```

**Technology:**
- Flask 3.0+ (lightweight web framework)
- Flask-CORS (cross-origin requests)
- JSON responses

---

### 3. AI Agent (LangChain)
**Files:** `agent/math_agent.py`

**Architecture:**
```
MathTutorAgent
├── System Prompt (Defines behavior)
├── LLM (OpenAI/Claude/Llama)
├── Tools
│   ├── ExplainConcept
│   ├── SolveProblem
│   ├── FindResources
│   └── CheckUnderstanding
├── Memory (Conversation history)
└── Agent Executor (REACT agent)
```

**How it Works:**
1. Receives user query
2. Analyzes query to understand intent
3. Selects appropriate tool(s)
4. Executes tool with LLM
5. Maintains conversation memory
6. Returns formatted response

**System Prompt:**
- Defines the tutor's personality
- Sets teaching approach
- Includes available topics
- Specifies output format

**Memory System:**
- Stores conversation history
- Enables context-aware responses
- Can be reset for new sessions

---

### 4. Data Handler
**Files:** `backend/data_handler.py`

**Responsibilities:**
- Read XLSX file
- Search resources by topic
- Format resources for AI context
- Return resource information

**Class:** `MathResourcesManager`

**Key Methods:**
```python
load_resources()              # Load from XLSX
get_all_resources()          # Get all resources
search_resources(query)       # Search by keyword
get_resources_for_topic()    # Get by topic
get_resources_as_context()   # Format for AI
```

**Data Structure:**
```
Columns: Title | Topic | URL | Description | Difficulty | Type
```

---

### 5. Configuration
**Files:** `config/settings.py`, `.env`

**Settings:**
- Flask configuration (host, port, debug)
- AI model selection
- API keys
- Model parameters
- Data file paths

**Configuration Options:**

```python
# Model Selection
AI_MODEL = 'openai'  # openai, claude, ollama, google
MODEL_NAME = 'gpt-4-turbo-preview'

# Model Parameters
MAX_TOKENS = 2048
TEMPERATURE = 0.7
TOP_P = 0.9

# Other Settings
FLASK_ENV = 'development'
DEBUG = True
PORT = 5000
```

---

## Data Flow: User Question → AI Response

### Step 1: Frontend → Backend
```javascript
// User types question and clicks Send
fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ message: "How do I solve x² = 16?" })
})
```

### Step 2: Backend Receives Request
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    # Process...
```

### Step 3: Backend Calls Agent
```python
# math_agent.process_query_simple(message)
response = math_agent.process_query_simple(message)
```

### Step 4: Agent With LLM
```
Query: System Prompt + Resources + User Message
       ↓
    LLM (GPT-4/Claude/Llama)
       ↓
    AI Reasoning (using Tools)
       ↓
    Response
```

### Step 5: Backend Returns Response
```python
return jsonify({
    "success": True,
    "message": "x = 4 or x = -4...",
    "model": "gpt-4-turbo-preview"
})
```

### Step 6: Frontend Displays Response
```javascript
// Display message in chat
addMessage(response.message, 'bot')
```

---

## Technology Stack

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Grid, Flexbox)
- **JavaScript (ES6+)** - Interactivity
- **Browser APIs** - Fetch API, LocalStorage

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0+** - Web framework
- **LangChain 0.1+** - AI orchestration
- **OpenAI SDK** - LLM access
- **Pandas** - Data handling
- **OpenPyXL** - XLSX reading

### AI/ML
- **LangChain** - Agent framework
- **OpenAI GPT-4/3.5** - Language model (primary)
- **Claude (Anthropic)** - Alternative LLM
- **Llama 2 (Ollama)** - Local alternative

### Infrastructure
- **Flask Development Server** - Local testing
- **HTTP/REST** - API communication
- **JSON** - Data format

---

## Deployment Architecture

### Local Development
```
Your Computer
├── Frontend (file:///)
├── Backend (localhost:5000)
└── Ollama (optional, localhost:11434)
```

### Production (Optional)
```
Cloud Server (AWS/Google Cloud/Heroku)
├── Frontend (Static files)
├── Flask App (Gunicorn + Nginx)
├── LB (Load Balancer)
├── API Keys (Environment variables)
└── Database (Optional, for logging)
```

---

## Security Considerations

### Current (Development)
- API keys in .env (never in .git)
- CORS enabled for localhost
- No authentication
- HTTP only (development)

### Production
- Store API keys in secure vault
- HTTPS only
- User authentication
- Rate limiting
- Input validation
- CORS restrictions
- Logging & monitoring

---

## Scalability Design

### Current
- Single Flask server
- In-memory conversation storage
- File-based resource data

### Scalable Options
1. **Database for history:** PostgreSQL/MongoDB
2. **Caching:** Redis for frequent queries
3. **Message queue:** Celery for async tasks
4. **CDN:** For static frontend files
5. **API Gateway:** Kong/AWS API Gateway
6. **Containerization:** Docker for easy deployment
7. **Monitoring:** ELK stack for logging

---

## Performance Optimization

### Frontend
- Lazy loading
- CSS minification
- JS minification
- Caching responses
- Debouncing inputs

### Backend
- Response caching
- Connection pooling
- Async processing
- Resource loading optimization
- LLM response caching

### Example: Response Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(query):
    # Cache common questions
    return math_agent.process_query(query)
```

---

## Error Handling

### Frontend
- Network error handling
- Timeout handling
- Empty response handling
- API error parsing

### Backend
- Try-catch around LLM calls
- Validation of inputs
- Graceful fallback responses
- Error logging

### Example:
```python
try:
    response = math_agent.process_query(query)
except Exception as e:
    return jsonify({
        "success": False,
        "error": "Failed to process query"
    }), 500
```

---

## Testing Strategy

### Frontend Tests
- Unit tests for API calls
- Integration tests for UI flows
- E2E tests for complete workflows

### Backend Tests
```python
# Test API endpoint
def test_chat_endpoint():
    response = client.post('/api/chat', 
        json={'message': 'Test'})
    assert response.status_code == 200
```

### Agent Tests
```python
# Test agent quality
def test_explanation_quality():
    response = agent.process_query("Explain derivatives")
    assert 'derivative' in response.lower()
    assert len(response) > 100
```

---

## Future Enhancements

### Short Term
- [ ] User authentication
- [ ] Save conversation history
- [ ] User preferences
- [ ] Multiple languages

### Medium Term
- [ ] Mobile app (React Native)
- [ ] Advanced visualizations
- [ ] LaTeX equation support
- [ ] Video generation
- [ ] Whiteboard mode

### Long Term
- [ ] Custom AI model fine-tuning
- [ ] Gamification
- [ ] Collaborative learning
- [ ] AI grading system
- [ ] Personalized learning paths

---

## Troubleshooting by Layer

### Frontend Issues
- Check browser console (F12)
- Verify backend URL
- Check CORS headers

### Backend Issues
- Check Flask logs
- Verify API key
- Check data file path

### Agent Issues
- Check system prompt
- Verify LLM response
- Check token limits

### Data Issues
- Verify XLSX format
- Check column names
- Validate file path

---

**For more details, see specific documentation files in the project.**
