# 📦 GitHub Setup Guide

Simple step-by-step guide to push your Math Study AI code to GitHub (required for cloud deployment).

## Why GitHub?

- ✅ Required for deploying on Render/Railway/CloudRun
- ✅ Version control for your code
- ✅ Easy to manage updates
- ✅ Share code with team members
- ✅ Free to use

---

## Step 1: Create GitHub Account (Free)

1. Go to: https://github.com/join
2. Sign up with email
3. Verify email
4. Choose free plan (recommended)

---

## Step 2: Install Git on Your Computer

### Windows:

```powershell
# Install via PowerShell/Terminal
# Download from: https://git-scm.com/download/win
# Run installer and follow instructions
# Restart terminal after installation

# Verify installation
git --version
```

---

## Step 3: Configure Git

```powershell
# Set your name
git config --global user.name "Your Name"

# Set your email (use same as GitHub)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

## Step 4: Create GitHub Repository

1. Log in to GitHub (https://github.com)
2. Click "+" icon (top right) → "New repository"
3. **Fill in details:**
   - Repository name: `MathStudyAI`
   - Description: "AI-powered Math Tutoring Application"
   - Visibility: **Public** (so hosting can access)
   - Initialize: **Skip** (we'll push existing code)
4. Click "Create repository"

---

## Step 5: Push Your Code to GitHub

### From PowerShell in your project folder:

```powershell
# Navigate to your project
cd c:\Users\soura\OneDrive\Documents\APRStudy\MathStudyAI

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Math Study AI application"

# Check your GitHub repo for these commands
# They will look like:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/MathStudyAI.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 6: Verify on GitHub

1. Go to your GitHub repo
2. Refresh the page
3. You should see all your files:
   - `backend/`
   - `frontend/`
   - `agent/`
   - `config/`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`
   - `README.md`
   - etc.

---

## Common Issues

### "fatal: not a git repository"

**Solution:** Run this first:
```powershell
git init
```

### "fatal: destination path already exists"

**Solution:** Already initialized, skip `git init`

### "Permission denied (publickey)"

**Solution:** Set up SSH key:
```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub
# Copy content from: C:\Users\YOUR_NAME\.ssh\id_ed25519.pub
# GitHub Settings → SSH Keys → Add SSH Key
```

---

## How to Update Code Later

Once on GitHub, updating is simple:

```powershell
# Make changes to files

# Add changes
git add .

# Commit
git commit -m "Describe what changed"

# Push to GitHub
git push
```

This automatically redeploys on Render!

---

## 🎯 Next Steps

After pushing to GitHub:

1. Go to https://render.com
2. Sign in with GitHub
3. Deploy your repo (see DEPLOY_NOW.md)

---

## ℹ️ Understanding Git

### Key Concepts:

1. **Repository** - Your project folder on GitHub
2. **Commit** - Save point in your code
3. **Branch** - Separate version of code
4. **Push** - Upload code to GitHub
5. **Pull** - Download code from GitHub

### Typical Workflow:

```
Edit Files
    ↓
git add .
    ↓
git commit -m "Description"
    ↓
git push
    ↓
GitHub Updated
    ↓
Render Auto-Deploys
```

---

## 🔒 .gitignore Explanation

Your `.gitignore` tells Git NOT to upload certain files:

```
.env                # Don't upload API keys!
__pycache__/        # Generated Python files
venv/               # Virtual environment
.vscode/            # IDE settings
*.pyc               # Compiled Python
```

This is important! Never upload `.env` with secret keys.

---

## ✅ Verification Checklist

- [ ] GitHub account created
- [ ] Git installed on computer
- [ ] Git configured with name/email
- [ ] GitHub repo created (public)
- [ ] Code pushed to GitHub
- [ ] All files visible on GitHub
- [ ] `.env` NOT on GitHub (check!)
- [ ] `Procfile` on GitHub
- [ ] `runtime.txt` on GitHub
- [ ] `requirements.txt` on GitHub

---

## Ready to Deploy?

Once GitHub is set up:

1. Go to **DEPLOY_NOW.md** for quick deployment
2. OR read **DEPLOYMENT.md** for detailed options

---

## 📚 Learn More

- GitHub Docs: https://docs.github.com/
- Git Tutorial: https://git-scm.com/book/en/v2
- Beginner's Guide: https://guides.github.com/

---

**All set? Let's deploy! 🚀**
