# 🐛 Troubleshooting & FAQ

Quick solutions to common problems.

---

## 🚀 Setup Issues

### Q: "ModuleNotFoundError: No module named 'flask'"
**A:** Dependencies not installed
```bash
pip install -r requirements.txt
```

### Q: "OPENAI_API_KEY not set"
**A:** Missing API key configuration
```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Edit .env and add your key
OPENAI_API_KEY=sk-...

# 3. Restart the app
```

### Q: "FileNotFoundError: [Errno 2] No such file or directory: '.env'"
**A:** Don't use .env file (optional)
- The app will work if you set environment variables differently
- Or create the .env file from .env.example

### Q: "Port 5000 already in use"
**A:** Change port in .env
```ini
PORT=5001
```

Or kill the process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Q: "Command not found: python"
**A:** Python not installed or wrong command
```bash
# Try python3 on Mac/Linux
python3 --version

# Install from python.org
```

---

## 🔗 API Connection Issues

### Q: "Failed to connect to server"
**A:** Backend not running

```bash
# Check if it's running
curl http://localhost:5000/api/health

# If not, start it
cd backend
python app.py
```

### Q: "CORS error in browser console"
**A:** Likely a configuration issue

```python
# In backend/app.py, CORS is already enabled
# If still having issues, try:
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Q: "API returns 500 error"
**A:** Check backend logs

```bash
# Look for error message in terminal where you ran
# python backend/app.py
# Common causes:
# - Missing API key
# - Invalid request format
# - Rate limit exceeded
```

---

## 🤖 AI Agent Issues

### Q: "API key error from OpenAI"
**A:** Invalid or missing key

```bash
# Verify key
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows

# Get new key if needed
# https://platform.openai.com/api-keys
```

### Q: "Model not found: gpt-4"
**A:** Check model name

```bash
# Common valid models:
# gpt-4-turbo-preview
# gpt-4
# gpt-3.5-turbo
# claude-3-opus-20240229
# llama2

# In .env:
MODEL_NAME=gpt-4-turbo-preview
```

### Q: "Timeout waiting for response"
**A:** Request taking too long

```python
# In config/settings.py, increase timeout
MAX_TOKENS = 3000  # Higher = longer responses = slower

# Or use faster model:
MODEL_NAME=gpt-3.5-turbo  # Faster than GPT-4
```

### Q: "AI giving gibberish responses"
**A:** Multiple possible causes

```bash
# 1. Wrong model selected
# Check MODEL_NAME in .env

# 2. Prompt issues
# Edit SYSTEM_PROMPT in agent/math_agent.py

# 3. Temperature too high
# In config/settings.py:
TEMPERATURE = 0.7  # Try 0.5 for more consistent

# 4. Model quota exceeded
# Check API usage dashboard
```

### Q: "Response is too short/long"
**A:** Adjust token limit

```python
# In config/settings.py:
MAX_TOKENS = 2048  # Increase for longer responses
                   # Decrease for shorter
```

---

## 🎨 Frontend Issues

### Q: "Chat not updating, messages not showing"
**A:** JavaScript error

```bash
# Check browser console (F12)
# Look for red error messages
# Common causes:
# - Backend not running
# - Wrong port number
# - Fetch API blocked by CORS
```

### Q: "Buttons not working"
**A:** JavaScript issue

```bash
# Check browser console for errors
# Refresh page (Ctrl+R or Cmd+R)
# Clear browser cache
```

### Q: "Page looks broken/ugly"
**A:** CSS not loaded

```bash
# Make sure styles.css is in frontend/ folder
# Hard refresh browser (Ctrl+Shift+R)
# Check browser console for CSS load errors
```

### Q: "Mobile version not working"
**A:** Responsive design issue

```bash
# Should work on all devices
# If not:
# 1. Hard refresh browser
# 2. Check browser zoom is 100%
# 3. Try different browser
```

---

## 💾 Data / File Issues

### Q: "XLSX file not found"
**A:** Missing or wrong path

```python
# In config/settings.py, check:
WEBSITES_FILE = os.path.join(DATA_DIR, 'math_websites.xlsx')

# File should be in: data/math_websites.xlsx
# If missing, app will create it on first run
```

### Q: "Resources not loading"
**A:** XLSX file format issue

```bash
# Columns must be exactly:
# Title, Topic, URL, Description, Difficulty, Type

# Check column names (case sensitive)
# Verify file is valid XLSX
```

### Q: "Can't modify resources XLSX"
**A:** File locked by app

```bash
# Stop the app (Ctrl+C)
# Edit the XLSX file
# Restart the app
```

---

## 📦 Dependency Issues

### Q: "pip install fails"
**A:** Compatibility issue

```bash
# Try updating pip first
pip install --upgrade pip

# Install specific versions
pip install -r requirements.txt --upgrade

# If still failing, try:
pip install --no-cache-dir -r requirements.txt
```

### Q: "LangChain version mismatch"
**A:** Incompatible versions

```bash
# Reinstall with compatible versions
pip install langchain==0.1.0 langchain-openai==0.0.5

# Or check versions
pip show langchain
```

### Q: "numpy or pandas error"
**A:** Common with data libraries

```bash
# Reinstall
pip install --upgrade numpy pandas

# Or specific version
pip install numpy==1.24.0 pandas==2.0.0
```

---

## ⚡ Performance Issues

### Q: "App is very slow"
**A:** Multiple possible causes

```bash
# 1. Using free tier / rate limited?
# Check API dashboard

# 2. Using slow model?
# Try GPT-3.5-Turbo instead of GPT-4

# 3. Using local Llama?
# Expected: 5-30 seconds per response

# 4. Computer specs?
# Add more RAM or use faster CPU
```

### Q: "Memory leak / app crashes"
**A:** Memory issue with conversations

```python
# In agent/math_agent.py:
# Clear memory periodically
math_agent.reset_conversation()

# Or limit conversation history:
# self.memory = ConversationBufferMemory(
#     max_token_limit=4000
# )
```

### Q: "High API costs"
**A:** Unexpected charges

```bash
# 1. Monitor API usage
# https://platform.openai.com/account/usage/overview

# 2. Set spending limits
# https://platform.openai.com/account/billing/overview

# 3. Use cheaper model
# GPT-3.5 instead of GPT-4

# 4. Cache responses
# Don't re-process same questions
```

---

## 🔑 API Key Issues

### Q: "Invalid API key format"
**A:** Wrong format

```bash
# OpenAI format: sk-...
# Claude format: sk-ant-...
# Google format: AIzaSy...

# Verify format matches provider
```

### Q: "API key not working"
**A:** Multiple causes

```bash
# 1. Check it's not expired
# 2. Verify it has right permissions
# 3. Try creating new key
# 4. Check environment variable is set
echo $OPENAI_API_KEY
```

### Q: "Rate limited by API"
**A:** Too many requests

```bash
# Wait a bit before making more requests
# Use GPT-3.5 (more generous rate limits)
# Upgrade your API account tier
```

---

## 🖥️ Windows Specific

### Q: "Run launcher (run.bat) doesn't work"
**A:** Script execution disabled

```bash
# Open PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run directly:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```

### Q: "Virtual env activation fails"
**A:** Path issue

```powershell
# Try PowerShell version:
.\venv\Scripts\Activate.ps1

# Or CMD:
venv\Scripts\activate.bat
```

---

## 🍎 Mac/Linux Specific

### Q: "run.sh permission denied"
**A:** Need to make executable

```bash
chmod +x run.sh
./run.sh
```

### Q: "Python command not working"
**A:** Python 3 vs Python

```bash
# Use python3 instead
python3 --version
python3 -m venv venv
python3 backend/app.py
```

---

## 🔍 Debugging Tips

### Enable Debug Logging
```python
# In backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check What's Running
```bash
# Find running processes
lsof -i :5000  # Shows what's on port 5000

# Kill specific process
kill -9 <PID>
```

### Test API Directly
```bash
# Test with curl
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "2+2"}'
```

### Browser Developer Tools
```
F12 → Console tab
Shows JavaScript errors

F12 → Network tab
Shows API calls and responses
```

---

## 🆘 Still Stuck?

### Step-by-Step Debugging

1. **Check it's running**
   ```bash
   # Backend
   curl http://localhost:5000/api/health
   
   # Should return: {"status": "healthy"}
   ```

2. **Check API key**
   ```bash
   echo $OPENAI_API_KEY
   # Should show: sk-...something...
   ```

3. **Check simple request**
   ```bash
   curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "hello"}'
   ```

4. **Check logs**
   ```bash
   # Look at terminal where you ran app.py
   # Find error messages
   ```

5. **Try simpler model**
   ```bash
   # If using Llama locally:
   ollama pull mistral  # Faster than llama2
   # Then update .env
   ```

---

## 📚 Resources

- **Python:** https://python.org/
- **Flask:** https://flask.palletsprojects.com/
- **LangChain:** https://python.langchain.com/
- **OpenAI:** https://openai.com/
- **Claude:** https://claude.ai/
- **Stack Overflow:** Search your error message

---

## 🎯 Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Package not installed | `pip install -r requirements.txt` |
| `ConnectionError` | Backend not running | `python backend/app.py` |
| `Invalid API key` | Wrong key or expired | Check and regenerate in API dashboard |
| `Port already in use` | Another app on port 5000 | Change PORT in .env or kill process |
| `FileNotFoundError` | Missing .env file | Copy from .env.example |
| `TimeoutError` | Request too slow | Increase timeout or use faster model |
| `CORS error` | Browser blocking request | Likely backend not running |
| `500 Internal Server Error` | Backend error | Check terminal logs |

---

## 💡 Pro Tips

1. **Always check logs first** - Terminal shows errors
2. **Restart when changing config** - Changes need app restart
3. **Test with curl** - Isolate frontend vs backend issues
4. **Use cheaper model for testing** - GPT-3.5 for development
5. **Keep API key safe** - Never commit to git
6. **Monitor costs** - Check API dashboard regularly
7. **Cache responses** - Avoid duplicate API calls
8. **Read error messages carefully** - They usually tell you what's wrong

---

## ❓ FAQ

**Q: Is it free?**  
A: Free tier available. Most models are $0.30-5 per month for student use.

**Q: Can I use this offline?**  
A: Yes, with local Llama 2 model. It's slower but completely private.

**Q: How do I deploy this?**  
A: See ARCHITECTURE.md for deployment options.

**Q: Can I modify the teaching style?**  
A: Yes, edit SYSTEM_PROMPT in agent/math_agent.py

**Q: Which model should I use?**  
A: Start with GPT-3.5 Turbo (cheap, fast). See MODEL_SELECTION.md.

**Q: How do I add more learning resources?**  
A: Edit data/math_websites.xlsx and restart.

---

**Still need help? Read the other documentation files or search for your specific error message online!** 🚀

