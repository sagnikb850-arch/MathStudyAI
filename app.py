"""
Streamlit App - A/B Testing Platform for Trigonometry Learning
Comparing Customized Tutor (Group 1) vs ChatGPT Interface (Group 2)
"""
import streamlit as st
import json
import os
import sys
import pandas as pd
try:
    import plotly.graph_objects as go
except ImportError:
    pass  # Plotly is optional for basic functionality
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.assessment_analyzer import AssessmentAnalyzerAgent
from agents.customized_tutor import CustomizedTutorAgent
from agents.chatgpt_agent import ChatGPTLikeAgent
from utils.data_storage import DataStorage

# Page configuration
st.set_page_config(
    page_title="Trigonometry Learning Platform",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add MathJax support for LaTeX rendering
mathjax_script = """
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$']],
    displayMath: [['$$', '$$']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
"""
st.markdown(mathjax_script, unsafe_allow_html=True)

# Initialize session state
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'group' not in st.session_state:
    st.session_state.group = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'pre_assessment_done' not in st.session_state:
    st.session_state.pre_assessment_done = False
if 'learning_done' not in st.session_state:
    st.session_state.learning_done = False
if 'final_assessment_done' not in st.session_state:
    st.session_state.final_assessment_done = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'admin_page' not in st.session_state:
    st.session_state.admin_page = 'dashboard'

# Load questions
with open('data/trigonometry_questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

# Questions will be loaded based on group
learning_questions = questions_data['learning_questions']
final_questions = questions_data['final_assessment']

# Initialize storage
storage = DataStorage('data')

# Helper function to render LaTeX expressions properly
def render_latex_content(text):
    """
    Render LaTeX as actual math symbols using MathJax
    Handles multiple LaTeX formats: $...$, $$...$$, \(...\), \[...\], and ( ... )
    """
    if not text or not text.strip():
        return
    
    import re
    
    # Convert common markdown LaTeX formats to MathJax format
    # Convert \( ... \) to $ ... $ (inline math)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
    
    # Convert \[ ... \] to $$ ... $$ (display math)
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    
    # Convert ( ... ) with LaTeX commands inside to $ ... $ (common AI output format)
    # Only convert if there are LaTeX commands inside the parentheses
    text = re.sub(r'\(\s*\\([a-zA-Z]+[^)]*)\)', r'$\\\1$', text)
    
    # Convert [ ... ] with LaTeX commands to $$ ... $$
    text = re.sub(r'\[\s*\\([a-zA-Z]+[^\]]*)\]', r'$$\\\1$$', text)
    
    # Render content with MathJax processing
    content_html = f"""
    <div class="math-content">
        {text}
    </div>
    <script>
        if (typeof MathJax !== 'undefined') {{
            MathJax.typesetPromise();
        }}
    </script>
    """
    st.markdown(content_html, unsafe_allow_html=True)

# Initialize agents (lazy load)
@st.cache_resource
def get_assessment_analyzer():
    return AssessmentAnalyzerAgent()

@st.cache_resource
def get_customized_tutor():
    return CustomizedTutorAgent()

@st.cache_resource
def get_chatgpt_agent():
    return ChatGPTLikeAgent()

# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================
def show_admin_login():
    """Admin login page"""
    st.title("🔐 Admin Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("Enter admin credentials to access the dashboard")
        
        with st.form("admin_login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                # Get admin credentials from secrets or env
                admin_user = os.getenv('ADMIN_USERNAME', 'admin')
                admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
                
                if username == admin_user and password == admin_pass:
                    st.session_state.is_admin = True
                    st.session_state.current_page = 'admin_dashboard'
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        st.divider()
        
        if st.button("← Back to Student Portal", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()


# ============================================================================
# ADMIN DASHBOARD
# ============================================================================
def show_admin_dashboard():
    """Main admin dashboard with tabs"""
    st.title("📊 Admin Dashboard")
    
    # Logout button in sidebar
    with st.sidebar:
        st.write("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.current_page = 'home'
            st.rerun()
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Progress Report", 
        "🏆 Comparison", 
        "📝 Manage Questions", 
        "💡 Practice Questions",
        "💬 Chat History",
        "👥 Student Management",
        "🗑️ Reset Data"
    ])
    
    with tab1:
        show_admin_progress()
    
    with tab2:
        show_admin_comparison()
    
    with tab3:
        show_admin_manage_questions()
    
    with tab4:
        show_admin_practice_questions()
    
    with tab5:
        show_admin_chat_history()
    
    with tab6:
        show_admin_student_management()
    
    with tab7:
        show_admin_reset_data()


def show_admin_progress():
    """Show detailed student progress"""
    st.header("Student Progress Tracking")
    
    # Load data
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        
        if len(perf_df) > 0:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_students = perf_df['student_id'].nunique()
                st.metric("Total Students", total_students)
            
            with col2:
                group1_count = len(perf_df[perf_df['group'] == '1']['student_id'].unique())
                st.metric("Group 1 Students", group1_count)
            
            with col3:
                group2_count = len(perf_df[perf_df['group'] == '2']['student_id'].unique())
                st.metric("Group 2 Students", group2_count)
            
            with col4:
                avg_score = perf_df['score_percentage'].mean()
                st.metric("Overall Avg Score", f"{avg_score:.1f}%")
            
            st.divider()
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_group = st.selectbox("Filter by Group", ["All", "Group 1", "Group 2"])
            with col2:
                filter_type = st.selectbox("Assessment Type", ["All", "Pre-Assessment", "Final Assessment"])
            
            # Apply filters
            filtered_df = perf_df.copy()
            if filter_group != "All":
                filtered_df = filtered_df[filtered_df['group'] == ('1' if filter_group == "Group 1" else '2')]
            if filter_type != "All":
                filtered_df = filtered_df[filtered_df['assessment_type'] == ('pre' if filter_type == "Pre-Assessment" else 'final')]
            
            # Display table
            st.subheader("Student Performance Details")
            display_df = filtered_df[['student_id', 'group', 'assessment_type', 'score_percentage', 'correct_answers', 'difficulty_level', 'timestamp']].copy()
            display_df['group'] = display_df['group'].map({'1': 'Group 1 (Customized)', '2': 'Group 2 (ChatGPT)'})
            display_df['assessment_type'] = display_df['assessment_type'].map({'pre': 'Pre-Assessment', 'final': 'Final Assessment'})
            st.dataframe(display_df, use_container_width=True)
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name=f"student_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No student data available yet.")
    else:
        st.info("No data file found. Students need to complete assessments first.")


def show_admin_comparison():
    """Show detailed comparison between Group 1 and Group 2"""
    st.header("Group Comparison Analysis")
    
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        
        if len(perf_df) > 0:
            # Calculate comparison
            comparison = storage.calculate_comparison()
            
            if comparison:
                # Display winner
                st.success(f"🏆 Winner: **{comparison['winner']}**")
                render_latex_content(comparison['analysis'])
                
                st.divider()
                
                # Metrics comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Group 1 (Customized Tutor)")
                    st.metric("Pre-Assessment Avg", f"{comparison['group1_avg_pre']:.1f}%")
                    st.metric("Final Assessment Avg", f"{comparison['group1_avg_final']:.1f}%")
                    st.metric("Improvement", f"{comparison['improvement_group1']:.1f}%", 
                             delta=f"{comparison['improvement_group1']:.1f}%")
                
                with col2:
                    st.subheader("💬 Group 2 (ChatGPT Interface)")
                    st.metric("Pre-Assessment Avg", f"{comparison['group2_avg_pre']:.1f}%")
                    st.metric("Final Assessment Avg", f"{comparison['group2_avg_final']:.1f}%")
                    st.metric("Improvement", f"{comparison['improvement_group2']:.1f}%",
                             delta=f"{comparison['improvement_group2']:.1f}%")
                
                st.divider()
                
                # Visualization
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Group 1 Pre',
                    x=['Pre-Assessment'],
                    y=[comparison['group1_avg_pre']],
                    marker_color='lightblue'
                ))
                
                fig.add_trace(go.Bar(
                    name='Group 1 Final',
                    x=['Final Assessment'],
                    y=[comparison['group1_avg_final']],
                    marker_color='blue'
                ))
                
                fig.add_trace(go.Bar(
                    name='Group 2 Pre',
                    x=['Pre-Assessment'],
                    y=[comparison['group2_avg_pre']],
                    marker_color='lightcoral'
                ))
                
                fig.add_trace(go.Bar(
                    name='Group 2 Final',
                    x=['Final Assessment'],
                    y=[comparison['group2_avg_final']],
                    marker_color='red'
                ))
                
                fig.update_layout(
                    title='Group Performance Comparison',
                    barmode='group',
                    yaxis_title='Average Score (%)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough data to calculate comparison yet.")
        else:
            st.info("No data available yet.")
    else:
        st.info("No data file found. Students need to complete assessments first.")


def show_admin_manage_questions():
    """Manage assessment questions"""
    st.header("Manage Question Sets")
    
    st.info("View and manage pre-assessment, learning, and final assessment questions.")
    
    question_type = st.selectbox(
        "Select Question Set",
        ["Pre-Assessment Group 1", "Pre-Assessment Group 2", "Learning Questions", "Final Assessment"]
    )
    
    # Load current questions
    with open('data/trigonometry_questions.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    if question_type == "Pre-Assessment Group 1":
        questions = questions_data['pre_assessment_group1']
        key = 'pre_assessment_group1'
    elif question_type == "Pre-Assessment Group 2":
        questions = questions_data['pre_assessment_group2']
        key = 'pre_assessment_group2'
    elif question_type == "Learning Questions":
        questions = questions_data['learning_questions']
        key = 'learning_questions'
    else:
        questions = questions_data['final_assessment']
        key = 'final_assessment'
    
    st.subheader(f"Current {question_type} Questions ({len(questions)} total)")
    
    # Display questions
    for i, q in enumerate(questions):
        text = q.get('question') or q.get('concept', 'N/A')
        preview = text[:50] if len(text) > 50 else text
        with st.expander(f"Question {i+1}: {preview}..."):
            st.json(q)
    
    st.divider()
    
    # Add new question
    st.subheader("➕ Add New Question")
    
    with st.form("add_question_form"):
        if key in ['pre_assessment', 'final_assessment']:
            new_q = st.text_area("Question Text")
            opt1 = st.text_input("Option 1")
            opt2 = st.text_input("Option 2")
            opt3 = st.text_input("Option 3")
            opt4 = st.text_input("Option 4")
            correct = st.selectbox("Correct Answer", [opt1, opt2, opt3, opt4])
            explanation = st.text_area("Explanation")
        else:
            new_q = st.text_area("Question Text")
            concept = st.text_input("Concept Name")
            hint = st.text_area("Hint/Teaching Point")
        
        if st.form_submit_button("Add Question"):
            if key in ['pre_assessment', 'final_assessment']:
                new_question = {
                    "id": len(questions) + 1,
                    "question": new_q,
                    "options": [opt1, opt2, opt3, opt4],
                    "correct_answer": correct,
                    "explanation": explanation
                }
            else:
                new_question = {
                    "id": len(questions) + 1,
                    "question": new_q,
                    "concept": concept,
                    "hint": hint
                }
            
            questions_data[key].append(new_question)
            
            # Save back to file
            with open('data/trigonometry_questions.json', 'w', encoding='utf-8') as f:
                json.dump(questions_data, f, indent=2)
            
            st.success("✅ Question added successfully!")
            st.rerun()


def show_admin_practice_questions():
    """Add practice questions for students"""
    st.header("Practice Questions Management")
    
    st.info("Create practice questions that students from both groups can access during learning.")
    
    target_group = st.selectbox(
        "Target Group",
        ["Both Groups", "Group 1 Only", "Group 2 Only"]
    )
    
    st.subheader("Create Practice Question")
    
    with st.form("practice_question_form"):
        practice_q = st.text_area("Question Text", height=100)
        practice_concept = st.text_input("Concept/Topic")
        practice_difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        practice_hint = st.text_area("Hint for Students", height=80)
        practice_solution = st.text_area("Solution/Explanation", height=150)
        
        if st.form_submit_button("Save Practice Question"):
            # Create practice questions file if doesn't exist
            practice_file = 'data/practice_questions.json'
            
            if os.path.exists(practice_file):
                with open(practice_file, 'r', encoding='utf-8') as f:
                    practice_data = json.load(f)
            else:
                practice_data = []
            
            new_practice = {
                "id": len(practice_data) + 1,
                "question": practice_q,
                "concept": practice_concept,
                "difficulty": practice_difficulty,
                "hint": practice_hint,
                "solution": practice_solution,
                "target_group": target_group,
                "created_at": datetime.now().isoformat()
            }
            
            practice_data.append(new_practice)
            
            with open(practice_file, 'w', encoding='utf-8') as f:
                json.dump(practice_data, f, indent=2)
            
            st.success("✅ Practice question saved successfully!")
            st.rerun()
    
    # Show existing practice questions
    st.divider()
    st.subheader("Existing Practice Questions")
    
    practice_file = 'data/practice_questions.json'
    if os.path.exists(practice_file):
        with open(practice_file, 'r', encoding='utf-8') as f:
            practice_data = json.load(f)
        
        if practice_data:
            for pq in practice_data:
                with st.expander(f"Q{pq['id']}: {pq['concept']} ({pq['difficulty']}) - {pq['target_group']}"):
                    st.markdown(f"**Question:** {pq['question']}")
                    st.markdown(f"**Hint:** {pq['hint']}")
                    st.markdown(f"**Solution:** {pq['solution']}")
        else:
            st.info("No practice questions yet.")
    else:
        st.info("No practice questions file found.")


def show_admin_chat_history():
    """View all student chat interactions"""
    st.header("💬 Student Chat History")
    st.write("Review how students interact with the tutoring system")
    
    # Get all chat histories
    all_chats = storage.get_all_chat_histories()
    
    if not all_chats:
        st.info("No chat history available yet.")
        return
    
    # Student selector
    student_ids = list(all_chats.keys())
    selected_student = st.selectbox("Select Student", student_ids)
    
    if selected_student:
        student_chats = all_chats[selected_student]
        
        # Get student tracking info
        tracking = storage.get_student_tracking(selected_student)
        
        # Display student info
        st.subheader(f"Student: {selected_student}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Group:** {tracking.get('group', 'N/A')}")
        with col2:
            st.info(f"**Days Interacted:** {tracking.get('days_interacted', 0)}")
        with col3:
            st.info(f"**Total Messages:** {len(student_chats)}")
        
        st.divider()
        
        # Display chat messages
        st.subheader("Chat Messages")
        for idx, chat in enumerate(student_chats):
            timestamp = chat.get('timestamp', 'N/A')
            role = chat.get('role', 'unknown')
            message = chat.get('message', '')
            
            if role == 'user':
                with st.chat_message("user"):
                    st.write(f"**[{timestamp}]**")
                    st.write(message)
            else:
                with st.chat_message("assistant"):
                    st.write(f"**[{timestamp}]**")
                    render_latex_content(message)
        
        # Download option
        st.divider()
        import json
        json_data = json.dumps(student_chats, indent=2)
        st.download_button(
            "📥 Download Chat History (JSON)",
            json_data,
            file_name=f"chat_history_{selected_student}.json",
            mime="application/json"
        )


def show_admin_student_management():
    """Manage student access and track progress"""
    st.header("👥 Student Management")
    st.write("Track student progress and manage final test access")
    
    # Get all student tracking data
    all_tracking = storage.get_all_student_tracking()
    
    if not all_tracking:
        st.info("No student data available yet.")
        return
    
    # Create DataFrame for better display
    tracking_list = []
    for student_id, data in all_tracking.items():
        tracking_list.append({
            'Student ID': student_id,
            'Group': f"Group {data.get('group', 'N/A')}",
            'Pre-Test Done': '✅' if data.get('pre_test_completed') else '❌',
            'Days Interacted': data.get('days_interacted', 0),
            'Final Test Enabled': '✅' if data.get('final_test_enabled') else '🔒',
            'Final Test Done': '✅' if data.get('final_test_completed') else '❌',
            'Admin Override': '⚠️' if data.get('admin_override') else '-'
        })
    
    df = pd.DataFrame(tracking_list)
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.subheader("🔧 Manage Student Access")
    
    # Student selector
    student_ids = list(all_tracking.keys())
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_student = st.selectbox("Select Student to Manage", student_ids)
    
    if selected_student:
        student_data = all_tracking[selected_student]
        
        # Display current status
        st.write("**Current Status:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Days Interacted", student_data.get('days_interacted', 0))
        with col2:
            status = "Enabled" if student_data.get('final_test_enabled') else "Locked"
            st.metric("Final Test", status)
        with col3:
            override = "Yes" if student_data.get('admin_override') else "No"
            st.metric("Admin Override", override)
        with col4:
            completed = "Yes" if student_data.get('final_test_completed') else "No"
            st.metric("Test Completed", completed)
        
        st.divider()
        
        # Admin actions
        st.write("**Admin Actions:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔓 Enable Final Test", use_container_width=True):
                if storage.admin_enable_final_test(selected_student, True):
                    st.success(f"✅ Final test enabled for {selected_student}")
                    st.rerun()
                else:
                    st.error("Failed to enable final test")
        
        with col2:
            if st.button("🔒 Disable Final Test", use_container_width=True):
                if storage.admin_enable_final_test(selected_student, False):
                    st.success(f"✅ Final test disabled for {selected_student}")
                    st.rerun()
                else:
                    st.error("Failed to disable final test")
        
        # View interaction dates
        st.divider()
        st.write("**Interaction History:**")
        interaction_dates = student_data.get('interaction_dates', [])
        if interaction_dates:
            for date in interaction_dates:
                st.write(f"- 📅 {date}")
        else:
            st.info("No interactions recorded yet")


def show_admin_reset_data():
    """Admin page to reset all data"""
    st.header("🗑️ Reset All Data")
    st.warning("⚠️ **DANGER ZONE** ⚠️")
    st.write("""
    This action will **permanently delete**:
    - All student chat history
    - All student tracking data
    - All performance ratings and assessment results
    
    **This cannot be undone!**
    """)
    
    st.divider()
    
    # Get current data count
    all_tracking = storage.get_all_student_tracking()
    student_count = len(all_tracking)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Students", student_count)
    with col2:
        chat_count = 0
        all_chats = storage.get_all_chat_histories()
        for student_chats in all_chats.values():
            chat_count += len(student_chats)
        st.metric("💬 Total Messages", chat_count)
    with col3:
        if os.path.exists('data/performance_ratings.csv'):
            import pandas as pd
            perf_df = pd.read_csv('data/performance_ratings.csv')
            st.metric("📝 Assessment Records", len(perf_df))
        else:
            st.metric("📝 Assessment Records", 0)
    
    st.divider()
    
    # Confirmation step
    st.subheader("⚠️ Confirmation Required")
    st.write("To proceed with data reset, please type: **RESET ALL DATA**")
    
    confirmation = st.text_input("Type confirmation text:", key="reset_confirmation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ RESET ALL DATA", type="primary", use_container_width=True, disabled=(confirmation != "RESET ALL DATA")):
            if confirmation == "RESET ALL DATA":
                with st.spinner("Deleting all data..."):
                    if storage.reset_all_data():
                        st.success("✅ All data has been successfully deleted!")
                        st.balloons()
                        st.info("The system is now clean and ready for new students.")
                        # Clear the confirmation field by rerunning
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Error occurred while resetting data. Please check logs.")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.info("Reset operation cancelled.")


# ============================================================================
# PAGE: Home / Group Selection
# ============================================================================
def show_home():
    """Home page with group selection"""
    
    # Admin access button in sidebar
    with st.sidebar:
        st.write("---")
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.current_page = 'admin_login'
            st.rerun()
    
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.title("📐 Trigonometry Learning Platform")
        st.subheader("Research Study: Comparing Teaching Methods")
        st.write("""
        Welcome! This platform helps us understand which teaching method works better:
        - **Group 1**: Customized AI Tutor with web search
        - **Group 2**: Simple ChatGPT-like interface
        """)
    
    st.divider()
    
    # Group selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨‍🎓 Group 1: Customized Tutor")
        st.info("""
        **Learning with AI Tutor**
        - Personalized teaching based on your level
        - Searches internet for best resources
        - Adapts to your weak areas
        - Step-by-step guidance
        """)
        if st.button("Join Group 1", key="btn_group1", use_container_width=True):
            st.session_state.group = '1'
            st.session_state.current_page = 'register'
            st.rerun()
    
    with col2:
        st.markdown("### 💬 Group 2: ChatGPT Interface")
        st.info("""
        **Learning with ChatGPT**
        - Ask questions freely
        - Get direct answers
        - Simple Q&A interface
        - Self-guided learning
        """)
        if st.button("Join Group 2", key="btn_group2", use_container_width=True):
            st.session_state.group = '2'
            st.session_state.current_page = 'register'
            st.rerun()
    
    st.divider()
    st.markdown("### 📊 Research Purpose")
    st.write("""
    This study compares how different teaching approaches help students learn Trigonometry.
    Your participation helps us improve education!
    """)


# ============================================================================
# PAGE: Student Registration
# ============================================================================
def show_registration():
    """Student registration page"""
    st.title("📋 Student Registration / Login")
    st.write(f"**Group**: {st.session_state.group}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        student_id = st.text_input(
            "Enter your School Student ID",
            placeholder="e.g., STU123456",
            help="Your unique identifier in the school system"
        )
    
    with col2:
        if st.button("Continue", use_container_width=True):
            if student_id.strip():
                st.session_state.student_id = student_id
                
                # Check if student exists and has completed pre-test
                tracking = storage.get_student_tracking(student_id)
                
                if tracking:
                    # Returning student - restore their group from tracking data
                    saved_group = tracking.get('group')
                    if saved_group:
                        st.session_state.group = saved_group
                    
                    if tracking.get('pre_test_completed', False):
                        # Skip pre-test, go directly to learning
                        st.success("✅ Welcome back! Continuing to tutoring session...")
                        st.session_state.pre_assessment_done = True
                        
                        # Check if final test is enabled
                        if tracking.get('final_test_enabled', False):
                            st.session_state.learning_done = True
                            st.session_state.current_page = 'final_assessment'
                        else:
                            if st.session_state.group == '1':
                                st.session_state.current_page = 'learning_group1'
                            else:
                                st.session_state.current_page = 'learning_group2'
                        
                        # Record daily interaction
                        storage.record_daily_interaction(student_id)
                        st.rerun()
                    else:
                        # Returning student with incomplete pre-test
                        st.session_state.current_page = 'pre_assessment'
                        st.rerun()
                else:
                    # Brand new student
                    storage.init_student_tracking(student_id, st.session_state.group)
                    st.session_state.current_page = 'pre_assessment'
                    st.rerun()
            else:
                st.error("Please enter a valid Student ID")
    
    st.info("Your Student ID will be used to track your progress throughout the study.")
    
    # Show status if returning student
    if student_id and student_id.strip():
        tracking = storage.get_student_tracking(student_id.strip())
        if tracking:
            st.divider()
            st.write("**Your Progress:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                if tracking.get('pre_test_completed'):
                    st.success("✅ Pre-test completed")
                else:
                    st.info("⏳ Pre-test pending")
            with col2:
                days = tracking.get('days_interacted', 0)
                st.info(f"📅 {days}/3 days interacted")
            with col3:
                if tracking.get('final_test_enabled'):
                    st.success("✅ Final test available")
                else:
                    st.warning("🔒 Final test locked")


# ============================================================================
# PAGE: Pre Assessment
# ============================================================================
def show_pre_assessment():
    """Pre-assessment quiz"""
    st.title("📝 Pre-Assessment Quiz")
    
    # Load questions based on group
    if st.session_state.group == '1':
        pre_questions = questions_data['pre_assessment_group1']
        st.write("Answer these 5 questions to assess your trigonometry knowledge. Show your work and provide numerical answers.")
    else:
        pre_questions = questions_data['pre_assessment_group2']
        st.write("Answer these 5 questions to assess your trigonometry knowledge. Show your work and provide numerical answers.")
    
    with st.form("pre_assessment_form"):
        answers = []
        
        for i, question in enumerate(pre_questions):
            st.subheader(f"Question {i+1}")
            render_latex_content(question['question'])
            
            # Both groups now use text input for complex problems
            answer = st.text_area(
                f"Your answer (include calculations):",
                key=f"pre_q{question['id']}",
                height=100,
                placeholder="Enter your answer and show your work..."
            )
            
            answers.append({
                'question_id': question['id'],
                'student_answer': answer
            })
        
        submitted = st.form_submit_button("Submit Pre-Assessment", use_container_width=True)
        
        if submitted:
            # Save assessment
            answer_list = [a['student_answer'] for a in answers]
            storage.save_assessment(
                st.session_state.student_id,
                st.session_state.group,
                'pre',
                answer_list
            )
            
            # Analyze with agent
            analyzer = get_assessment_analyzer()
            analysis = analyzer.analyze_assessment(
                st.session_state.student_id,
                answers,
                pre_questions
            )
            
            if analysis['success']:
                # Save analysis
                storage.save_performance_rating(
                    st.session_state.student_id,
                    st.session_state.group,
                    'pre',
                    analysis['analysis']
                )
                
                # Update student tracking - mark pre-test as completed
                storage.update_pre_test_completion(st.session_state.student_id)
                
                # Record first interaction
                storage.record_daily_interaction(st.session_state.student_id)
                
                # Store in session
                st.session_state.pre_assessment_analysis = analysis['analysis']
                st.session_state.pre_assessment_done = True
                st.session_state.current_page = 'learning'
                
                # Show confirmation without revealing score for Group 1
                if st.session_state.group == '1':
                    st.success("✅ Pre-assessment submitted! Proceeding to learning phase...")
                else:
                    st.success(f"✅ Pre-assessment complete! Score: {analysis['analysis'].get('score_percentage', 0):.1f}%")
                
                st.rerun()
            else:
                st.error(f"Error analyzing assessment: {analysis.get('error')}")


# ============================================================================
# PAGE: Learning Phase
# ============================================================================
def show_learning():
    """Learning phase for Group 1 or Group 2"""
    st.title("📚 Learning Phase")
    
    if st.session_state.group == '1':
        show_group1_learning()
    else:
        show_group2_learning()


def show_group1_learning():
    """Customized Tutor for Group 1 - Interactive Chat Interface"""
    st.header("👨‍🏫 Learn with Customized AI Tutor")
    st.write("The AI tutor will guide you through concepts using Socratic questioning. Respond to each question to continue learning!")
    
    # Get pre-assessment analysis (scores hidden for Group 1)
    analysis = st.session_state.get('pre_assessment_analysis', {})
    
    # Do not show scores for Group 1 to maintain study integrity
    st.info("Your pre-assessment has been analyzed. The AI tutor will adapt to your needs.")
    
    # Initialize tutor in session state
    if 'tutor' not in st.session_state:
        st.session_state.tutor = get_customized_tutor()
    
    # Load chat history from storage for returning students
    if 'chat_history_loaded' not in st.session_state:
        stored_chats = storage.get_chat_history(st.session_state.student_id)
        if stored_chats:
            st.session_state.stored_chat_history = stored_chats
        else:
            st.session_state.stored_chat_history = []
        st.session_state.chat_history_loaded = True
    
    # Display previous chat history if exists
    if st.session_state.get('stored_chat_history', []):
        with st.expander("📝 Your Previous Chat History", expanded=True):
            st.write("Here are your previous interactions with the AI tutor:")
            for chat in st.session_state.stored_chat_history:
                role = chat.get('role', 'user')
                message = chat.get('message', '')
                timestamp = chat.get('timestamp', '').split('T')[0] if 'T' in chat.get('timestamp', '') else ''
                
                with st.chat_message(role):
                    if timestamp:
                        st.caption(f"📅 {timestamp}")
                    render_latex_content(message)
            st.divider()
    
    # Initialize concept chat history for new messages
    if 'concept_chats' not in st.session_state:
        st.session_state.concept_chats = {}
    
    # Learning concepts - each with its own chat
    for question in learning_questions:
        concept_id = question['id']
        concept_key = f"chat_{concept_id}"
        
        with st.expander(f"📖 {question['concept']} - {question['question']}", expanded=False):
            # Initialize chat history for this concept
            if concept_key not in st.session_state.concept_chats:
                st.session_state.concept_chats[concept_key] = []
            
            # Start learning button
            if len(st.session_state.concept_chats[concept_key]) == 0:
                if st.button(f"Start Learning: {question['concept']}", key=f"start_{concept_id}"):
                    with st.spinner("AI Tutor is preparing to guide you..."):
                        explanation = st.session_state.tutor.teach_concept(
                            question['id'],
                            question,
                            student_level="intermediate"
                        )
                        
                        if explanation['success']:
                            st.session_state.concept_chats[concept_key].append({
                                'role': 'assistant',
                                'content': explanation['explanation']
                            })
                            
                            # Save learning progress
                            storage.save_learning_progress(
                                st.session_state.student_id,
                                {
                                    'question_id': question['id'],
                                    'concept': question['concept'],
                                    'accessed_at': datetime.now().isoformat()
                                }
                            )
                            st.rerun()
            
            # Display chat history for this concept
            for msg in st.session_state.concept_chats[concept_key]:
                with st.chat_message(msg['role']):
                    render_latex_content(msg['content'])
            
            # Chat input for this concept
            if len(st.session_state.concept_chats[concept_key]) > 0:
                user_response = st.chat_input(
                    f"Your response about {question['concept']}...",
                    key=f"input_{concept_id}"
                )
                
                if user_response:
                    # Add user message to chat
                    st.session_state.concept_chats[concept_key].append({
                        'role': 'user',
                        'content': user_response
                    })
                    
                    # Save user message to database
                    storage.save_chat_message(
                        st.session_state.student_id,
                        st.session_state.group,
                        'user',
                        user_response
                    )
                    
                    # Record daily interaction
                    storage.record_daily_interaction(st.session_state.student_id)
                    
                    # Get tutor's response
                    with st.spinner("AI Tutor is analyzing your response..."):
                        response = st.session_state.tutor.answer_student_question(
                            user_response,
                            student_previous_response=user_response
                        )
                        
                        if response['success']:
                            st.session_state.concept_chats[concept_key].append({
                                'role': 'assistant',
                                'content': response['answer']
                            })
                            
                            # Save assistant message to database
                            storage.save_chat_message(
                                st.session_state.student_id,
                                st.session_state.group,
                                'assistant',
                                response['answer']
                            )
                            
                            # Save interaction
                            storage.save_learning_progress(
                                st.session_state.student_id,
                                {
                                    'question_id': question['id'],
                                    'concept': question['concept'],
                                    'student_response': user_response,
                                    'tutor_response': response['answer'],
                                    'timestamp': datetime.now().isoformat()
                                }
                            )
                    
                    st.rerun()
    
    st.divider()
    
    # Check if final test is enabled
    tracking = storage.get_student_tracking(st.session_state.student_id)
    final_test_enabled = tracking.get('final_test_enabled', False) if tracking else False
    days_interacted = tracking.get('days_interacted', 0) if tracking else 0
    
    if final_test_enabled:
        if st.button("Finish Learning & Go to Final Assessment", use_container_width=True):
            st.session_state.learning_done = True
            st.session_state.current_page = 'final_assessment'
            st.rerun()
    else:
        st.info(f"📅 You have interacted for {days_interacted}/3 days. Complete 3 days to unlock the final assessment!")
        st.button("Final Assessment (Locked)", use_container_width=True, disabled=True)


def show_group2_learning():
    """ChatGPT-like interface for Group 2"""
    st.header("💬 Learn with ChatGPT Interface")
    st.write("Ask any questions about the learning topics. The AI will help you understand.")
    
    agent = get_chatgpt_agent()
    
    # Chat interface
    st.subheader("Learning Questions to Explore")
    st.write("Here are some topics you can ask about:")
    
    topics = [q['concept'] for q in learning_questions]
    st.write(", ".join(topics))
    
    st.write("---")
    st.subheader("💬 Chat with AI Assistant")
    
    # Load chat history from storage for returning students
    if 'chat_history' not in st.session_state:
        stored_chats = storage.get_chat_history(st.session_state.student_id)
        if stored_chats:
            # Convert stored format to session state format
            st.session_state.chat_history = [
                {
                    'role': chat.get('role', 'user'),
                    'content': chat.get('message', '')
                }
                for chat in stored_chats
            ]
        else:
            st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            render_latex_content(msg['content'])
    
    # Chat input
    user_input = st.chat_input("Ask a question about trigonometry...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Save user message to database
        storage.save_chat_message(
            st.session_state.student_id,
            st.session_state.group,
            'user',
            user_input
        )
        
        # Record daily interaction
        storage.record_daily_interaction(st.session_state.student_id)
        
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            response = agent.ask_question(user_input)
            
            if response['success']:
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response['answer']
                })
                
                # Save assistant message to database
                storage.save_chat_message(
                    st.session_state.student_id,
                    st.session_state.group,
                    'assistant',
                    response['answer']
                )
                
                # Save learning progress
                storage.save_learning_progress(
                    st.session_state.student_id,
                    {
                        'question': user_input,
                        'answered_at': datetime.now().isoformat()
                    }
                )
                
                with st.chat_message("assistant"):
                    render_latex_content(response['answer'])
        
        st.rerun()
    
    st.divider()
    
    # Check if final test is enabled
    tracking = storage.get_student_tracking(st.session_state.student_id)
    final_test_enabled = tracking.get('final_test_enabled', False) if tracking else False
    days_interacted = tracking.get('days_interacted', 0) if tracking else 0
    
    if final_test_enabled:
        if st.button("Finish Learning & Go to Final Assessment", use_container_width=True):
            st.session_state.learning_done = True
            st.session_state.current_page = 'final_assessment'
            st.rerun()
    else:
        st.info(f"📅 You have interacted for {days_interacted}/3 days. Complete 3 days to unlock the final assessment!")
        st.button("Final Assessment (Locked)", use_container_width=True, disabled=True)


# ============================================================================
# PAGE: Final Assessment
# ============================================================================
def show_final_assessment():
    """Final assessment quiz"""
    st.title("🎯 Final Assessment Quiz")
    st.write("Answer these 5 final questions. Good luck!")
    
    with st.form("final_assessment_form"):
        answers = []
        
        for i, question in enumerate(final_questions):
            st.subheader(f"Question {i+1}")
            render_latex_content(question['question'])
            
            answer = st.radio(
                "Select your answer:",
                options=question['options'],
                key=f"final_q{question['id']}"
            )
            answers.append({
                'question_id': question['id'],
                'student_answer': answer
            })
        
        submitted = st.form_submit_button("Submit Final Assessment", use_container_width=True)
        
        if submitted:
            # Save assessment
            answer_list = [a['student_answer'] for a in answers]
            storage.save_assessment(
                st.session_state.student_id,
                st.session_state.group,
                'final',
                answer_list
            )
            
            # Analyze with agent
            analyzer = get_assessment_analyzer()
            analysis = analyzer.analyze_assessment(
                st.session_state.student_id,
                answers,
                final_questions
            )
            
            if analysis['success']:
                # Save analysis
                storage.save_performance_rating(
                    st.session_state.student_id,
                    st.session_state.group,
                    'final',
                    analysis['analysis']
                )
                
                # Update student tracking - mark final test as completed
                storage.update_final_test_completion(st.session_state.student_id)
                
                # Store in session
                st.session_state.final_assessment_analysis = analysis['analysis']
                st.session_state.final_assessment_done = True
                st.session_state.current_page = 'results'
                st.rerun()
            else:
                st.error(f"Error analyzing assessment: {analysis.get('error')}")


# ============================================================================
# PAGE: Results
# ============================================================================
def show_results():
    """Results and comparison page"""
    st.title("🏆 Your Learning Results")
    
    pre_analysis = st.session_state.get('pre_assessment_analysis', {})
    final_analysis = st.session_state.get('final_assessment_analysis', {})
    
    # Hide scores for Group 1 to maintain study integrity
    if st.session_state.group != '1':
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Pre-Assessment Score",
                f"{pre_analysis.get('score_percentage', 0):.1f}%"
            )
        
        with col2:
            st.metric(
                "Final Assessment Score",
                f"{final_analysis.get('score_percentage', 0):.1f}%"
            )
        
        with col3:
            improvement = final_analysis.get('score_percentage', 0) - pre_analysis.get('score_percentage', 0)
            st.metric(
                "Improvement",
                f"{improvement:+.1f}%"
            )
    else:
        st.info("Thank you for completing the assessments! Your responses have been recorded for research purposes. Scores are not displayed to maintain study integrity.")
    
    st.divider()
    
    # Show feedback (hidden for Group 1)
    if st.session_state.group != '1':
        st.subheader("📊 Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Pre-Assessment Feedback**")
            with st.container(border=True):
                render_latex_content(pre_analysis.get('detailed_feedback', 'No feedback available'))
        
        with col2:
            st.write("**Final Assessment Feedback**")
            with st.container(border=True):
                render_latex_content(final_analysis.get('detailed_feedback', 'No feedback available'))
        
        st.divider()
    
    st.subheader("📈 Group Comparison")
    
    # Calculate comparison
    comparison = storage.calculate_comparison()
    
    if comparison:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Group 1 (Customized Tutor)**")
            st.metric("Pre-Assessment Avg", f"{comparison.get('group1_avg_pre', 0):.1f}%")
            st.metric("Final Assessment Avg", f"{comparison.get('group1_avg_final', 0):.1f}%")
            st.metric("Improvement", f"{comparison.get('improvement_group1', 0):+.1f}%")
        
        with col2:
            st.write("**Group 2 (ChatGPT)**")
            st.metric("Pre-Assessment Avg", f"{comparison.get('group2_avg_pre', 0):.1f}%")
            st.metric("Final Assessment Avg", f"{comparison.get('group2_avg_final', 0):.1f}%")
            st.metric("Improvement", f"{comparison.get('improvement_group2', 0):+.1f}%")
        
        st.divider()
        st.success(f"**Winner**: {comparison.get('winner', 'TBD')}")
        render_latex_content(comparison.get('analysis', 'Analysis pending'))
    
    st.divider()
    
    if st.button("Start Over", use_container_width=True):
        # Reset session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
# Main App
# ============================================================================
def main():
    """Main app flow"""
    
    # Sidebar
    with st.sidebar:
        st.title("📐 Trigonometry Study")
        
        if st.session_state.student_id:
            st.success(f"Student ID: {st.session_state.student_id}")
            st.info(f"Group: {st.session_state.group}")
        
        st.write("---")
        st.write("**Progress**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Pre: " + ("✅" if st.session_state.pre_assessment_done else "⬜"))
        with col2:
            st.write("Learn: " + ("✅" if st.session_state.learning_done else "⬜"))
        with col3:
            st.write("Final: " + ("✅" if st.session_state.final_assessment_done else "⬜"))
    
    # Main content
    if st.session_state.current_page == 'home':
        show_home()
    elif st.session_state.current_page == 'admin_login':
        show_admin_login()
    elif st.session_state.current_page == 'admin_dashboard':
        if st.session_state.is_admin:
            show_admin_dashboard()
        else:
            st.error("Unauthorized access. Please login first.")
            st.session_state.current_page = 'admin_login'
            st.rerun()
    elif st.session_state.current_page == 'register':
        show_registration()
    elif st.session_state.current_page == 'pre_assessment':
        show_pre_assessment()
    elif st.session_state.current_page == 'learning':
        show_learning()
    elif st.session_state.current_page == 'final_assessment':
        show_final_assessment()
    elif st.session_state.current_page == 'results':
        show_results()


if __name__ == "__main__":
    main()
