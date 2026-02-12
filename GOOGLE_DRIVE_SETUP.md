# Google Drive Integration Setup Guide

## Overview
This guide will help you set up Google Drive integration to automatically sync all chat history, assessments, and student data to your Google Drive folder.

**Your Google Drive Folder:**
https://drive.google.com/drive/folders/1kq4MQZsYeiF3-5UUGN7FDunc2dhT6suO

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "MathStudyAI-Drive" and click "Create"

---

## Step 2: Enable Google Drive API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it and press "Enable"

---

## Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: `mathstudyai-sync`
4. Description: `Service account for syncing data to Google Drive`
5. Click "Create and Continue"
6. Skip optional steps and click "Done"

---

## Step 4: Generate Service Account Key

1. In "Credentials" page, click on your service account email
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose **JSON** format
5. Click "Create" - a JSON file will download

---

## Step 5: Share Google Drive Folder

1. Open your Google Drive folder: https://drive.google.com/drive/folders/1kq4MQZsYeiF3-5UUGN7FDunc2dhT6suO
2. Click "Share" button
3. Add the service account email (looks like: `mathstudyai-sync@your-project.iam.gserviceaccount.com`)
4. Give it **Editor** access
5. Click "Share"

---

## Step 6: Configure Streamlit Secrets

### For Local Development (`.streamlit/secrets.toml`):

Create `.streamlit/secrets.toml` in your project root:

```toml
# OpenAI API Key
OPENAI_API_KEY = "your-openai-key-here"

# Google Drive Credentials
[google_drive]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "mathstudyai-sync@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

**Copy all values from your downloaded JSON key file into the `[google_drive]` section.**

---

### For Streamlit Cloud Deployment:

1. Go to your app on [Streamlit Cloud](https://share.streamlit.io/)
2. Click the 3 dots menu → "Settings"
3. Go to "Secrets" section
4. Paste the same content from above (including the `[google_drive]` section)
5. Click "Save"

---

## Step 7: Test the Integration

### Verify Setup:

```python
from utils.gdrive_sync import get_gdrive_sync

gdrive = get_gdrive_sync()
if gdrive.enabled:
    print("✅ Google Drive sync is enabled!")
else:
    print("❌ Google Drive sync is not configured")
```

### Manual Sync Test:

```python
# Sync all data files
from utils.data_storage import DataStorage

storage = DataStorage()
if storage.gdrive and storage.gdrive.enabled:
    results = storage.gdrive.sync_data_folder()
    print(f"Uploaded: {results['uploaded']}")
    print(f"Failed: {results['failed']}")
```

---

## Files That Will Be Synced

The following files are automatically synced to your Google Drive folder:

### JSON Files:
- `chat_history.json` - All chat conversations
- `learning_history.json` - Learning progress tracking
- `learning_progress.json` - Student learning milestones
- `student_progress.json` - Student advancement data
- `student_tracking.json` - Student session tracking

### CSV Files:
- `assessments.csv` - Pre and post assessment answers
- `performance_ratings.csv` - Performance analysis results
- `comparison_results.csv` - Group comparison statistics
- `group1_chat_history.csv` - Group 1 chat logs with concepts
- `group2_chat_history.csv` - Group 2 chat logs

---

## Automatic Sync

Files are synced automatically:
- ✅ Every time a chat message is saved
- ✅ After each assessment is completed
- ✅ When student progress is updated
- ✅ Real-time for CSV exports

---

## Troubleshooting

### "Google Drive sync not enabled" message:
- Check that `secrets.toml` has the `[google_drive]` section
- Verify all fields from JSON key are copied correctly
- Ensure no extra quotes or spaces in the private_key field

### "Permission denied" errors:
- Make sure you shared the Google Drive folder with the service account email
- Give the service account "Editor" permissions

### Files not appearing in Drive:
- Check the folder ID is correct: `1kq4MQZsYeiF3-5UUGN7FDunc2dhT6suO`
- Verify service account has access to the folder
- Check Streamlit logs for error messages

---

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.streamlit/secrets.toml` to Git
- Add `.streamlit/` to your `.gitignore`
- Service account keys are sensitive - treat them like passwords
- Only share the Google Drive folder with the service account, not publicly

---

## Benefits

✅ **Persistent Storage:** Data survives Streamlit Cloud redeployments
✅ **Backup:** All data automatically backed up to Google Drive
✅ **Access:** View and analyze data from anywhere via Google Drive
✅ **Collaboration:** Share folder with team members for data analysis
✅ **Version History:** Google Drive tracks file version history

---

## File Storage Structure

Your Google Drive folder will contain:
```
MathStudyAI/
├── chat_history.json
├── learning_history.json
├── learning_progress.json
├── student_progress.json
├── student_tracking.json
├── assessments.csv
├── performance_ratings.csv
├── comparison_results.csv
├── group1_chat_history.csv
└── group2_chat_history.csv
```

All files update in real-time as students interact with the application!
