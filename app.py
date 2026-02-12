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

# Initialize agents (lazy load)
@st.cache_resource
def get_assessment_analyzer():
    return AssessmentAnalyzerAgent()

@st.cache_resource(ttl=3600)  # Cache for 1 hour, then refresh
def get_customized_tutor(_version="v2.0"):
    """
    Get customized tutor agent. Increment _version to force cache refresh.
    Current version: v2.0 - Added answer_additional_question method
    """
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
        "💬 Full Chat History (with OBSERVATION)",
        "📋 Pre-Assessment Results",
        "📅 Student Interaction Tracking"
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
        show_admin_full_chat_history()
    
    with tab6:
        show_admin_preassessment_results()
    
    with tab7:
        show_admin_interaction_tracking()


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
                st.markdown(comparison['analysis'])
                
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
        ["Pre-Assessment", "Learning Questions", "Final Assessment"]
    )
    
    # Load current questions
    with open('data/trigonometry_questions.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    if question_type == "Pre-Assessment":
        # Pre-assessment has questions for both groups
        questions_group1 = questions_data.get('pre_assessment_group1', [])
        questions_group2 = questions_data.get('pre_assessment_group2', [])
        questions = questions_group1 + questions_group2
        key = 'pre_assessment'
    elif question_type == "Learning Questions":
        questions = questions_data.get('learning_questions', [])
        key = 'learning_questions'
    else:
        # Final assessment has questions for both groups
        final_group1 = questions_data.get('final_assessment_group1', [])
        final_group2 = questions_data.get('final_assessment_group2', [])
        questions = final_group1 + final_group2
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


def show_admin_full_chat_history():
    """Admin view of full chat responses including OBSERVATION sections"""
    st.header("💬 Full Chat History (with OBSERVATION)")
    st.info("This view shows student chat interactions from both groups with complete AI responses including OBSERVATION sections.")
    
    # Load chat history data
    if os.path.exists('data/chat_history.json'):
        with open('data/chat_history.json', 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        
        if chat_data:
            # Get list of students
            students = list(chat_data.keys())
            selected_student = st.selectbox("Select Student ID", students)
            
            if selected_student:
                st.subheader(f"Chat History for: {selected_student}")
                
                student_messages = chat_data[selected_student]
                
                if student_messages:
                    # Group messages by timestamp/session for better display
                    st.write(f"**Total Messages:** {len(student_messages)}")
                    
                    # Display each message
                    for idx, message in enumerate(student_messages):
                        timestamp = message.get('timestamp', 'Unknown time')
                        group = message.get('group', 'Unknown group')
                        role = message.get('role', 'unknown')
                        content = message.get('message', 'No content')
                        
                        with st.expander(f"Message {idx + 1} - {role.title()} - {group} - {timestamp}"):
                            st.markdown(f"**Group:** {group}")
                            st.markdown(f"**Role:** {role.title()}")
                            st.markdown(f"**Timestamp:** {timestamp}")
                            
                            st.divider()
                            
                            if role == 'user':
                                st.markdown("### 👤 Student Message:")
                                st.info(content)
                            else:
                                st.markdown("### 🤖 AI Response:")
                                if group == 'Group 1':
                                    st.success(f"**AI Tutor Response:** {content}")
                                    # Note: For Group 1, this is the filtered response (no OBSERVATION)
                                    st.caption("📝 Note: This is the filtered response shown to student (OBSERVATION sections removed)")
                                else:
                                    st.success(f"**ChatGPT Response:** {content}")
                    
                    # Also load learning progress for Group 1 OBSERVATION data
                    if os.path.exists('data/learning_progress.json'):
                        with open('data/learning_progress.json', 'r', encoding='utf-8') as f:
                            progress_data = json.load(f)
                        
                        if selected_student in progress_data:
                            st.divider()
                            st.subheader("🔍 Group 1 Full Responses (with OBSERVATION)")
                            st.info("These are the complete AI Tutor responses including OBSERVATION sections that students don't see.")
                            
                            student_progress = progress_data[selected_student]
                            for idx, interaction in enumerate(student_progress):
                                if 'tutor_response_full' in interaction:
                                    with st.expander(f"Full Response {idx + 1} - {interaction.get('concept', 'N/A')} - {interaction.get('timestamp', 'N/A')}"):
                                        st.markdown("### 🔍 Admin View (Full Response with OBSERVATION):")
                                        st.warning(interaction['tutor_response_full'])
                                        
                                        # Highlight if OBSERVATION is present
                                        if 'OBSERVATION' in interaction['tutor_response_full'].upper():
                                            st.caption("✅ Contains OBSERVATION section (hidden from student)")
                                        else:
                                            st.caption("ℹ️ No OBSERVATION section in this response")
                else:
                    st.info("No chat messages recorded for this student yet.")
        else:
            st.info("No student chat history available yet.")
    else:
        st.info("No chat history data found. Students need to start chatting first.")


def show_admin_preassessment_results():
    """Display pre-assessment results for each participant"""
    st.header("📋 Pre-Assessment Results")
    st.info("View detailed pre-assessment answers from all participants")
    
    # Check if assessments.csv exists
    if os.path.exists('data/assessments.csv'):
        assessments_df = pd.read_csv('data/assessments.csv')
        
        # Filter for pre-assessments only
        pre_assessments = assessments_df[assessments_df['assessment_type'] == 'pre'].copy()
        
        if len(pre_assessments) > 0:
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                filter_group = st.selectbox(
                    "Filter by Group",
                    ["All", "Group 1", "Group 2"],
                    key="pre_assess_group_filter"
                )
            
            with col2:
                # Get unique students
                students = pre_assessments['student_id'].unique().tolist()
                filter_student = st.selectbox(
                    "Filter by Student",
                    ["All"] + students,
                    key="pre_assess_student_filter"
                )
            
            # Apply filters
            filtered_df = pre_assessments.copy()
            if filter_group != "All":
                group_num = '1' if filter_group == "Group 1" else '2'
                filtered_df = filtered_df[filtered_df['group'] == group_num]
            if filter_student != "All":
                filtered_df = filtered_df[filtered_df['student_id'] == filter_student]
            
            st.divider()
            
            # Display results for each participant
            st.subheader(f"Pre-Assessment Answers ({len(filtered_df)} participants)")
            
            for idx, row in filtered_df.iterrows():
                student_id = row['student_id']
                group = f"Group {row['group']}"
                timestamp = row['timestamp']
                
                with st.expander(f"👤 {student_id} - {group} - {timestamp}"):
                    # Create columns for better display
                    st.markdown(f"**Student ID:** {student_id}")
                    st.markdown(f"**Group:** {group}")
                    st.markdown(f"**Submitted:** {timestamp}")
                    
                    st.divider()
                    
                    # Display each question and answer
                    for q_num in range(1, 6):
                        q_col = f'q{q_num}_answer'
                        if q_col in row and pd.notna(row[q_col]):
                            st.markdown(f"### Question {q_num}")
                            st.markdown(f"**Answer:** {row[q_col]}")
                            st.write("")
                    
                    # Show performance metrics if available
                    st.divider()
                    st.markdown("**Performance Metrics:**")
                    
                    # Check if performance data exists
                    if os.path.exists('data/performance_ratings.csv'):
                        perf_df = pd.read_csv('data/performance_ratings.csv')
                        student_perf = perf_df[
                            (perf_df['student_id'] == student_id) & 
                            (perf_df['assessment_type'] == 'pre')
                        ]
                        
                        if len(student_perf) > 0:
                            perf_row = student_perf.iloc[0]
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Score", f"{perf_row['score_percentage']:.1f}%")
                            with col2:
                                # Pre-assessment has 5 questions
                                st.metric("Correct Answers", f"{perf_row['correct_answers']}/5")
                            with col3:
                                st.metric("Difficulty", perf_row['difficulty_level'])
                        else:
                            st.info("Performance analysis not available for this student")
                    else:
                        st.info("Performance data not available")
            
            st.divider()
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Pre-Assessment Data as CSV",
                data=csv,
                file_name=f"pre_assessment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No pre-assessment submissions yet.")
    else:
        st.info("No assessment data available. Students need to complete pre-assessments first.")


def show_admin_interaction_tracking():
    """Display student interaction tracking and allow manual final test access"""
    st.header("📅 Student Interaction Tracking")
    st.info("Monitor student engagement and manage final test access")
    
    # Get all student tracking data
    all_tracking = storage.get_all_student_tracking()
    
    if all_tracking:
        # Convert to DataFrame for easier display
        tracking_list = []
        for student_id, data in all_tracking.items():
            tracking_list.append({
                'Student ID': student_id,
                'Group': data.get('group', 'N/A'),
                'Pre-Test': '✅' if data.get('pre_test_completed', False) else '❌',
                'Days Interacted': data.get('days_interacted', 0),
                'Interaction Dates': len(data.get('interaction_dates', [])),
                'Final Test Status': '✅ Enabled' if data.get('final_test_enabled', False) else '🔒 Locked',
                'Final Test Done': '✅' if data.get('final_test_completed', False) else '❌',
                'Admin Override': '✅' if data.get('admin_override', False) else '❌'
            })
        
        df = pd.DataFrame(tracking_list)
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", len(all_tracking))
        with col2:
            completed_pre = sum(1 for d in all_tracking.values() if d.get('pre_test_completed', False))
            st.metric("Pre-Tests Completed", completed_pre)
        with col3:
            eligible_final = sum(1 for d in all_tracking.values() if d.get('final_test_enabled', False))
            st.metric("Final Test Eligible", eligible_final)
        with col4:
            completed_final = sum(1 for d in all_tracking.values() if d.get('final_test_completed', False))
            st.metric("Final Tests Completed", completed_final)
        
        st.divider()
        
        # Display detailed table
        st.subheader("📋 Student Tracking Details")
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        
        # Admin Controls for Final Test Access
        st.subheader("⚙️ Admin Controls: Manually Enable Final Test")
        st.write("Admins can manually enable the final test for students who haven't met the 3-day requirement.")
        
        # Select student to modify
        student_ids = list(all_tracking.keys())
        selected_student = st.selectbox("Select Student ID", student_ids)
        
        if selected_student:
            student_data = all_tracking[selected_student]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Group:** {student_data.get('group', 'N/A')}")
                st.write(f"**Pre-Test Status:** {'Completed' if student_data.get('pre_test_completed', False) else 'Not Completed'}")
                st.write(f"**Days Interacted:** {student_data.get('days_interacted', 0)}/3")
            
            with col2:
                st.write(f"**Final Test Status:** {'Enabled' if student_data.get('final_test_enabled', False) else 'Locked'}")
                st.write(f"**Final Test Completed:** {'Yes' if student_data.get('final_test_completed', False) else 'No'}")
                st.write(f"**Admin Override:** {'Yes' if student_data.get('admin_override', False) else 'No'}")
            
            st.divider()
            
            # Buttons for manual control
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Enable Final Test (Admin Override)", key=f"enable_{selected_student}", use_container_width=True):
                    if storage.admin_enable_final_test(selected_student, enabled=True):
                        st.success(f"Final test enabled for student {selected_student}")
                        st.rerun()
                    else:
                        st.error("Failed to enable final test")
            
            with col2:
                if st.button("🔒 Disable Final Test", key=f"disable_{selected_student}", use_container_width=True):
                    if storage.admin_enable_final_test(selected_student, enabled=False):
                        st.success(f"Final test disabled for student {selected_student}")
                        st.rerun()
                    else:
                        st.error("Failed to disable final test")
            
            # Show detailed interaction history
            st.divider()
            st.subheader(f"📊 Interaction History for {selected_student}")
            interaction_dates = student_data.get('interaction_dates', [])
            if interaction_dates:
                st.write(f"**Total unique days:** {len(interaction_dates)}")
                st.write("**Dates:**")
                for date in interaction_dates:
                    st.write(f"- {date}")
            else:
                st.info("No interactions recorded yet")
    else:
        st.info("No student tracking data available yet. Students need to register first.")



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
    st.title("📋 Student Registration")
    st.write(f"**Group**: {st.session_state.group}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        student_id = st.text_input(
            "Enter your School Student ID",
            placeholder="e.g., STU123456",
            help="Your unique identifier in the school system"
        )
    
    with col2:
        if st.button("Register & Continue", use_container_width=True):
            if student_id.strip():
                st.session_state.student_id = student_id
                
                # Check if returning student
                tracking = storage.get_student_tracking(student_id)
                
                if tracking:
                    # Returning student - restore their group and check pre-test status
                    st.session_state.group = tracking.get('group', st.session_state.group)
                    
                    if tracking.get('pre_test_completed', False):
                        # Skip pre-test, go directly to learning
                        st.info("Welcome back! Continuing your learning session...")
                        st.session_state.pre_assessment_done = True
                        st.session_state.current_page = 'learning'
                    else:
                        # Pre-test not completed yet
                        st.session_state.current_page = 'pre_assessment'
                else:
                    # New student - initialize tracking
                    storage.init_student_tracking(student_id, st.session_state.group)
                    st.session_state.current_page = 'pre_assessment'
                
                st.rerun()
            else:
                st.error("Please enter a valid Student ID")
    
    st.info("Your Student ID will be used to track your progress throughout the study.")


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
            st.markdown(question['question'])
            
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
                
                # Store in session
                st.session_state.pre_assessment_analysis = analysis['analysis']
                st.session_state.pre_assessment_done = True
                
                # Update student tracking - mark pre-test as completed
                storage.update_pre_test_completion(st.session_state.student_id)
                
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
    
    # Initialize concept chat history
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
                                'content': explanation['explanation']  # Filtered response for student
                            })
                            
                            # Save chat message to history
                            storage.save_chat_message(
                                st.session_state.student_id,
                                'Group 1',
                                'assistant',
                                explanation['explanation']
                            )
                            
                            # Save learning progress with FULL response for admin
                            storage.save_learning_progress(
                                st.session_state.student_id,
                                {
                                    'question_id': question['id'],
                                    'concept': question['concept'],
                                    'tutor_response_filtered': explanation['explanation'],  # Student sees this
                                    'tutor_response_full': explanation.get('full_response', explanation['explanation']),  # Admin sees this
                                    'accessed_at': datetime.now().isoformat()
                                }
                            )
                            st.rerun()
            
            # Display chat history for this concept
            for msg in st.session_state.concept_chats[concept_key]:
                with st.chat_message(msg['role']):
                    # Extra safety: Remove any OBSERVATION that might have slipped through
                    content = msg['content']
                    if 'OBSERVATION' in content.upper():
                        # Emergency filter
                        import re
                        # Remove any line containing OBSERVATION
                        lines = [line for line in content.split('\n') if 'observation' not in line.lower()]
                        content = '\n'.join(lines)
                        # Remove OBSERVATION sections
                        content = re.sub(r'(?i)\*\*observation:?\*\*[^\n]*(\n[^\*]*)*', '', content)
                        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content).strip()
                    st.markdown(content)
            
            # Chat input for this concept
            if len(st.session_state.concept_chats[concept_key]) > 0:
                user_response = st.chat_input(
                    f"Your response about {question['concept']}...",
                    key=f"input_{concept_id}"
                )
                
                if user_response:
                    # Record daily interaction for tracking
                    storage.record_daily_interaction(st.session_state.student_id)
                    
                    # Add user message to chat
                    st.session_state.concept_chats[concept_key].append({
                        'role': 'user',
                        'content': user_response
                    })
                    
                    # Save user message to chat history
                    storage.save_chat_message(
                        st.session_state.student_id,
                        'Group 1',
                        'user',
                        user_response
                    )
                    
                    # Get tutor's response
                    with st.spinner("AI Tutor is analyzing your response..."):
                        response = st.session_state.tutor.answer_student_question(
                            user_response,
                            student_previous_response=user_response
                        )
                        
                        if response['success']:
                            st.session_state.concept_chats[concept_key].append({
                                'role': 'assistant',
                                'content': response['answer']  # Filtered response for student
                            })
                            
                            # Save AI response to chat history
                            storage.save_chat_message(
                                st.session_state.student_id,
                                'Group 1',
                                'assistant',
                                response['answer']
                            )
                            
                            # Save interaction with FULL response for admin
                            storage.save_learning_progress(
                                st.session_state.student_id,
                                {
                                    'question_id': question['id'],
                                    'concept': question['concept'],
                                    'student_response': user_response,
                                    'tutor_response_filtered': response['answer'],  # Student sees this
                                    'tutor_response_full': response.get('full_response', response['answer']),  # Admin sees this with OBSERVATION
                                    'timestamp': datetime.now().isoformat()
                                }
                            )
                    
                    st.rerun()
    
    # NEW: Additional Questions Chatbox
    st.subheader("💬 Ask Additional Questions")
    st.write("Got confused about something? Need extra clarification? Ask me anything about trigonometry concepts!")
    
    # Initialize additional chat history
    if 'additional_chat' not in st.session_state:
        st.session_state.additional_chat = []
    
    # Display additional chat history
    if st.session_state.additional_chat:
        st.write("**Previous Questions:**")
        for msg in st.session_state.additional_chat:
            with st.chat_message(msg['role']):
                # Extra safety: Remove any OBSERVATION that might have slipped through
                content = msg['content']
                if 'OBSERVATION' in content.upper():
                    # Emergency filter
                    import re
                    lines = [line for line in content.split('\n') if 'observation' not in line.lower()]
                    content = '\n'.join(lines)
                    content = re.sub(r'(?i)\*\*observation:?\*\*[^\n]*(\n[^\*]*)*', '', content)
                    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content).strip()
                st.markdown(content)
    
    # Additional question input
    additional_question = st.chat_input(
        "Ask any trigonometry question... (e.g., 'Can you explain sin again?' or 'What's the difference between tan and sin?')",
        key="additional_question_input"
    )
    
    if additional_question:
        # Record interaction
        storage.record_daily_interaction(st.session_state.student_id)
        
        # Add user question to additional chat
        st.session_state.additional_chat.append({
            'role': 'user',
            'content': additional_question
        })
        
        # Save to chat history
        storage.save_chat_message(
            st.session_state.student_id,
            'Group 1 - Additional',
            'user',
            additional_question
        )
        
        # Get tutor's response to additional question
        with st.spinner("AI Tutor is thinking about your additional question..."):
            additional_response = st.session_state.tutor.answer_additional_question(
                additional_question,
                context=f"Student is learning: {', '.join([c for c in st.session_state.concept_chats.keys()])}"
            )
            
            if additional_response['success']:
                st.session_state.additional_chat.append({
                    'role': 'assistant',
                    'content': additional_response['answer']
                })
                
                # Save AI response
                storage.save_chat_message(
                    st.session_state.student_id,
                    'Group 1 - Additional',
                    'assistant',
                    additional_response['answer']
                )
                
                # Save interaction with full response for admin
                storage.save_learning_progress(
                    st.session_state.student_id,
                    {
                        'type': 'additional_question',
                        'question': additional_question,
                        'tutor_response_filtered': additional_response['answer'],
                        'tutor_response_full': additional_response.get('full_response', additional_response['answer']),
                        'student_mood': additional_response.get('student_mood', 'neutral'),
                        'timestamp': datetime.now().isoformat()
                    }
                )
            else:
                st.error(f"Sorry, I had trouble with that question: {additional_response.get('error', 'Unknown error')}")
        
        st.rerun()
    
    # Show student progress summary
    if hasattr(st.session_state.tutor, 'get_student_progress_summary'):
        progress = st.session_state.tutor.get_student_progress_summary()
        
        with st.expander("📊 Your Learning Progress", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Concepts Explored", progress['total_concepts_attempted'])
                st.metric("Learning Mood", progress['current_mood'].title())
                
            with col2:
                st.metric("Successes", progress['success_count'])
                st.metric("Hints Given", progress['total_hints_given'])
                
            with col3:
                st.metric("Steps Completed", f"{progress['completed_steps']}/{progress['total_steps']}")
                
                if progress['learning_insights']['is_engaged']:
                    st.success("🌟 You're doing great!")
                elif progress['learning_insights']['needs_encouragement']:
                    st.info("💪 Keep going! You're learning!")
                    
            if progress['concepts_mastered']:
                st.write("**Concepts You've Mastered:**")
                for concept in progress['concepts_mastered']:
                    st.write(f"✅ {concept}")
    
    st.divider()
    
    # Check final test eligibility
    tracking = storage.get_student_tracking(st.session_state.student_id)
    days_interacted = tracking.get('days_interacted', 0)
    final_test_enabled = tracking.get('final_test_enabled', False)
    
    if final_test_enabled:
        if st.button("Finish Learning & Go to Final Assessment", use_container_width=True):
            st.session_state.learning_done = True
            st.session_state.current_page = 'final_assessment'
            st.rerun()
    else:
        st.info(f"📅 **Final Test Requirement:** You need to interact with the learning system for 3 days to unlock the final test.\n\n" + 
                f"**Progress:** {days_interacted} out of 3 days completed.\n\n" +
                f"Come back on different days to continue learning!")
        st.button("Final Assessment (Locked)", disabled=True, use_container_width=True)


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
    
    # Display chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    
    # Chat input
    user_input = st.chat_input("Ask a question about trigonometry...")
    
    if user_input:
        # Record daily interaction for tracking
        storage.record_daily_interaction(st.session_state.student_id)
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Save user message to chat history
        storage.save_chat_message(
            st.session_state.student_id,
            'Group 2',
            'user',
            user_input
        )
        
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
                
                # Save AI response to chat history
                storage.save_chat_message(
                    st.session_state.student_id,
                    'Group 2',
                    'assistant',
                    response['answer']
                )
                
                # Save learning progress WITH RESPONSE for admin review
                storage.save_learning_progress(
                    st.session_state.student_id,
                    {
                        'group': 'Group 2',
                        'student_question': user_input,
                        'ai_response': response['answer'],
                        'timestamp': datetime.now().isoformat()
                    }
                )
                
                with st.chat_message("assistant"):
                    st.markdown(response['answer'])
        
        st.rerun()
    
    st.divider()
    
    # Check final test eligibility
    tracking = storage.get_student_tracking(st.session_state.student_id)
    days_interacted = tracking.get('days_interacted', 0)
    final_test_enabled = tracking.get('final_test_enabled', False)
    
    if final_test_enabled:
        if st.button("Finish Learning & Go to Final Assessment", use_container_width=True):
            st.session_state.learning_done = True
            st.session_state.current_page = 'final_assessment'
            st.rerun()
    else:
        st.info(f"📅 **Final Test Requirement:** You need to interact with the learning system for 3 days to unlock the final test.\n\n" + 
                f"**Progress:** {days_interacted} out of 3 days completed.\n\n" +
                f"Come back on different days to continue learning!")
        st.button("Final Assessment (Locked)", disabled=True, use_container_width=True)


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
            st.markdown(question['question'])
            
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
                
                # Store in session
                st.session_state.final_assessment_analysis = analysis['analysis']
                st.session_state.final_assessment_done = True
                
                # Update student tracking - mark final test as completed
                storage.update_final_test_completion(st.session_state.student_id)
                
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
                st.markdown(pre_analysis.get('detailed_feedback', 'No feedback available'))
        
        with col2:
            st.write("**Final Assessment Feedback**")
            with st.container(border=True):
                st.markdown(final_analysis.get('detailed_feedback', 'No feedback available'))
        
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
        st.info(comparison.get('analysis', 'Analysis pending'))
    
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
