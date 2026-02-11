"""
Streamlit App - A/B Testing Platform for Trigonometry Learning
Comparing Customized Tutor (Group 1) vs ChatGPT Interface (Group 2)
"""
import streamlit as st
import json
import os
import sys
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

# Load questions
with open('data/trigonometry_questions.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

pre_questions = questions_data['pre_assessment']
learning_questions = questions_data['learning_questions']
final_questions = questions_data['final_assessment']

# Initialize storage
storage = DataStorage('data')

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
# PAGE: Home / Group Selection
# ============================================================================
def show_home():
    """Home page with group selection"""
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
    st.write("Answer these 5 questions to assess your current trigonometry knowledge.")
    
    with st.form("pre_assessment_form"):
        answers = []
        
        for i, question in enumerate(pre_questions):
            st.subheader(f"Question {i+1}")
            st.write(question['question'])
            
            answer = st.radio(
                "Select your answer:",
                options=question['options'],
                key=f"pre_q{question['id']}"
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
                st.session_state.current_page = 'learning'
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
    """Customized Tutor for Group 1"""
    st.header("👨‍🏫 Learn with Customized AI Tutor")
    st.write("The AI tutor will guide you through these concepts based on your needs.")
    
    # Get pre-assessment analysis
    analysis = st.session_state.get('pre_assessment_analysis', {})
    
    if analysis:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Score", f"{analysis.get('score_percentage', 0):.1f}%")
        with col2:
            st.metric("Difficulty Level", analysis.get('difficulty_level', 'Unknown'))
    
    # Learning questions with tutor
    tutor = get_customized_tutor()
    
    for question in learning_questions:
        with st.expander(f"📖 {question['concept']} - {question['question']}", expanded=False):
            # Get tutor explanation
            if st.button(f"Get Explanation", key=f"explain_{question['id']}"):
                with st.spinner("AI Tutor is preparing explanation..."):
                    explanation = tutor.teach_concept(
                        question['id'],
                        question,
                        student_level="intermediate"
                    )
                    
                    if explanation['success']:
                        st.markdown(explanation['explanation'])
                        
                        # Save learning progress
                        storage.save_learning_progress(
                            st.session_state.student_id,
                            {
                                'question_id': question['id'],
                                'concept': question['concept'],
                                'accessed_at': datetime.now().isoformat()
                            }
                        )
            
            # Student can ask questions
            st.write("---")
            st.write("**Have a Question?**")
            student_q = st.text_input(f"Ask about {question['concept']}", key=f"ask_{question['id']}")
            
            if student_q:
                if st.button(f"Get Answer", key=f"answer_{question['id']}"):
                    with st.spinner("AI Tutor is thinking..."):
                        response = tutor.answer_student_question(student_q)
                        if response['success']:
                            st.markdown(response['answer'])
    
    st.divider()
    
    if st.button("Finish Learning & Go to Final Assessment", use_container_width=True):
        st.session_state.learning_done = True
        st.session_state.current_page = 'final_assessment'
        st.rerun()


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
            st.write(msg['content'])
    
    # Chat input
    user_input = st.chat_input("Ask a question about trigonometry...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
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
                
                # Save learning progress
                storage.save_learning_progress(
                    st.session_state.student_id,
                    {
                        'question': user_input,
                        'answered_at': datetime.now().isoformat()
                    }
                )
                
                with st.chat_message("assistant"):
                    st.write(response['answer'])
        
        st.rerun()
    
    st.divider()
    
    if st.button("Finish Learning & Go to Final Assessment", use_container_width=True):
        st.session_state.learning_done = True
        st.session_state.current_page = 'final_assessment'
        st.rerun()


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
            st.write(question['question'])
            
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
    
    st.divider()
    
    # Show feedback
    st.subheader("📊 Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Pre-Assessment Feedback**")
        st.info(pre_analysis.get('detailed_feedback', 'No feedback available'))
    
    with col2:
        st.write("**Final Assessment Feedback**")
        st.success(final_analysis.get('detailed_feedback', 'No feedback available'))
    
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
