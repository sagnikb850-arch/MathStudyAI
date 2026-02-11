"""
Data Storage Utility - File-based storage without database
Uses CSV, JSON for persistence
"""
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class DataStorage:
    """
    Manages all data storage operations using files
    """
    
    def __init__(self, data_dir: str = "data"):
        """Initialize data storage"""
        self.data_dir = data_dir
        Path(self.data_dir).mkdir(exist_ok=True)
        
        # File paths
        self.assessments_file = os.path.join(data_dir, "assessments.csv")
        self.student_progress_file = os.path.join(data_dir, "student_progress.json")
        self.performance_file = os.path.join(data_dir, "performance_ratings.csv")
        self.learning_history_file = os.path.join(data_dir, "learning_history.json")
        self.comparison_file = os.path.join(data_dir, "comparison_results.csv")
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Create empty files if they don't exist"""
        # CSV files
        for file in [self.assessments_file, self.performance_file, self.comparison_file]:
            if not os.path.exists(file):
                if file == self.assessments_file:
                    df = pd.DataFrame(columns=[
                        'student_id', 'group', 'assessment_type', 'timestamp',
                        'q1_answer', 'q2_answer', 'q3_answer', 'q4_answer', 'q5_answer',
                        'score', 'attempts'
                    ])
                    df.to_csv(file, index=False)
                elif file == self.performance_file:
                    df = pd.DataFrame(columns=[
                        'student_id', 'group', 'assessment_type', 'score_percentage',
                        'correct_answers', 'weak_areas', 'strong_areas', 'difficulty_level',
                        'timestamp'
                    ])
                    df.to_csv(file, index=False)
                elif file == self.comparison_file:
                    df = pd.DataFrame(columns=[
                        'group1_avg_pre', 'group2_avg_pre', 'group1_avg_final', 'group2_avg_final',
                        'improvement_group1', 'improvement_group2', 'winner', 'analysis', 'timestamp'
                    ])
                    df.to_csv(file, index=False)
        
        # JSON files
        for file in [self.student_progress_file, self.learning_history_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)
    
    def save_assessment(self, student_id: str, group: str, assessment_type: str,
                       answers: List[str], score: int = 0) -> bool:
        """Save assessment answers"""
        try:
            df = pd.read_csv(self.assessments_file)
            
            new_row = {
                'student_id': student_id,
                'group': group,
                'assessment_type': assessment_type,
                'timestamp': datetime.now().isoformat(),
                'q1_answer': answers[0] if len(answers) > 0 else '',
                'q2_answer': answers[1] if len(answers) > 1 else '',
                'q3_answer': answers[2] if len(answers) > 2 else '',
                'q4_answer': answers[3] if len(answers) > 3 else '',
                'q5_answer': answers[4] if len(answers) > 4 else '',
                'score': score,
                'attempts': 1
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(self.assessments_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving assessment: {e}")
            return False
    
    def save_performance_rating(self, student_id: str, group: str, assessment_type: str,
                               rating: Dict[str, Any]) -> bool:
        """Save performance analysis from agent"""
        try:
            df = pd.read_csv(self.performance_file)
            
            new_row = {
                'student_id': student_id,
                'group': group,
                'assessment_type': assessment_type,
                'score_percentage': rating.get('score_percentage', 0),
                'correct_answers': rating.get('correct_answers', 0),
                'weak_areas': '|'.join(rating.get('weak_areas', [])),
                'strong_areas': '|'.join(rating.get('strong_areas', [])),
                'difficulty_level': rating.get('difficulty_level', 'Unknown'),
                'timestamp': datetime.now().isoformat()
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(self.performance_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving performance rating: {e}")
            return False
    
    def save_learning_progress(self, student_id: str, progress: Dict[str, Any]) -> bool:
        """Save student learning progress"""
        try:
            with open(self.learning_history_file, 'r') as f:
                data = json.load(f)
            
            if student_id not in data:
                data[student_id] = []
            
            data[student_id].append({
                'timestamp': datetime.now().isoformat(),
                'progress': progress
            })
            
            with open(self.learning_history_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving learning progress: {e}")
            return False
    
    def get_student_assessments(self, student_id: str) -> List[Dict]:
        """Get all assessments for a student"""
        try:
            df = pd.read_csv(self.assessments_file)
            student_data = df[df['student_id'] == student_id].to_dict('records')
            return student_data
        except Exception as e:
            print(f"Error getting assessments: {e}")
            return []
    
    def get_group_performance(self, group: str, assessment_type: str = 'pre') -> List[Dict]:
        """Get performance data for a group"""
        try:
            df = pd.read_csv(self.performance_file)
            filtered = df[(df['group'] == group) & (df['assessment_type'] == assessment_type)]
            return filtered.to_dict('records')
        except Exception as e:
            print(f"Error getting group performance: {e}")
            return []
    
    def calculate_comparison(self) -> Dict[str, Any]:
        """Calculate comparison between groups"""
        try:
            perf_df = pd.read_csv(self.performance_file)
            
            # Get pre-assessment averages
            g1_pre = perf_df[(perf_df['group'] == '1') & (perf_df['assessment_type'] == 'pre')]
            g2_pre = perf_df[(perf_df['group'] == '2') & (perf_df['assessment_type'] == 'pre')]
            
            g1_pre_avg = g1_pre['score_percentage'].mean() if len(g1_pre) > 0 else 0
            g2_pre_avg = g2_pre['score_percentage'].mean() if len(g2_pre) > 0 else 0
            
            # Get final assessment averages
            g1_final = perf_df[(perf_df['group'] == '1') & (perf_df['assessment_type'] == 'final')]
            g2_final = perf_df[(perf_df['group'] == '2') & (perf_df['assessment_type'] == 'final')]
            
            g1_final_avg = g1_final['score_percentage'].mean() if len(g1_final) > 0 else 0
            g2_final_avg = g2_final['score_percentage'].mean() if len(g2_final) > 0 else 0
            
            # Calculate improvement
            g1_improvement = g1_final_avg - g1_pre_avg
            g2_improvement = g2_final_avg - g2_pre_avg
            
            # Determine winner
            if g1_improvement > g2_improvement:
                winner = "Group 1 (Customized Tutor)"
            elif g2_improvement > g1_improvement:
                winner = "Group 2 (ChatGPT Interface)"
            else:
                winner = "Tie"
            
            result = {
                'group1_avg_pre': round(g1_pre_avg, 2),
                'group2_avg_pre': round(g2_pre_avg, 2),
                'group1_avg_final': round(g1_final_avg, 2),
                'group2_avg_final': round(g2_final_avg, 2),
                'improvement_group1': round(g1_improvement, 2),
                'improvement_group2': round(g2_improvement, 2),
                'winner': winner,
                'analysis': f"Group 1 improved by {g1_improvement:.2f}%, Group 2 improved by {g2_improvement:.2f}%",
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to file
            if os.path.exists(self.comparison_file):
                df = pd.read_csv(self.comparison_file)
                df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
            else:
                df = pd.DataFrame([result])
            
            df.to_csv(self.comparison_file, index=False)
            
            return result
        
        except Exception as e:
            print(f"Error calculating comparison: {e}")
            return {}
