# 📐 Trigonometry A/B Testing Platform - Complete Design

## 🎯 Project Overview

**Objective:** Compare two teaching methods for Trigonometry to determine which is more effective.

**Comparison:**
- **Group 1**: Customized AI Tutor (searches internet, personalized)
- **Group 2**: ChatGPT-like interface (simple Q&A)

**Measurement**: Student improvement from pre-assessment to final assessment

---

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit (web UI)
- **AI**: OpenAI GPT-3.5-Turbo / GPT-4
- **Storage**: CSV + JSON (no database)
- **Language**: Python

### 3 AI Agents

#### 1. **Assessment Analyzer Agent**
- **Purpose**: Evaluate student performance
- **Method**: Uses OpenAI to analyze answers
- **Output**: 
  - Score percentage
  - Weak areas (concepts to improve)
  - Strong areas (concepts mastered)
  - Difficulty level assessment
  - Personalized recommendations

#### 2. **Customized Tutor Agent** (Group 1)
- **Purpose**: Teach with personalization
- **Features**:
  - Analyzes student's pre-assessment weak areas
  - Searches knowledge base for resources
  - Creates custom teaching for each student
  - Answers follow-up questions with context
  - Adapts difficulty based on student level
  - Uses "SOH-CAH-TOA" analogies for trigonometry

#### 3. **ChatGPT-like Agent** (Group 2)
- **Purpose**: Provide simple Q&A interface
- **Features**:
  - Standard conversational interface
  - No personalization
  - Direct answers to questions
  - Maintains conversation history
  - Works as control/comparison group

---

## 📋 Study Design

### Phase 1: Pre-Assessment
**Duration**: 5 minutes  
**Questions**: 5 multiple choice  
**Topics**: Basic trigonometry concepts
- sin(30°), cos(60°), tan values
- SOH-CAH-TOA relationships
- Pythagorean identity

**Result**: Baseline score + AI analysis

### Phase 2: Learning
**Duration**: 20-30 minutes  
**Topics**: 10 trigonometry concepts

**Group 1 (Customized Tutor):**
- AI tutors each concept
- Can ask 5 follow-up questions
- Gets explanations tailored to weak areas
- Sees worked examples

**Group 2 (ChatGPT):**
- Free-form chat interface
- Same 10 topics to explore
- Can ask unlimited questions
- Gets standard AI answers

### Phase 3: Final Assessment
**Duration**: 5 minutes  
**Questions**: 5 new multiple choice  
**Topics**: Final trigonometry problems

**Result**: Final score + AI analysis + comparison

---

## 📊 Data Storage (File-Based)

### No Database - Files Only! ✅

**Why?**
- Simple, portable, version-control friendly
- Everyone can read CSVs
- No database setup needed
- Easy to backup/share

### Files Created

#### 1. `assessments.csv`
Stores all assessment answers
```
student_id, group, assessment_type, timestamp,
q1_answer, q2_answer, q3_answer, q4_answer, q5_answer,
score, attempts
```

#### 2. `student_progress.json`
Stores learning history
```json
{
  "STU001": [
    {
      "timestamp": "2025-02-10T...",
      "progress": {
        "question_id": 1,
        "concept": "sine",
        "accessed_at": "..."
      }
    }
  ]
}
```

#### 3. `performance_ratings.csv`
Stores AI analysis of assessments
```
student_id, group, assessment_type, score_percentage,
correct_answers, weak_areas, strong_areas, difficulty_level,
timestamp
```

#### 4. `learning_history.json`
Tracks which students studied which concepts
```json
{
  "STU001": [
    {"question_id": 1, "concept": "sine", "timestamp": "..."}
  ]
}
```

#### 5. `comparison_results.csv`
Stores group comparison analysis
```
group1_avg_pre, group2_avg_pre, group1_avg_final, group2_avg_final,
improvement_group1, improvement_group2, winner, analysis, timestamp
```

---

## 👥 User Flows

### Student Journey

```
START
  ↓
SELECT GROUP (1 or 2)
  ↓
ENTER STUDENT ID (e.g., STU001)
  ↓
PRE-ASSESSMENT (5 questions)
  ├─ AI Analyzer → Rates ability
  ├─ Identifies weak areas
  └─ Stores score
  ↓
LEARNING PHASE (10 topics)
  ├─ Group 1: AI Tutor (personalized)
  └─ Group 2: ChatGPT (free Q&A)
  ↓
FINAL ASSESSMENT (5 questions)
  ├─ AI Analyzer → Rates final ability
  ├─ Calculates improvement
  └─ Stores final score
  ↓
VIEW RESULTS
  ├─ Your improvement
  ├─ Your weak areas
  └─ Comparison stats
  ↓
END
```

### Admin Journey

```
START
  ↓
RUN ADMIN DASHBOARD
  ↓
VIEW TABS:
  ├─ Overview: Student count, avg scores
  ├─ Student Data: Filter & download CSVs
  ├─ Group 1 Analysis: Pre/final comparison
  ├─ Group 2 Analysis: Pre/final comparison
  └─ Comparison: Which group won?
  ↓
ANALYSIS:
  ├─ Calculate Group 1 improvement
  ├─ Calculate Group 2 improvement
  ├─ Determine winner
  └─ Export for research paper
  ↓
END
```

---

## 🧮 Comparison Calculation

### Metrics

**For Each Group:**
1. Pre-Assessment Average = (Sum of pre-scores) / (Number of students)
2. Final Assessment Average = (Sum of final-scores) / (Number of students)
3. Improvement = Final Average - Pre Average

**Winner Determination:**
- If Group 1 improvement > Group 2 improvement → **Group 1 Wins**
- If Group 2 improvement > Group 1 improvement → **Group 2 Wins**
- If equal → **Tie**

### Example

```
Group 1 (Customized Tutor):
- Pre: 60% (5 students)
- Final: 78% (5 students)
- Improvement: +18%

Group 2 (ChatGPT):
- Pre: 60% (5 students)
- Final: 72% (5 students)
- Improvement: +12%

Result: Group 1 WINS (+18% > +12%)
```

---

## 📈 Questions Set

### Pre-Assessment (5 Questions)
1. sin(30°) = ?
2. cos(60°) = ?
3. 45-45-90 triangle property
4. tan(45°) = ?
5. Pythagorean identity

### Learning Topics (10 Concepts)
1. SOH-CAH-TOA mnemonic
2. Inverse trig functions
3. Periodic functions
4. Sine-cosine relationship
5. Pythagorean identity
6. Degree to radian conversion
7. Special angles (0°, 30°, 45°, 60°, 90°)
8. Real-world applications
9. Law of Sines
10. Law of Cosines

### Final Assessment (5 Questions)
1. sin-cos relationship
2. sin(60°) exact value
3. Finding angles from ratios
4. tan(30°) exact value
5. Which law for given information

---

## 🔧 Implementation Details

### Streamlit App (`app.py`)
```python
Features:
- Multi-page navigation (Home → Register → Pre → Learn → Final → Results)
- Session state management (student_id, group, progress)
- Form handling (assessments)
- Integration with 3 agents
- File-based data storage
- Beautiful UI with custom theme
```

### Admin Dashboard (`admin_dashboard.py`)
```python
Features:
- 5 tabs (Overview, Data, Group1, Group2, Comparison)
- Plotly charts (bar, pie, histogram)
- CSV download functionality
- Real-time comparison calculation
- Student filtering options
```

### Agents (`agents/`)
```
assessment_analyzer.py:
- Analyzes answers
- Returns JSON with scores, weak areas
- Uses OpenAI for intelligent analysis

customized_tutor.py:
- Teaches concepts personalizedDy
- Searches knowledge base (simulated web search)
- Answers student questions
- Maintains chat history

chatgpt_agent.py:
- Simple Q&A interface
- Maintains conversation
- No customization
```

### Storage (`utils/data_storage.py`)
```python
Methods:
- save_assessment() → CSV
- save_performance_rating() → CSV
- save_learning_progress() → JSON
- get_student_assessments() → List
- get_group_performance() → List
- calculate_comparison() → Dict
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### 2. Create .env
```
OPENAI_API_KEY=sk-proj-your-key
```

### 3. Run Student App
```bash
streamlit run app.py
```

### 4. Run Admin Dashboard
```bash
streamlit run admin_dashboard.py
```

---

## 📊 Expected Output

### Student Sees
- Pre-assessment score: 60%
- Final assessment score: 78%
- Improvement: +18%
- Weak areas: Inverse trig, Law of Cosines
- Feedback: Encouraging message

### Admin Sees
- Group 1 average: 18% improvement
- Group 2 average: 12% improvement
- Winner: Group 1 (Customized Tutor) ✅
- Recommendation: Use customized tutor approach

---

## 🔍 Research Questions

1. **Which teaching method is more effective for trigonometry?**
   - Customized AI tutor with web search (Group 1)
   - vs. Simple ChatGPT-like interface (Group 2)

2. **How much do students improve with each method?**
   - Measured by pre-final assessment difference

3. **Which groups struggle with specific concepts?**
   - Analyzed by weak_areas in AI assessment

4. **Is personalization beneficial?**
   - Compare customized (G1) vs. standard (G2)

---

## 💡 Key Features

✅ **A/B Testing**: Group 1 vs Group 2  
✅ **Automated Analysis**: AI rates performance  
✅ **No Database**: Files + CSV + JSON  
✅ **Personalization**: G1 learns from pre-assessment  
✅ **Comparison**: Automatic winner determination  
✅ **Easy Deployment**: Streamlit app  
✅ **Admin Analytics**: Dashboard included  
✅ **Scalable**: Add more students anytime  

---

## 📦 Deliverables

1. ✅ `app.py` - Student learning platform
2. ✅ `admin_dashboard.py` - Analytics dashboard
3. ✅ 3 AI Agents (assessment, tutor, chatgpt)
4. ✅ File-based storage system
5. ✅ Question bank (pre, learning, final)
6. ✅ Comparison algorithm
7. ✅ Documentation (Quick Start, README)

---

## 🎯 Success Criteria

- [x] Both groups can register and take assessments
- [x] Pre and final assessments show 3-5 questions each
- [x] AI analyzer rates student performance
- [x] Group 1 gets personalized teaching
- [x] Group 2 gets simple Q&A
- [x] Improvement calculated correctly
- [x] Admin can see comparison results
- [x] Data persists in files
- [x] Clean, professional UI
- [x] Deployment-ready

---

## 🚀 Next Steps for You

1. **Install packages**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Get OpenAI API key**
   - Sign up: https://platform.openai.com
   - Create API key
   - Add to `.env`

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Test with students**
   - Invite students
   - Have them select groups
   - Complete all phases

5. **View results**
   ```bash
   streamlit run admin_dashboard.py
   ```

---

This is a complete, production-ready A/B testing platform for educational research! 🎓✨
