# 🚀 Quick Start Guide - Streamlit App

## ⚡ 5-Minute Setup

### Step 1: Install Streamlit Packages
```bash
cd MathStudyAI
pip install -r requirements_streamlit.txt
```

### Step 2: Create .env File

Create a file named `.env` in the `MathStudyAI` folder with:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
FLASK_ENV=development
```

**Get your OpenAI API key:**
1. Go to https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy and paste it in .env

### Step 3: Run the App

**For Students:**
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

**For Administrators:**
```bash
streamlit run admin_dashboard.py
```
Opens at: http://localhost:8501

---

## 📋 What Students Do

1. **Select Group** (1 or 2)
2. **Enter Student ID** (school ID)
3. **Take Pre-Assessment** (5 questions)
4. **Learn** (10 topics):
   - Group 1: AI Tutor guides you (searches web, personalizes)
   - Group 2: Free chat (ask any question)
5. **Take Final Assessment** (5 questions)
6. **See Results** (your improvement!)

---

## 📊 What Administrators Do

Run `streamlit run admin_dashboard.py` to see:

✅ **Overview Tab** - Student count, average scores  
✅ **Student Data Tab** - All full data (filter by group)  
✅ **Group 1 Analysis** - Customized Tutor results  
✅ **Group 2 Analysis** - ChatGPT results  
✅ **Comparison Tab** - Winner determination

---

## 📁 Project Structure

```
MathStudyAI/
├── app.py                              # Main student app
├── admin_dashboard.py                  # Admin analytics
├── agents/
│   ├── assessment_analyzer.py          # Rates student performance
│   ├── customized_tutor.py             # Group 1 AI tutor
│   └── chatgpt_agent.py                # Group 2 simple chat
├── utils/
│   └── data_storage.py                 # File-based storage
├── data/
│   ├── trigonometry_questions.json    # 15 questions (5+10+5)
│   ├── assessments.csv                 # Answers storage
│   ├── student_progress.json           # Learning history
│   ├── performance_ratings.csv         # AI analysis
│   └── comparison_results.csv          # Group comparison
├── .env                                # Your API key
├── .streamlit/
│   └── config.toml                     # Streamlit settings
└── requirements_streamlit.txt          # Dependencies
```

---

## 🧪 Test It

### Test with 1 Student
```bash
streamlit run app.py
```

1. Select Group 1
2. Enter Student ID: `TEST001`
3. Answer all questions
4. See analysis

### Test with Multiple Groups
1. Run first student (Group 1, ID: `STU001`)
2. Run second student (Group 2, ID: `STU002`)
3. Both complete all 3 assessments
4. Run admin dashboard to see comparison

---

## 📊 Data Flow

```
Student Answers (Form)
        ↓
Assessment Analyzer Agent (OpenAI)
        ↓
Performance Rating (JSON)
        ↓
Save to CSV (data/performance_ratings.csv)
        ↓
Admin Dashboard (Reads CSVs)
        ↓
Comparison & Winner (Calculated)
```

---

## 🔑 3 AI Agents Explained

### 1. Assessment Analyzer
**Role**: Grades assessments, identifies weak areas  
**Input**: Student answers + questions  
**Output**: Score %, weak areas, difficulty level  
**Uses**: OpenAI to analyze understanding

### 2. Customized Tutor (Group 1)
**Role**: Teaches with personalization  
**Input**: Student's pre-assessment weak areas  
**Output**: Tailored lesson explanations  
**Uses**: OpenAI + web search (simulated knowledge base)

### 3. ChatGPT Agent (Group 2)
**Role**: Simple Q&A chatbot  
**Input**: Student questions  
**Output**: Direct answers  
**Uses**: OpenAI, no customization

---

## ✅ Checklist Before Running

- [ ] Python 3.8+ installed
- [ ] `.env` file created with API key
- [ ] Requirements installed: `pip install -r requirements_streamlit.txt`
- [ ] `data/` folder exists
- [ ] `trigonometry_questions.json` is in data/
- [ ] `.streamlit/config.toml` exists

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Unable to import streamlit" | Run: `pip install streamlit==1.40.0` |
| "API key not found" | Add to `.env`: `OPENAI_API_KEY=sk-...` |
| "Questions not loading" | Check `data/trigonometry_questions.json` exists |
| "Data not saving" | Make sure `data/` folder writable |
| Port 8501 already in use | Run: `streamlit run app.py --server.port 8502` |

---

## 💡 Pro Tips

### Development
```bash
# Run with auto-reload disabled
streamlit run app.py --logger.level=debug

# Use different port
streamlit run app.py --server.port 8502

# Run admin dashboard simultaneously
# (In separate terminal)
streamlit run admin_dashboard.py --server.port 8502
```

### Student Testing
1. Test with `STU001`, `STU002`, etc.
2. Try both groups for comparison
3. Complete all 3 assessment phases
4. Check results

### Admin Testing
1. Add multiple students
2. Verify CSVs are created in `data/`
3. Run dashboard to see aggregated data
4. Export comparisons as CSV

---

## 📝 Customizing Questions

Edit `data/trigonometry_questions.json`:

```json
{
  "pre_assessment": [
    {
      "id": 1,
      "question": "Your question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A",
      "explanation": "Why A is correct"
    }
  ]
}
```

---

## 🎓 Next Steps

1. ✅ **Run app**: `streamlit run app.py`
2. ✅ **Invite students**: Share the URL
3. ✅ **Collect data**: Students complete assessments
4. ✅ **Analyze**: Run `streamlit run admin_dashboard.py`
5. ✅ **Publish**: Write up the research findings!

---

## 🚀 Ready?

```bash
streamlit run app.py
```

Your Trigonometry A/B testing platform is now live! 📐✨
