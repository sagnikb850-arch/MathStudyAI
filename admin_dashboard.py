"""
Admin Dashboard for viewing study results
Run with: streamlit run admin_dashboard.py
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_storage import DataStorage

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Admin Dashboard - Study Analysis")

storage = DataStorage('data')

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "👥 Student Data",
    "🎯 Group 1 Analysis",
    "💬 Group 2 Analysis",
    "🏆 Comparison"
])

# ============================================================================
# TAB 1: Overview
# ============================================================================
with tab1:
    st.header("Study Overview")
    
    # Load data
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            students = perf_df['student_id'].nunique()
            st.metric("Total Students", students)
        
        with col2:
            group1 = len(perf_df[perf_df['group'] == '1'])
            st.metric("Group 1 Responses", group1)
        
        with col3:
            group2 = len(perf_df[perf_df['group'] == '2'])
            st.metric("Group 2 Responses", group2)
        
        with col4:
            avg_score = perf_df['score_percentage'].mean()
            st.metric("Overall Avg Score", f"{avg_score:.1f}%")
        
        st.divider()
        
        # Score distribution
        st.subheader("Score Distribution")
        
        fig = px.histogram(
            perf_df,
            x='score_percentage',
            nbins=20,
            title='Score Distribution',
            labels={'score_percentage': 'Score (%)', 'count': 'Number of Students'},
            color='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet. Students need to complete assessments.")


# ============================================================================
# TAB 2: Student Data
# ============================================================================
with tab2:
    st.header("Student Performance Data")
    
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            selected_group = st.selectbox("Select Group", ['All', '1', '2'])
        
        with col2:
            selected_type = st.selectbox("Assessment Type", ['All', 'pre', 'final'])
        
        # Filter data
        filtered_df = perf_df.copy()
        if selected_group != 'All':
            filtered_df = filtered_df[filtered_df['group'] == selected_group]
        if selected_type != 'All':
            filtered_df = filtered_df[filtered_df['assessment_type'] == selected_type]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="student_data.csv"
        )
    else:
        st.info("No student data available yet.")


# ============================================================================
# TAB 3: Group 1 Detailed Analysis
# ============================================================================
with tab3:
    st.header("Group 1: Customized Tutor Analysis")
    
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        g1_data = perf_df[perf_df['group'] == '1']
        
        if len(g1_data) > 0:
            # Pre vs Final scores
            pre_scores = g1_data[g1_data['assessment_type'] == 'pre']['score_percentage']
            final_scores = g1_data[g1_data['assessment_type'] == 'final']['score_percentage']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Pre-Assessment Avg",
                    f"{pre_scores.mean():.1f}%",
                    f"({len(pre_scores)} students)"
                )
            
            with col2:
                st.metric(
                    "Final Assessment Avg",
                    f"{final_scores.mean():.1f}%",
                    f"({len(final_scores)} students)"
                )
            
            with col3:
                improvement = final_scores.mean() - pre_scores.mean()
                st.metric(
                    "Improvement",
                    f"{improvement:+.1f}%"
                )
            
            st.divider()
            
            # Score comparison chart
            st.subheader("Pre vs Final Scores")
            
            comparison_data = {
                'Assessment': ['Pre-Assessment', 'Final Assessment'],
                'Average Score': [pre_scores.mean(), final_scores.mean()]
            }
            
            fig = px.bar(
                comparison_data,
                x='Assessment',
                y='Average Score',
                title='Group 1: Pre vs Final Scores',
                color='Assessment'
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
            
            # Difficulty breakdown
            st.subheader("Difficulty Levels")
            difficulty_dist = g1_data['difficulty_level'].value_counts()
            fig = px.pie(
                values=difficulty_dist.values,
                names=difficulty_dist.index,
                title='Distribution of Difficulty Levels'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("No Group 1 data yet.")
    else:
        st.info("No data available.")


# ============================================================================
# TAB 4: Group 2 Detailed Analysis
# ============================================================================
with tab4:
    st.header("Group 2: ChatGPT Interface Analysis")
    
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        g2_data = perf_df[perf_df['group'] == '2']
        
        if len(g2_data) > 0:
            # Pre vs Final scores
            pre_scores = g2_data[g2_data['assessment_type'] == 'pre']['score_percentage']
            final_scores = g2_data[g2_data['assessment_type'] == 'final']['score_percentage']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Pre-Assessment Avg",
                    f"{pre_scores.mean():.1f}%",
                    f"({len(pre_scores)} students)"
                )
            
            with col2:
                st.metric(
                    "Final Assessment Avg",
                    f"{final_scores.mean():.1f}%",
                    f"({len(final_scores)} students)"
                )
            
            with col3:
                improvement = final_scores.mean() - pre_scores.mean()
                st.metric(
                    "Improvement",
                    f"{improvement:+.1f}%"
                )
            
            st.divider()
            
            # Score comparison chart
            st.subheader("Pre vs Final Scores")
            
            comparison_data = {
                'Assessment': ['Pre-Assessment', 'Final Assessment'],
                'Average Score': [pre_scores.mean(), final_scores.mean()]
            }
            
            fig = px.bar(
                comparison_data,
                x='Assessment',
                y='Average Score',
                title='Group 2: Pre vs Final Scores',
                color='Assessment'
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
            
            # Difficulty breakdown
            st.subheader("Difficulty Levels")
            difficulty_dist = g2_data['difficulty_level'].value_counts()
            fig = px.pie(
                values=difficulty_dist.values,
                names=difficulty_dist.index,
                title='Distribution of Difficulty Levels'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("No Group 2 data yet.")
    else:
        st.info("No data available.")


# ============================================================================
# TAB 5: Group Comparison
# ============================================================================
with tab5:
    st.header("🏆 Group 1 vs Group 2 Comparison")
    
    if os.path.exists('data/performance_ratings.csv'):
        perf_df = pd.read_csv('data/performance_ratings.csv')
        
        # Get averages
        g1_pre = perf_df[(perf_df['group'] == '1') & (perf_df['assessment_type'] == 'pre')]['score_percentage'].mean()
        g1_final = perf_df[(perf_df['group'] == '1') & (perf_df['assessment_type'] == 'final')]['score_percentage'].mean()
        
        g2_pre = perf_df[(perf_df['group'] == '2') & (perf_df['assessment_type'] == 'pre')]['score_percentage'].mean()
        g2_final = perf_df[(perf_df['group'] == '2') & (perf_df['assessment_type'] == 'final')]['score_percentage'].mean()
        
        g1_improvement = g1_final - g1_pre
        g2_improvement = g2_final - g2_pre
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Group 1 Pre Avg", f"{g1_pre:.1f}%")
        with col2:
            st.metric("Group 1 Final Avg", f"{g1_final:.1f}%")
        with col3:
            st.metric("Group 2 Pre Avg", f"{g2_pre:.1f}%")
        with col4:
            st.metric("Group 2 Final Avg", f"{g2_final:.1f}%")
        
        st.divider()
        
        # Improvement comparison
        col1, col2 = st.columns(2)
        
        with col1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Group 1 Improvement", f"{g1_improvement:+.1f}%")
            with col_b:
                st.metric("Group 2 Improvement", f"{g2_improvement:+.1f}%")
        
        with col2:
            # Winner
            if g1_improvement > g2_improvement:
                st.success(f"🏆 **Group 1 Wins** - {g1_improvement:.1f}% vs {g2_improvement:.1f}%")
            elif g2_improvement > g1_improvement:
                st.success(f"🏆 **Group 2 Wins** - {g2_improvement:.1f}% vs {g1_improvement:.1f}%")
            else:
                st.info("📊 **Tie** - Same improvement!")
        
        st.divider()
        
        # Comparison chart
        st.subheader("Performance Comparison")
        
        comparison_df = pd.DataFrame({
            'Group': ['Group 1\n(Customized Tutor)', 'Group 1\n(Customized Tutor)', 
                     'Group 2\n(ChatGPT)', 'Group 2\n(ChatGPT)'],
            'Assessment': ['Pre', 'Final', 'Pre', 'Final'],
            'Score': [g1_pre, g1_final, g2_pre, g2_final]
        })
        
        fig = px.bar(
            comparison_df,
            x='Group',
            y='Score',
            color='Assessment',
            title='Scores by Group and Assessment',
            barmode='group'
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis
        st.subheader("📊 Analysis")
        
        st.write(f"""
        ### Key Findings:
        
        **Group 1 (Customized Tutor with Web Search):**
        - Pre-Assessment Average: {g1_pre:.1f}%
        - Final Assessment Average: {g1_final:.1f}%
        - Improvement: {g1_improvement:+.1f}%
        
        **Group 2 (ChatGPT-like Interface):**
        - Pre-Assessment Average: {g2_pre:.1f}%
        - Final Assessment Average: {g2_final:.1f}%
        - Improvement: {g2_improvement:+.1f}%
        
        ### Conclusion:
        Group {"1" if g1_improvement > g2_improvement else "2" if g2_improvement > g1_improvement else "1 and 2 (Tie)"} showed better learning improvement
        for Trigonometry education.
        """)
    
    else:
        st.info("No comparison data yet. Need at least 1 student from each group to complete assessments.")

st.divider()
st.markdown("---")
st.markdown("*Last updated and auto-refreshing* | Data stored in `data/` folder")
