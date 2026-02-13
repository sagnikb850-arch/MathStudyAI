"""
Automatic Data Backup Utility
Exports data files every 10 minutes when admin is logged in
"""
import os
import json
import zipfile
import threading
import time
from datetime import datetime
from io import BytesIO
import streamlit as st


class AutoBackup:
    """Auto-backup manager for data files"""
    
    def __init__(self, data_dir='data', backup_interval=600):
        """
        Initialize auto-backup
        
        Args:
            data_dir: Directory containing data files
            backup_interval: Backup interval in seconds (default 600 = 10 minutes)
        """
        self.data_dir = data_dir
        self.backup_interval = backup_interval
        self.last_backup = None
        self.backup_enabled = False
        
    def should_backup(self):
        """Check if it's time for a backup"""
        if not self.backup_enabled:
            return False
            
        if self.last_backup is None:
            return True
            
        elapsed = time.time() - self.last_backup
        return elapsed >= self.backup_interval
    
    def create_backup_zip(self):
        """Create ZIP archive of all data files"""
        data_files = {
            "chat_history.json": os.path.join(self.data_dir, "chat_history.json"),
            "group1_chat_history.csv": os.path.join(self.data_dir, "group1_chat_history.csv"),
            "group2_chat_history.csv": os.path.join(self.data_dir, "group2_chat_history.csv"),
            "learning_history.json": os.path.join(self.data_dir, "learning_history.json"),
            "student_progress.json": os.path.join(self.data_dir, "student_progress.json"),
            "student_tracking.json": os.path.join(self.data_dir, "student_tracking.json"),
            "assessments.csv": os.path.join(self.data_dir, "assessments.csv"),
            "performance_ratings.csv": os.path.join(self.data_dir, "performance_ratings.csv"),
            "comparison_results.csv": os.path.join(self.data_dir, "comparison_results.csv")
        }
        
        # Create ZIP in memory
        zip_buffer = BytesIO()
        files_added = 0
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, file_path in data_files.items():
                if os.path.exists(file_path):
                    zip_file.write(file_path, file_name)
                    files_added += 1
        
        if files_added == 0:
            return None, "No data files found"
            
        zip_buffer.seek(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mathstudyai_backup_{timestamp}.zip"
        
        self.last_backup = time.time()
        return zip_buffer.getvalue(), filename
    
    def enable(self):
        """Enable automatic backups"""
        self.backup_enabled = True
    
    def disable(self):
        """Disable automatic backups"""
        self.backup_enabled = False
    
    def get_time_until_next_backup(self):
        """Get seconds until next backup"""
        if not self.backup_enabled or self.last_backup is None:
            return 0
        
        elapsed = time.time() - self.last_backup
        remaining = max(0, self.backup_interval - elapsed)
        return int(remaining)
    
    def get_last_backup_time(self):
        """Get formatted last backup time"""
        if self.last_backup is None:
            return "Never"
        
        return datetime.fromtimestamp(self.last_backup).strftime("%Y-%m-%d %H:%M:%S")


# Global instance
_auto_backup = None

def get_auto_backup():
    """Get or create global auto-backup instance"""
    global _auto_backup
    if _auto_backup is None:
        _auto_backup = AutoBackup(data_dir='data', backup_interval=600)  # 10 minutes
    return _auto_backup
