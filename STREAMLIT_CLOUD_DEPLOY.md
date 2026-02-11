# 🚀 Deploy to Streamlit Cloud - Step-by-Step Guide

## ✅ Pre-Deployment Checklist

Your app is ready to deploy! Here's what we've prepared:

- ✅ `app.py` - Main Streamlit application
- ✅ `requirements_streamlit.txt` - All dependencies listed
- ✅ `data/trigonometry_questions.json` - Questions data
- ✅ `.gitignore` - Configured to exclude secrets
- ✅ `.streamlit/config.toml` - Streamlit configuration

---

## 📋 Step 1: Push Code to GitHub

### 1.1 Initialize Git Repository (if not done)

```bash
cd C:\Users\soura\OneDrive\Documents\APRStudy\MathStudyAI
git init
git add .
git commit -m "Initial commit - Math Study AI for trigonometry assessment"
```

### 1.2 Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `MathStudyAI` (or any name you prefer)
3. Description: `AI-powered trigonometry learning platform for A/B testing`
4. Make it: **Public** (required for Streamlit Community Cloud free tier)
5. **Don't** initialize with README (we already have files)
6. Click **"Create repository"**

### 1.3 Push to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/MathStudyAI.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy on Streamlit Cloud

### 2.1 Sign Up / Login

1. Go to: https://share.streamlit.io
2. Click **"Sign up"** or **"Sign in"**
3. Use your **GitHub account** to sign in (easiest)

### 2.2 Create New App

1. Click **"New app"** on the dashboard
2. Fill in the deployment form:
   - **Repository**: Select `YOUR_USERNAME/MathStudyAI`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain or leave default

### 2.3 Add Secrets (CRITICAL!)

Before clicking Deploy, add your OpenAI API key:

1. Click **"Advanced settings"**
2. Find the **"Secrets"** section
3. Paste this in the secrets box (replace with YOUR actual API key):

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
MODEL_NAME = "gpt-4o-mini"
AI_MODEL = "openai"
MAX_TOKENS = 1024
TEMPERATURE = 0.7
```

4. Click **"Save"**

### 2.4 Set Python Requirements

By default, Streamlit Cloud looks for `requirements.txt`, but we need `requirements_streamlit.txt`.

**Option A: Rename the file** (recommended)

```bash
# In your local repository
cd C:\Users\soura\OneDrive\Documents\APRStudy\MathStudyAI
copy requirements_streamlit.txt requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt for Streamlit Cloud"
git push
```

**Option B: Use Advanced Settings**

In Streamlit Cloud:
1. Click **"Advanced settings"**
2. Under **"Python requirements"**, change to: `requirements_streamlit.txt`

### 2.5 Deploy!

1. Click **"Deploy"** button
2. Wait 3-5 minutes for build (watch the logs)
3. Once deployed, you'll get a URL like:
   ```
   https://YOUR_USERNAME-mathstudyai.streamlit.app
   ```

---

## ✅ Step 3: Test Your Deployment

### 3.1 Test the App Flow

1. Open the app URL in incognito/private browser
2. Test the full student journey:
   - ✅ Select Group 1 or Group 2
   - ✅ Register with a test student ID
   - ✅ Complete pre-assessment
   - ✅ Test learning phase (AI responses)
   - ✅ Complete final assessment

### 3.2 Check for Errors

Watch the Streamlit Cloud logs:
- Go to your app dashboard
- Click **"Manage app"**
- Check **"Logs"** tab for any errors

Common issues:
- **401 API error**: Wrong API key in secrets
- **429 Quota error**: No billing on OpenAI account
- **Module not found**: Missing package in requirements file

---

## 👥 Step 4: Share with 20 Students

### 4.1 Get Your App URL

Your app will be at:
```
https://YOUR_USERNAME-mathstudyai.streamlit.app
```

### 4.2 Share Instructions with Students

**Email Template:**

```
Subject: Trigonometry Learning Study - Access Instructions

Dear Students,

You're invited to participate in our trigonometry learning study!

📐 Access the platform here:
👉 https://YOUR_USERNAME-mathstudyai.streamlit.app

Instructions:
1. Click the link above
2. Choose your assigned group (Group 1 or Group 2)
3. Enter your Student ID when prompted
4. Complete the pre-assessment (5 questions)
5. Learn using the AI tutor
6. Complete the final assessment (5 questions)

⏰ Time Required: 20-30 minutes
📱 Works on: Desktop, tablet, or phone
🔒 Privacy: Your ID is used only for this study

Questions? Reply to this email.

Thank you for participating!
```

### 4.3 Student Distribution

- **Group 1 (Customized Tutor)**: 10 students
- **Group 2 (ChatGPT Interface)**: 10 students

Assign students to groups before they start.

---

## 📊 Step 5: Monitor & Download Results

### 5.1 Access Admin Dashboard

While students are using the app, data is stored in:
- `data/assessments.csv` - All assessment answers
- `data/performance_ratings.csv` - AI analysis of performance
- `data/learning_history.json` - Student interactions

### 5.2 Download Results After Study

**Important**: Streamlit Cloud uses ephemeral storage. Download data regularly!

**Option A: Use Admin Dashboard** (if you created one)
- Add this to your app for easy download

**Option B: Access via Streamlit Cloud**
- Use `admin_dashboard.py` to view results

**Option C: Via GitHub (if you commit data)**
```bash
# In your app, add a download button
import streamlit as st
import pandas as pd

df = pd.read_csv('data/assessments.csv')
st.download_button("Download Results", data=df.to_csv(), file_name="results.csv")
```

---

## 💰 Cost Estimate for 20 Students

### OpenAI API Costs (GPT-4o-mini)

- **Per student**: ~$0.10 - $0.20
- **20 students**: ~$2 - $4 total
- **Buffer**: Set billing limit to $10 to be safe

### Streamlit Cloud

- **Community tier**: FREE
- **Supports**: Up to 1GB RAM, unlimited visitors
- **20 concurrent students**: ✅ Supported

**Total Cost**: ~$2-4 for OpenAI API usage only

---

## ⚠️ Important Notes

### For Students:
1. **Keep browser open**: Session state is lost if tab closes
2. **One session per student**: Complete start-to-finish
3. **Stable internet**: Required for AI responses

### For You:
1. **Monitor logs**: Check for API errors during study
2. **Backup data**: Download CSV files after each session
3. **API billing**: Set a $10 usage limit as safety
4. **App restarts**: Streamlit may restart if idle >7 days

---

## 🐛 Troubleshooting

### App Won't Start
```
Check logs → Look for import errors → Verify requirements_streamlit.txt
```

### API Errors (401, 429)
```
Go to Streamlit Cloud → Manage app → Secrets → Verify OPENAI_API_KEY
Check OpenAI billing: https://platform.openai.com/account/billing
```

### Data Not Saving
```
Streamlit uses ephemeral storage - data resets on app restart
Download CSV files after study completes
Consider adding cloud storage (S3, Google Sheets) for production
```

### Students Can't Access
```
Verify URL is correct and public
Check if app is "sleeping" - first visit may take 30 seconds to wake
```

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **OpenAI Docs**: https://platform.openai.com/docs
- **Streamlit Forum**: https://discuss.streamlit.io

---

## ✅ Quick Deployment Checklist

- [ ] Git repository initialized
- [ ] Code pushed to GitHub (public repo)
- [ ] Streamlit Cloud account created
- [ ] App deployed from GitHub repo
- [ ] Secrets added (OPENAI_API_KEY)
- [ ] OpenAI billing configured
- [ ] Test student flow works end-to-end
- [ ] Share URL with students
- [ ] Monitor during study session
- [ ] Download results after completion

**Ready to deploy? Follow the steps above!** 🚀
