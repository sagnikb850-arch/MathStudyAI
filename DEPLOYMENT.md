# 🚀 Deployment Guide - Host Your Math Study AI Online

Complete guide to deploy your Math Study AI application so students can access it from anywhere.

## 🎯 Quick Comparison: Hosting Options

| Platform | Cost | Setup Time | Performance | Best For |
|----------|------|-----------|-------------|----------|
| **Heroku** | Free-$7/mo | 10 min | Good | Quick deployment |
| **PythonAnywhere** | Free-$5/mo | 10 min | Good | Python apps |
| **Replit** | Free-$7/mo | 5 min | Good | Quick demos |
| **Railway** | Pay-as-you-go | 10 min | Good | Modern platform |
| **Render** | Free-$7/mo | 10 min | Good | Easy deployment |
| **AWS** | Free tier, then $$ | 30 min | Excellent | Scalable |
| **DigitalOcean** | $5/mo | 20 min | Excellent | Budget-friendly |
| **Google Cloud** | Free tier, then $$ | 30 min | Excellent | Professional |
| **Local + Ngrok** | Free | 5 min | Good | Testing only |

---

## ✅ Recommended: Render (Easiest & Free)

### Why Render?
✅ **Free tier available**  
✅ **Auto-deploys from GitHub**  
✅ **Includes SSL (HTTPS)**  
✅ **Simple setup (5 minutes)**  
✅ **No credit card for free tier**  

### Step-by-Step Deployment on Render

#### Step 1: Push Code to GitHub

```bash
# 1.1 Initialize git in your project
cd c:\Users\soura\OneDrive\Documents\APRStudy\MathStudyAI
git init
git add .
git commit -m "Initial commit - Math Study AI"

# 1.2 Create GitHub repository
# Go to https://github.com/new
# Name: MathStudyAI
# Make it Public
# Copy the commands to push your code
```

**Push to GitHub:**
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/MathStudyAI.git
git push -u origin main
```

#### Step 2: Create `.gitignore`

Add this to `.gitignore` (don't commit sensitive files):

```
.env
__pycache__/
*.pyc
venv/
.vscode/
.DS_Store
data/math_websites.xlsx
```

#### Step 3: Create `Procfile`

Create file: `Procfile` (no extension, in root folder)

```
web: python backend/app.py
```

#### Step 4: Create `runtime.txt`

Create file: `runtime.txt`

```
python-3.11.8
```

#### Step 5: Update `requirements.txt`

Make sure your requirements.txt is in project root with:

```
Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
openpyxl==3.1.5
pandas==2.0.0
requests==2.31.0
langchain==0.1.0
langchain-community==0.0.1
langchain-openai==0.0.5
openai==1.3.0
gunicorn==21.2.0
```

#### Step 6: Deploy on Render

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **Click:** "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure:**
   - **Name:** `math-study-ai`
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.app:app`
   - **Instance Type:** Free (or Starter $7/mo)

6. **Add Environment Variables:**
   - Click "Environment" → "Add Secret File"
   - Upload your `.env` file OR add variables manually:
     - `OPENAI_API_KEY` = your API key
     - `AI_MODEL` = openai
     - `MODEL_NAME` = gpt-3.5-turbo
     - `FLASK_ENV` = production

7. **Deploy!** Click "Create Web Service"

**That's it!** Your app will be live at: `https://math-study-ai.onrender.com`

---

## 🎯 Alternative: PythonAnywhere (Also Easy)

### Step-by-Step for PythonAnywhere

1. **Sign up:** https://www.pythonanywhere.com (free account)
2. **Upload code:** Via "Upload a zip file" or Git
3. **Create Web App:**
   - Click "Web" → "Add new web app"
   - Choose "Flask"
   - Choose Python version (3.11)
4. **Edit WSGI file:** Add your Flask app path
5. **Configure environment variables** in settings
6. **Reload web app**

**Live at:** `https://yourusername.pythonanywhere.com`

---

## 🌐 Option: DigitalOcean ($5/month - Best Value)

### Advantages:
- **$5/month droplet** (virtual server)
- **Full control over server**
- **Great performance**
- **Scalable if needed**
- **Includes email support**

### Deployment Steps:

1. **Create DigitalOcean Account:** https://digitalocean.com
2. **Create Droplet:**
   - OS: Ubuntu 22.04 LTS
   - Size: Basic ($5/month)
   - Region: Choose closest to you
3. **SSH into server:**
```bash
ssh root@YOUR_DROPLET_IP
```

4. **Install dependencies:**
```bash
apt update
apt install python3-pip python3-venv git nginx
```

5. **Clone your repo:**
```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/MathStudyAI.git
cd MathStudyAI
```

6. **Setup Python environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

7. **Create systemd service file:**

Create: `/etc/systemd/system/mathstudyai.service`

```ini
[Unit]
Description=Math Study AI Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/MathStudyAI
Environment="PATH=/var/www/MathStudyAI/venv/bin"
ExecStart=/var/www/MathStudyAI/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    backend.app:app

[Install]
WantedBy=multi-user.target
```

8. **Setup Nginx as reverse proxy:**

Create: `/etc/nginx/sites-available/mathstudyai`

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

9. **Enable site:**
```bash
ln -s /etc/nginx/sites-available/mathstudyai /etc/nginx/sites-enabled/
systemctl restart nginx
```

10. **Start service:**
```bash
systemctl start mathstudyai
systemctl enable mathstudyai
```

11. **Get SSL certificate (free):**
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

**App live at:** `https://your-domain.com`

---

## 🚀 Quick Option: Railway (Modern & Easy)

### Steps:

1. **Go to:** https://railway.app
2. **Connect GitHub**
3. **Click "Deploy from GitHub"**
4. **Select your repo**
5. **Add environment variables**
6. **Deploy!**

Cost: Pay-as-you-go (~$5-10/month for light usage)

---

## 🔐 Production Configuration Changes

### Update `backend/app.py` for Production:

```python
# At the top of app.py, add:
import os

# Change debug setting
DEBUG = os.getenv('FLASK_ENV') != 'production'

# For production:
if __name__ == '__main__':
    # Development
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    # Production (use Gunicorn instead)
```

### Update `config/settings.py`:

```python
# Add:
ALLOWED_HOSTS = ['*']  # For development only
# For production, use specific domains:
# ALLOWED_HOSTS = ['math-study-ai.onrender.com', 'yourdomain.com']
```

### Environment Variables to Set (Production):

```
FLASK_ENV=production
DEBUG=False
OPENAI_API_KEY=your_key_here
AI_MODEL=openai
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=2048
TEMPERATURE=0.7
```

---

## 📊 Comparing Hosting Costs

### Free Options (Forever Free):
- **Render:** 750 free hours/month (enough for low usage)
- **PythonAnywhere:** Limited free tier
- **Replit:** Free tier available
- **Railway:** Free credits initially

### Recommended Budget:
- **Per month:** $0-10
- **Year:** $0-120

### Cost Optimization Tips:
1. Use free tier as long as possible
2. Upgrade when traffic increases
3. Use auto-scaling (pay for what you use)
4. Monitor resource usage
5. Cache responses to reduce API calls

---

## 🔗 Student Access Methods

### Method 1: Direct Link
Share the URL with students:
```
https://math-study-ai.onrender.com
```

### Method 2: QR Code
Generate QR code pointing to your app:
- Use: https://qr-code-generator.com/
- Paste your URL
- Display in classroom

### Method 3: Class Portal
If you have a learning management system (LMS):
- Canvas
- Google Classroom
- Moodle
- Add as external link

### Method 4: Email List
Send access link via email/message:
```
Dear Students,

Your Math Study AI is now live!

📚 Visit: https://math-study-ai.onrender.com
👤 Username: your_course_code
🔑 Password: (if needed)

Happy learning!
```

---

## 📈 Managing Student Access

### Option A: Public Access (Anyone can use)
Pros:
- ✅ Simple setup
- ✅ No authentication needed
- ✅ Students can share with friends

Cons:
- ❌ Costly if heavily used
- ❌ No tracking of who uses it
- ❌ No usage limits

### Option B: Protected Access (With Login)

Add authentication to `backend/app.py`:

```python
from functools import wraps
import json

# Simple API key authentication
STUDENT_API_KEYS = {
    'student_2024_001': 'class_code_1',
    'student_2024_002': 'class_code_1',
}

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key not in STUDENT_API_KEYS:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/chat', methods=['POST'])
@require_api_key
def chat():
    # Your existing code
```

Frontend authentication in `frontend/script.js`:

```javascript
const API_KEY = 'your_student_key_from_teacher';

function sendRequest(endpoint, data) {
    return fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY  // Add API key to header
        },
        body: JSON.stringify(data)
    });
}
```

---

## 📊 Monitoring & Analytics

### Track Usage:

```python
# Add to backend/app.py
import json
from datetime import datetime

def log_usage(user_id, endpoint, tokens_used):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'endpoint': endpoint,
        'tokens': tokens_used
    }
    with open('usage_log.json', 'a') as f:
        json.dump(log_entry, f)
        f.write('\n')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_id = request.headers.get('X-User-ID', 'anonymous')
    # ... existing code ...
    log_usage(user_id, '/api/chat', tokens_used)
```

### Monitor Costs:

OpenAI Dashboard:
- https://platform.openai.com/account/billing/overview
- Set usage limits
- Monitor API costs in real-time

---

## 🔧 Troubleshooting Deployment

### Issue: "ModuleNotFoundError"
```bash
# Solution: Ensure requirements.txt is in root
# And all dependencies are listed
pip freeze > requirements.txt
```

### Issue: "API key not found"
```
Solution: Add environment variable in hosting dashboard
OPENAI_API_KEY=sk-...
```

### Issue: "Frontend can't connect to backend"
```
Solution: Update API_BASE_URL in frontend/script.js to your production URL
const API_BASE_URL = 'https://math-study-ai.onrender.com/api';
```

### Issue: "Slow responses"
Solutions:
1. Upgrade to paid tier
2. Use a faster model (GPT-3.5 instead of GPT-4)
3. Implement response caching
4. Use local Llama model

### Issue: "High costs"
Solutions:
1. Monitor API usage
2. Set spending limits
3. Cache responses
4. Use cheaper model
5. Implement rate limiting

---

## 🏆 Recommended Setup for Teachers/Scale

### Small Class (10-30 students):
- **Platform:** Render (free) or PythonAnywhere ($5/mo)
- **Model:** GPT-3.5 Turbo (~$5/mo)
- **Cost:** $5-10/month
- **Setup:** 10 minutes

### Medium Class (30-100 students):
- **Platform:** DigitalOcean ($5/mo)
- **Model:** GPT-3.5 Turbo ($10-20/mo)
- **Caching:** Implement response caching
- **Cost:** $15-30/month
- **Setup:** 1 hour

### Large Setup (100+ students):
- **Platform:** AWS or Google Cloud
- **Model:** GPT-3.5 Turbo with streaming
- **Caching:** Redis cache layer
- **Auth:** User authentication
- **Cost:** $50-200+/month
- **Setup:** 1-2 days

---

## 📝 Step-by-Step: Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Procfile
- [ ] Create runtime.txt
- [ ] Update requirements.txt
- [ ] Add .gitignore
- [ ] Sign up on hosting platform
- [ ] Connect GitHub repo
- [ ] Set environment variables
- [ ] Deploy
- [ ] Test with your domain
- [ ] Share link with students
- [ ] Monitor usage & costs
- [ ] Collect student feedback
- [ ] Iterate and improve

---

## 🎓 Final Tips

### For Teachers:
1. **Start free** - Use free tier to test
2. **Monitor costs** - Set spending limits
3. **Collect feedback** - Ask students what works
4. **Document access** - Write clear instructions
5. **Set limits** - Rate limit if needed

### For Students:
1. **Bookmark the URL** - Easy access
2. **Use browser cache** - Faster loading
3. **Share feedback** - Tell teacher what to improve
4. **Don't share API keys** - Keep credentials safe

---

## 🚀 Deploy Now!

**Quickest Option:** Use Render (5 minutes, free)

1. Push code to GitHub
2. Create `.gitignore`, `Procfile`, `runtime.txt`
3. Sign up on Render.com
4. Connect your GitHub repo
5. Add environment variables
6. Deploy!

Your Math Study AI is now live! 🎉

---

**Questions?** Check README.md or SETUP.md for more details.
