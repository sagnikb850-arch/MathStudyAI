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
        self.chat_history_file = os.path.join(data_dir, "chat_history.json")
        self.student_tracking_file = os.path.join(data_dir, "student_tracking.json")
        
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
        for file in [self.student_progress_file, self.learning_history_file, 
                     self.chat_history_file, self.student_tracking_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)
    
    def save_assessment(self, student_id: str, group: str, assessment_type: str,
                       answers: List[str], score: int = 0) -> bool:
        """Save assessment answers"""
        try:
            timestamp = datetime.now().isoformat()
            
            # Save to JSON (for backward compatibility)
            df = pd.read_csv(self.assessments_file)
            
            new_row = {
                'student_id': student_id,
                'group': group,
                'assessment_type': assessment_type,
                'timestamp': timestamp,
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
                'timestamp': timestamp,
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
    # ==================== NEW FEATURES ====================
    
    def save_chat_message(self, student_id: str, group: str, role: str, message: str, concept: str = None) -> bool:
        """Save a chat message to history (both JSON and CSV)"""
        try:

            timestamp = datetime.now().isoformat()

            

            # Save to JSON (for backward compatibility)
            with open(self.chat_history_file, 'r') as f:
                data = json.load(f)
            
            if student_id not in data:
                data[student_id] = []
            
            data[student_id].append({
                'timestamp': timestamp,
                'group': group,
                'role': role,  # 'user' or 'assistant'
                'message': message
            })
            
            with open(self.chat_history_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            
            # Save to CSV in real-time
            if 'Group 1' in group:
                csv_file = os.path.join(self.data_dir, "group1_chat_history.csv")
                self._append_to_csv(csv_file, {
                    'User ID': student_id,
                    'Date': timestamp,
                    'Concept/Query': concept or 'General Question',
                    'Role': role.title(),
                    'Message': message
                }, group=1)
            elif group == 'Group 2':
                csv_file = os.path.join(self.data_dir, "group2_chat_history.csv")
                self._append_to_csv(csv_file, {
                    'User ID': student_id,
                    'Date': timestamp,
                    'Query': 'Chat Conversation',
                    'Role': role.title(),
                    'Message': message
                }, group=2)
            return True
        except Exception as e:
            print(f"Error saving chat message: {e}")
            return False
    
    def get_chat_history(self, student_id: str) -> List[Dict]:
        """Get chat history for a student"""
        try:

            timestamp = datetime.now().isoformat()

            

            # Save to JSON (for backward compatibility)
            with open(self.chat_history_file, 'r') as f:
                data = json.load(f)
            return data.get(student_id, [])
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def get_all_chat_histories(self) -> Dict[str, List[Dict]]:
        """Get all chat histories (for admin)"""
        try:

            timestamp = datetime.now().isoformat()

            

            # Save to JSON (for backward compatibility)
            with open(self.chat_history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error getting all chat histories: {e}")
            return {}
    
    def init_student_tracking(self, student_id: str, group: str) -> bool:
        """Initialize tracking for a new student"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                data = json.load(f)
            
            if student_id not in data:
                data[student_id] = {
                    'group': group,
                    'pre_test_completed': False,
                    'pre_test_date': None,
                    'interaction_dates': [],  # List of dates student interacted
                    'days_interacted': 0,
                    'final_test_enabled': False,
                    'final_test_completed': False,
                    'final_test_date': None,
                    'admin_override': False,  # Admin can manually enable final test
                    'created_at': datetime.now().isoformat()
                }
                
                with open(self.student_tracking_file, 'w') as f:
                    json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error initializing student tracking: {e}")
            return False
    
    def update_pre_test_completion(self, student_id: str) -> bool:
        """Mark pre-test as completed"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                data = json.load(f)
            
            if student_id in data:
                data[student_id]['pre_test_completed'] = True
                data[student_id]['pre_test_date'] = datetime.now().isoformat()
                
                with open(self.student_tracking_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error updating pre-test completion: {e}")
            return False
    
    def record_daily_interaction(self, student_id: str) -> bool:
        """Record student interaction for today"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                data = json.load(f)
            
            if student_id in data:
                today = datetime.now().date().isoformat()
                
                if today not in data[student_id]['interaction_dates']:
                    data[student_id]['interaction_dates'].append(today)
                    data[student_id]['days_interacted'] = len(data[student_id]['interaction_dates'])
                    
                    # Auto-enable final test after 3 days
                    if data[student_id]['days_interacted'] >= 3 and not data[student_id]['final_test_completed']:
                        data[student_id]['final_test_enabled'] = True
                    
                    with open(self.student_tracking_file, 'w') as f:
                        json.dump(data, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error recording daily interaction: {e}")
            return False
    
    def get_student_tracking(self, student_id: str) -> Dict:
        """Get tracking data for a student"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                data = json.load(f)
            return data.get(student_id, {})
        except Exception as e:
            print(f"Error getting student tracking: {e}")
            return {}
    
    def get_all_student_tracking(self) -> Dict:
        """Get all student tracking data (for admin)"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error getting all student tracking: {e}")
            return {}
    
    def admin_enable_final_test(self, student_id: str, enabled: bool = True) -> bool:
        """Admin manually enable/disable final test for a student"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                data = json.load(f)
            
            if student_id in data:
                data[student_id]['final_test_enabled'] = enabled
                data[student_id]['admin_override'] = True
                
                with open(self.student_tracking_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error admin enabling final test: {e}")
            return False
    
    def update_final_test_completion(self, student_id: str) -> bool:
        """Mark final test as completed"""
        try:
            with open(self.student_tracking_file, 'r') as f:
                data = json.load(f)
            
            if student_id in data:
                data[student_id]['final_test_completed'] = True
                data[student_id]['final_test_date'] = datetime.now().isoformat()
                
                with open(self.student_tracking_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error updating final test completion: {e}")
            return False
    def reset_all_data(self) -> bool:
        """Admin function to clear all student data and start fresh"""
        try:
            # Reset chat history
            with open(self.chat_history_file, 'w') as f:
                json.dump({}, f, indent=2)
            
            # Reset student tracking
            with open(self.student_tracking_file, 'w') as f:
                json.dump({}, f, indent=2)
            
            # Delete performance ratings CSV if it exists
            if os.path.exists('data/performance_ratings.csv'):
                os.remove('data/performance_ratings.csv')
            
            # Delete assessments CSV if it exists
            if os.path.exists('data/assessments.csv'):
                os.remove('data/assessments.csv')
            
            return True
        except Exception as e:
            print(f"Error resetting all data: {e}")
            return False


    def export_group1_chat_to_excel(self, output_file: str = None) -> bool:
        """
        Export Group 1 chat history to Excel file
        Columns: User ID, Date, Concept/Query, Role, Message
        """
        try:
            if output_file is None:
                output_file = os.path.join(self.data_dir, "group1_chat_history.xlsx")
            
            # Load chat history
            if not os.path.exists(self.chat_history_file):
                print("No chat history found")
                return False
            
            with open(self.chat_history_file, 'r') as f:
                chat_data = json.load(f)
            
            # Load learning progress to get concepts/queries
            learning_data = {}
            if os.path.exists(self.learning_history_file):
                with open(self.learning_history_file, 'r') as f:
                    learning_data = json.load(f)
            
            # Prepare data for DataFrame
            rows = []
            for student_id, messages in chat_data.items():
                for msg in messages:
                    # Filter for Group 1 messages only
                    if 'Group 1' in msg.get('group', ''):
                        # Try to find the concept from learning history
                        concept = "General Question"
                        if student_id in learning_data:
                            for interaction in learning_data.get(student_id, []):
                                concept = interaction.get('concept', 'General Question')
                                break  # Use the most recent concept
                        
                        rows.append({
                            'User ID': student_id,
                            'Date': msg.get('timestamp', ''),
                            'Concept/Query': concept,
                            'Role': msg.get('role', '').title(),
                            'Message': msg.get('message', '')
                        })
            
            if not rows:
                print("No Group 1 chat messages found")
                return False
            
            # Create DataFrame and export to Excel
            df = pd.DataFrame(rows)
            df = df.sort_values(by=['User ID', 'Date'])
            df.to_excel(output_file, index=False, engine='openpyxl')
            
            print(f"Group 1 chat history exported to: {output_file}")
            return True
        
        except Exception as e:
            print(f"Error exporting Group 1 chat history: {e}")
            return False

    def export_group2_chat_to_excel(self, output_file: str = None) -> bool:
        """
        Export Group 2 chat history to Excel file
        Columns: User ID, Date, Query, Role, Message
        """
        try:
            if output_file is None:
                output_file = os.path.join(self.data_dir, "group2_chat_history.xlsx")
            
            # Load chat history
            if not os.path.exists(self.chat_history_file):
                print("No chat history found")
                return False
            
            with open(self.chat_history_file, 'r') as f:
                chat_data = json.load(f)
            
            # Prepare data for DataFrame
            rows = []
            for student_id, messages in chat_data.items():
                for msg in messages:
                    # Filter for Group 2 messages only
                    if msg.get('group', '') == 'Group 2':
                        rows.append({
                            'User ID': student_id,
                            'Date': msg.get('timestamp', ''),
                            'Query': 'Chat Conversation',  # Group 2 is free-form chat
                            'Role': msg.get('role', '').title(),
                            'Message': msg.get('message', '')
                        })
            
            if not rows:
                print("No Group 2 chat messages found")
                return False
            
            # Create DataFrame and export to Excel
            df = pd.DataFrame(rows)
            df = df.sort_values(by=['User ID', 'Date'])
            df.to_excel(output_file, index=False, engine='openpyxl')
            
            print(f"Group 2 chat history exported to: {output_file}")
            return True
        
        except Exception as e:
            print(f"Error exporting Group 2 chat history: {e}")
            return False

    def export_all_chats_to_excel(self) -> bool:
        """Export both Group 1 and Group 2 chat histories to separate Excel files"""
        try:
            group1_success = self.export_group1_chat_to_excel()
            group2_success = self.export_group2_chat_to_excel()
            
            if group1_success and group2_success:
                print("All chat histories exported successfully!")
                return True
            elif group1_success or group2_success:
                print("Some chat histories exported (check logs)")
                return True
            else:
                print("Failed to export chat histories")
                return False
        
        except Exception as e:
            print(f"Error exporting all chat histories: {e}")
            return False



    def _append_to_csv(self, csv_file: str, row_data: dict, group: int) -> bool:
        """Helper method to append a row to CSV file"""
        try:
            # Define columns based on group
            if group == 1:
                columns = ['User ID', 'Date', 'Concept/Query', 'Role', 'Message']
            else:  # group == 2
                columns = ['User ID', 'Date', 'Query', 'Role', 'Message']
            
            # Read existing data or create new DataFrame
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
            else:
                df = pd.DataFrame(columns=columns)
            
            # Append new row
            new_row = pd.DataFrame([row_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save to CSV`n            df.to_csv(csv_file, index=False)
            return True
        except Exception as e:
            print(f"Error appending to CSV: {e}")
            return False




