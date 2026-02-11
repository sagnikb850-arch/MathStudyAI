# 🔐 Admin Access Guide

## Overview

The admin panel allows administrators to:
- ✅ Monitor student progress in real-time
- ✅ Compare performance between Group 1 and Group 2
- ✅ Manage assessment questions (add/remove)
- ✅ Create practice questions for students
- ✅ Download data as CSV files

## Accessing Admin Panel

### Local Development

1. **Credentials** (set in `.env` file):
   - Username: `admin`
   - Password: `admin123`

2. **Access Steps**:
   - Open the app homepage
   - Click **"🔐 Admin Login"** button in the sidebar
   - Enter credentials
   - Click "Login"

### Production (Streamlit Cloud)

1. **Set Credentials in Secrets**:
   - Go to Streamlit Cloud app dashboard
   - Click "⚙ Settings" → "Secrets"
   - Add:
     ```toml
     ADMIN_USERNAME = "admin"
     ADMIN_PASSWORD = "YourSecurePassword123!"
     ```

2. **Access**:
   - Same as local: Click "🔐 Admin Login" in sidebar
   - Use the credentials you set in secrets

---

## Admin Dashboard Features

### 1. 📈 Progress Report

**View real-time student progress:**

- **Summary Metrics**:
  - Total students enrolled
  - Group 1 vs Group 2 counts
  - Overall average score

- **Filter Options**:
  - By group (All / Group 1 / Group 2)
  - By assessment type (Pre / Final)

- **Student Details Table**:
  - Student ID
  - Group assignment
  - Assessment type
  - Score percentage
  - Correct answers count
  - Difficulty level
  - Timestamp

- **Download Data**:
  - Export filtered data as CSV
  - Filename includes timestamp

---

### 2. 🏆 Comparison Report

**Compare Group 1 vs Group 2 performance:**

- **Winner Display**:
  - Shows which group improved more
  - Analysis summary

- **Side-by-Side Metrics**:
  - Pre-assessment averages
  - Final assessment averages
  - Improvement percentages (with delta indicators)

- **Visual Comparison**:
  - Interactive bar chart
  - Group-by-group comparison
  - Pre vs Final scores

- **Statistical Analysis**:
  - Automatically calculated from all student data
  - Updates in real-time as students complete assessments

---

### 3. 📝 Manage Questions

**Add or modify assessment questions:**

#### View Existing Questions

- Select question set:
  - Pre-Assessment (5 questions)
  - Learning Questions (concept-based)
  - Final Assessment (5 questions)

- Each question displays:
  - Full question text
  - Options (for assessments)
  - Correct answer
  - Explanation/hint

#### Add New Questions

**For Pre/Final Assessment:**
- Question text
- 4 multiple choice options
- Correct answer selection
- Explanation for students

**For Learning Questions:**
- Question text
- Concept name
- Hint/teaching point

**Saved to:** `data/trigonometry_questions.json`

---

### 4. 💡 Practice Questions

**Create additional practice questions for students:**

- **Target Groups**:
  - Both Groups (default)
  - Group 1 Only
  - Group 2 Only

- **Question Details**:
  - Question text
  - Concept/topic
  - Difficulty level (Easy/Medium/Hard)
  - Hint for students
  - Full solution/explanation

- **View Existing Practice Questions**:
  - Expandable list
  - Shows all details per question

**Saved to:** `data/practice_questions.json`

---

## Data Files Generated

### 1. `data/assessments.csv`
- Raw assessment answers
- Columns: student_id, group, assessment_type, q1-q5 answers, score, timestamp

### 2. `data/performance_ratings.csv`
- AI-analyzed performance data
- Columns: student_id, group, assessment_type, score_percentage, correct_answers, weak_areas, strong_areas, difficulty_level, timestamp

### 3. `data/comparison_results.csv`
- Group comparison calculations
- Columns: group1_avg_pre, group2_avg_pre, group1_avg_final, group2_avg_final, improvement_group1, improvement_group2, winner, analysis, timestamp

### 4. `data/student_progress.json`
- Student progress tracking (JSON)

### 5. `data/learning_history.json`
- Learning activity logs (JSON)

### 6. `data/practice_questions.json`
- Admin-created practice questions (JSON)

---

## Security Best Practices

### Local Development
✅ `.env` file with admin credentials  
✅ Never commit `.env` to git  

### Production (Streamlit Cloud)
✅ Use Streamlit Secrets (encrypted)  
✅ Use strong passwords (12+ characters, mixed case, numbers, symbols)  
✅ Change default password immediately  

### Recommended Password Format
```
MinLength: 12 characters
Include: Uppercase, lowercase, numbers, special characters
Example: Admin@Trig2026!Secure
```

---

## Workflow Example: 20 Students

### Before Study Starts
1. ✅ Login to admin panel
2. ✅ Review existing questions
3. ✅ Add practice questions if needed
4. ✅ Share student access link

### During Study (Students Working)
1. ✅ Monitor "Progress Report" tab
2. ✅ Check how many students completed each stage
3. ✅ Watch real-time scores

### After Study Completes
1. ✅ Go to "Comparison" tab
2. ✅ Review winner and improvement stats
3. ✅ Download data from "Progress Report"
4. ✅ Export CSV for analysis in Excel/Python

---

## Troubleshooting

### Can't Login
- ❌ Check username/password in `.env` or Streamlit Secrets
- ❌ Ensure no typos (case-sensitive)
- ❌ Verify secrets are saved properly on Streamlit Cloud

### No Data Showing
- ❌ Students must complete assessments first
- ❌ Check that `data/` folder exists
- ❌ Verify file permissions

### Charts Not Displaying
- ❌ Plotly may not be installed
- ❌ Run: `pip install plotly`
- ❌ Check requirements.txt includes plotly

### Questions Not Saving
- ❌ Check write permissions on `data/` folder
- ❌ Verify JSON format is valid
- ❌ Streamlit Cloud: data persists during session, download backups

---

## Tips for Managing 20 Students

1. **Before Session**:
   - Test admin login works
   - Verify all questions load correctly
   - Prepare practice questions in advance

2. **During Session**:
   - Keep admin panel open in separate tab
   - Monitor progress every 5-10 minutes
   - Be ready to answer student questions

3. **After Session**:
   - Download CSV immediately (Streamlit Cloud storage is ephemeral)
   - Save backup of all data files
   - Run comparison analysis

4. **Data Backup**:
   ```bash
   # Download these files after study:
   - assessments.csv
   - performance_ratings.csv
   - comparison_results.csv
   ```

---

## FAQ

**Q: Can students see the admin panel?**  
A: No, only accessible with admin credentials.

**Q: Can multiple admins be logged in?**  
A: Yes, but each needs their own browser session.

**Q: How do I change the admin password?**  
A: Update `ADMIN_PASSWORD` in `.env` (local) or Streamlit Secrets (cloud).

**Q: Can I add more than one admin user?**  
A: Currently supports one admin account. For multiple admins, extend the authentication logic in `app.py`.

**Q: Do questions update for students immediately?**  
A: No, students need to refresh their browser or restart their session to see new questions.

**Q: How long is data stored on Streamlit Cloud?**  
A: Only during the app's runtime. Download CSVs regularly!

---

## Support

For issues or questions:
1. Check this guide first
2. Review app logs in Streamlit Cloud dashboard
3. Check `data/` folder permissions and files

---

**Admin panel is now ready! 🚀**

Login credentials:
- Local: `admin` / `admin123`
- Production: Set in Streamlit Cloud Secrets
