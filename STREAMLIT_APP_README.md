# 📐 Trigonometry A/B Testing Platform - Streamlit App

A comprehensive research platform comparing two teaching approaches for Trigonometry:
- **Group 1**: Customized AI Tutor (searches internet, personalizes teaching)
- **Group 2**: ChatGPT-like interface (simple Q&A)

## 🎯 Features

### Study Design
✅ Pre-assessment (5 questions)  
✅ Learning phase (10 concepts)  
✅ Final assessment (5 questions)  
✅ Automated performance comparison  

### 3 AI Agents
1. **Assessment Analyzer** - Rates student performance, identifies weak areas
2. **Customized Tutor** - Searches web, teaches based on student level
3. **ChatGPT Agent** - Simple Q&A interface

### File-Based Storage (No Database!)
- `assessments.csv` - Pre/final assessment answers
- `student_progress.json` - Learning history
- `performance_ratings.csv` - Agent analysis results
- `comparison_results.csv` - Group 1 vs Group 2 analysis
- `trigonometry_questions.json` - Question sets

## 🚀 How to Run

### 1. Install Requirements
```bash
pip install -r requirements_streamlit.txt
```

### 2. Set Up Environment
Create `.env` file with:
```
OPENAI_API_KEY=sk-proj-your-key-here
FLASK_ENV=development
```

### 3. Run the App
```bash
streamlit run app.py
```

App will open at: `http://localhost:8501`

## 📋 Student Flow

### Step 1: Group Selection
- Student chooses Group 1 or Group 2
- Saves their choice

### Step 2: Register
- Enter School Student ID
- System stores for tracking

### Step 3: Pre-Assessment
- Answer 5 questions
- AI Analyzer rates performance
- System identifies weak areas

### Step 4: Learning Phase
**Group 1 (Customized Tutor):**
- AI tutors 10 concepts
- Searches internet for resources
- Adapts to student's weak areas
- Can ask follow-up questions

**Group 2 (ChatGPT):**
- Free-form chat interface
- Ask any question
- Self-paced learning
- Same 10 topics to explore

### Step 5: Final Assessment
- Answer 5 new questions
- AI rates final performance
- System calculates improvement

### Step 6: Results
- Individual performance metrics
- Group 1 vs Group 2 comparison
- Winner determination

## 📊 Data Storage Structure

```
data/
├── trigonometry_questions.json    # All question sets
├── assessments.csv                # Assessment answers
├── student_progress.json          # Learning history
├── performance_ratings.csv        # AI ratings
└── comparison_results.csv         # Group comparison
```

## 🤖 AI Agents Explained

### Assessment Analyzer
- Uses OpenAI to evaluate answers
- Generates JSON scores: percentage, weak/strong areas
- Returns difficulty level and recommendations

### Customized Tutor (Group 1)
- Analyzes pre-assessment results
- Creates personalized teaching for each concept
- Searches knowledge base for topics
- Answers student questions with context
- Builds on previous weak areas

### ChatGPT Agent (Group 2)
- Simple conversational interface
- Maintains chat history
- No customization
- Standard Q&A

## 📈 Analysis & Comparison

The system automatically:
1. Calculates pre-assessment average for each group
2. Calculates final assessment average for each group
3. Calculates improvement: `Final - Pre`
4. Determines winner: larger improvement
5. Stores comparison results

## 📁 Questions Format (JSON)

```json
{
  "pre_assessment": [
    {
      "id": 1,
      "question": "What is sin(30°)?",
      "options": ["0.5", "0.866", "1", "0"],
      "correct_answer": "0.5",
      "explanation": "sin(30°) = 0.5"
    }
  ]
}
```

## 🔧 Admin Features (TODO)

Add admin page to view:
- All student data
- Group statistics
- View learning progress
- Export reports

## 💾 Storage Benefits (No Database)

✅ **No Setup**: No database installation  
✅ **Portable**: Files go anywhere  
✅ **Simple**: Everyone can read/edit CSVs  
✅ **Backup**: Just copy the `data/` folder  
✅ **Git-Friendly**: Track changes in version control  

## ⚠️ Limitations & Improvements

**Current Limitations:**
- No multi-user concurrency (use database for production)
- Local file storage only
- No user authentication
- No real web search (using knowledge base)

**For Production:**
- Add database (PostgreSQL/MongoDB)
- Add user authentication
- Implement real web search (Google Custom Search API)
- Add admin dashboard
- Add analytics
- Deploy on cloud (Streamlit Cloud, Heroku)

## 🧪 Testing

### Test Pre-Assessment
1. Open app, select group
2. Enter test ID: "TEST001"
3. Answer questions (should save to CSV)

### Test Learning
- Group 1: Click explain buttons
- Group 2: Type questions

### Test Comparison
- Run multiple students in both groups
- Check `comparison_results.csv`

## 🆘 Troubleshooting

### "Error: undefined"
- Check if `.env` has valid OpenAI API key
- Check internet connection

### Questions not loading
- Verify `data/trigonometry_questions.json` exists
- Check JSON syntax

### Data not saving
- Check if `data/` folder has write permissions
- Check if CSV files exist

## 📞 Support

For issues:
1. Check `.streamlit/` config
2. Restart Streamlit: `Ctrl+C` then `streamlit run app.py`
3. Check logs for errors

## 📚 Next Steps

1. ✅ Set up OpenAI API key
2. ✅ Run Streamlit app  
3. ✅ Get students to use it
4. ✅ Analyze results
5. ✅ Compare performance

---

**Ready to research?** Run `streamlit run app.py` now! 🚀
