"""
Google Drive Sync Utility
Syncs data files (CSV, JSON) to Google Drive folder
"""
import os
import json
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import streamlit as st


class GoogleDriveSync:
    """
    Sync local data files to Google Drive
    Uses service account credentials from Streamlit secrets
    """
    
    # Your Google Drive folder ID from the URL
    FOLDER_ID = "1YMvj1BCtsGXE-6tB9fdTY6ESjSUFTZBf"
    
    def __init__(self):
        """Initialize Google Drive API client"""
        self.service = None
        self.enabled = False
        self.folder_id = self.FOLDER_ID
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Drive service with credentials from Streamlit secrets"""
        try:
            # Try to get credentials from Streamlit secrets
            if hasattr(st, 'secrets') and 'google_drive' in st.secrets:
                # Load service account credentials from secrets
                credentials_dict = dict(st.secrets['google_drive'])
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
                
                self.service = build('drive', 'v3', credentials=credentials)
                self.enabled = True
                print("✅ Google Drive sync enabled")
            else:
                print("⚠️ Google Drive credentials not found in secrets. Sync disabled.")
                self.enabled = False
                
        except Exception as e:
            print(f"⚠️ Google Drive initialization failed: {e}. Sync disabled.")
            self.enabled = False
    
    def upload_file(self, file_path: str, folder_id: str = None) -> Optional[str]:
        """
        Upload or update a file to Google Drive
        
        Args:
            file_path: Local file path to upload
            folder_id: Google Drive folder ID (defaults to FOLDER_ID)
            
        Returns:
            File ID if successful, None otherwise
        """
        if not self.enabled:
            print("⚠️ Google Drive sync not enabled")
            return None
        
        try:
            file_name = os.path.basename(file_path)
            folder_id = folder_id or self.FOLDER_ID
            
            print(f"📤 Attempting to upload {file_name} to folder {folder_id}")
            
            # Check if file already exists in folder
            existing_file_id = self._find_file_in_folder(file_name, folder_id)
            
            # Determine MIME type
            mime_type = 'application/json' if file_path.endswith('.json') else 'text/csv'
            
            if existing_file_id:
                # Update existing file
                print(f"🔄 Updating existing file {file_name} (ID: {existing_file_id})")
                media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
                updated_file = self.service.files().update(
                    fileId=existing_file_id,
                    media_body=media
                ).execute()
                print(f"✅ Updated {file_name} in Google Drive")
                return updated_file.get('id')
            else:
                # Create new file
                print(f"📝 Creating new file {file_name}")
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
                created_file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                print(f"✅ Uploaded {file_name} to Google Drive")
                return created_file.get('id')
                
        except HttpError as error:
            print(f"❌ Google Drive HTTP error: {error}")
            print(f"❌ Error details: {error.resp.status} - {error.error_details}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error during upload: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _find_file_in_folder(self, file_name: str, folder_id: str) -> Optional[str]:
        """
        Find a file by name in a specific folder
        
        Returns:
            File ID if found, None otherwise
        """
        try:
            query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            files = results.get('files', [])
            return files[0]['id'] if files else None
            
        except Exception as e:
            print(f"⚠️ Error finding file: {e}")
            return None
    
    def sync_data_folder(self, data_dir: str = "data") -> dict:
        """
        Sync all files in data folder to Google Drive
        
        Args:
            data_dir: Local data directory path
            
        Returns:
            Dictionary with sync results
        """
        if not self.enabled:
            return {"success": False, "error": "Google Drive sync not enabled"}
        
        results = {
            "success": True,
            "uploaded": [],
            "failed": []
        }
        
        try:
            # Sync JSON files
            json_files = ['chat_history.json', 'learning_history.json', 
                         'learning_progress.json', 'student_progress.json', 
                         'student_tracking.json']
            
            # Sync CSV files
            csv_files = ['assessments.csv', 'performance_ratings.csv', 
                        'comparison_results.csv', 'group1_chat_history.csv', 
                        'group2_chat_history.csv']
            
            all_files = json_files + csv_files
            
            for file_name in all_files:
                file_path = os.path.join(data_dir, file_name)
                if os.path.exists(file_path):
                    file_id = self.upload_file(file_path)
                    if file_id:
                        results["uploaded"].append(file_name)
                    else:
                        results["failed"].append(file_name)
            
            if results["failed"]:
                results["success"] = False
                
        except Exception as e:
            results["success"] = False
            results["error"] = str(e)
        
        return results


# Global instance for easy access
_gdrive_sync = None

def get_gdrive_sync() -> GoogleDriveSync:
    """Get or create global GoogleDriveSync instance"""
    global _gdrive_sync
    if _gdrive_sync is None:
        _gdrive_sync = GoogleDriveSync()
    return _gdrive_sync
