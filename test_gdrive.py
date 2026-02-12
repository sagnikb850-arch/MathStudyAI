"""
Test Google Drive Integration
Run this on Streamlit Cloud to diagnose issues
"""
import streamlit as st
from utils.gdrive_sync import get_gdrive_sync

st.title("🔍 Google Drive Integration Test")

st.write("---")
st.header("1. Checking Secrets Configuration")

# Check if secrets exist
if hasattr(st, 'secrets'):
    if 'google_drive' in st.secrets:
        st.success("✅ Google Drive secrets found!")
        
        # Show what fields are present
        fields = list(st.secrets['google_drive'].keys())
        st.write(f"**Found {len(fields)} fields:**")
        st.write(", ".join(fields))
        
        # Check critical fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing = [f for f in required_fields if f not in fields]
        
        if missing:
            st.error(f"❌ Missing required fields: {', '.join(missing)}")
        else:
            st.success("✅ All required fields present")
            
        # Show service account email
        if 'client_email' in st.secrets['google_drive']:
            email = st.secrets['google_drive']['client_email']
            st.info(f"**Service Account Email:** `{email}`")
            st.write("⚠️ Make sure you shared your Google Drive folder with this email!")
    else:
        st.error("❌ No 'google_drive' section found in secrets")
        st.write("You need to add the Google Drive credentials to Streamlit Cloud secrets")
else:
    st.error("❌ No secrets configured")

st.write("---")
st.header("2. Testing Google Drive Connection")

gdrive = get_gdrive_sync()

if gdrive.enabled:
    st.success("✅ Google Drive sync is ENABLED")
    st.write(f"**Folder ID:** `{gdrive.folder_id}`")
    st.write(f"**Folder URL:** https://drive.google.com/drive/u/0/folders/{gdrive.folder_id}")
    
    st.write("---")
    st.header("3. Test File Upload")
    
    if st.button("Upload Test File"):
        try:
            import os
            import json
            from datetime import datetime
            
            # Create test file
            test_data = {
                "test": "Google Drive integration test",
                "timestamp": datetime.now().isoformat(),
                "status": "testing"
            }
            
            test_file = "data/test_gdrive.json"
            os.makedirs("data", exist_ok=True)
            
            with open(test_file, 'w') as f:
                json.dump(test_data, f, indent=2)
            
            st.info("📤 Uploading test file...")
            
            file_id = gdrive.upload_file(test_file)
            
            if file_id:
                st.success(f"✅ Test file uploaded successfully! File ID: {file_id}")
                st.write("Check your Google Drive folder - you should see 'test_gdrive.json'")
            else:
                st.error("❌ Upload failed. Check the error messages above.")
                st.write("**Possible issues:**")
                st.write("- Google Drive folder not shared with service account")
                st.write("- Invalid folder ID")
                st.write("- Permission denied")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            
else:
    st.error("❌ Google Drive sync is DISABLED")
    st.write("**Possible reasons:**")
    st.write("- Secrets not configured in Streamlit Cloud")
    st.write("- Missing or invalid credentials")
    st.write("- Configuration error")

st.write("---")
st.header("4. Checklist")

checklist = [
    ("Created Google Cloud project and enabled Drive API", False),
    ("Created service account and downloaded JSON key", False),
    ("Added secrets to Streamlit Cloud (Settings → Secrets)", False),
    ("Shared Google Drive folder with service account email", False),
    ("Gave service account 'Editor' permission", False),
    ("Redeployed the app after adding secrets", False)
]

st.write("**Setup Checklist:**")
for item, checked in checklist:
    st.write(f"{'✅' if checked else '⬜'} {item}")

st.write("---")
st.info("💡 **Next Steps:** If any checks fail, follow the setup guide in GOOGLE_DRIVE_SETUP.md")
