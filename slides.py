from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# === Set up ===
SERVICE_ACCOUNT_FILE = '/etc/secrets/service.json'
TEMPLATE_PRESENTATION_ID = '1RuvpF6yzv2cBsXULKU6g4FpOcxY0BxYwHQFwkPnG9cg'
FOLDER_ID = '1tm8mpJgD0_MYuIjsXfyMRVZFCFdVDepG'  # Replace with the folder ID from your personal Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations'
]


try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)
    slides_service = build('slides', 'v1', credentials=credentials)
except FileNotFoundError:
    print("Error: Service account file 'service.json' not found.")
    exit(1)
except Exception as e:
    print(f"Error setting up credentials: {e}")
    exit(1)

# === Step 1: Copy the presentation to your personal Drive ===
try:
    copied_file = {
        'name': 'Jordan Meeting - Auto Copy',
        'parents': [FOLDER_ID]
    }
    copied_presentation = drive_service.files().copy(
        fileId=TEMPLATE_PRESENTATION_ID,
        body=copied_file
    ).execute()
    copied_presentation_id = copied_presentation['id']
    print(f"✔ Copied Presentation ID: {copied_presentation_id}")
    print(f"Access it here: https://docs.google.com/presentation/d/{copied_presentation_id}/edit")
except HttpError as e:
    print(f"Error copying presentation: {e}")
    if e.resp.status == 404:
        print("Check if TEMPLATE_PRESENTATION_ID or FOLDER_ID is correct and shared with the service account.")
    exit(1)

# === Step 2: Make the presentation editable by anyone with the link ===
try:
    permission = {
        'type': 'anyone',
        'role': 'writer'
    }
    drive_service.permissions().create(
        fileId=copied_presentation_id,
        body=permission
    ).execute()
    print("✔ Set permissions: Anyone with the link can edit.")
except HttpError as e:
    print(f"Error setting permissions: {e}")
    exit(1)

# # === Optional Step: Share with your personal email ===
# try:
#     permission = {
#         'type': 'user',
#         'role': 'writer',
#         'emailAddress': 'your-email@example.com'  # Replace with your personal Google account email
#     }
#     drive_service.permissions().create(
#         fileId=copied_presentation_id,
#         body=permission
#     ).execute()
#     print("✔ Shared presentation with your-email@example.com")
# except HttpError as e:
#     print(f"Error sharing presentation: {e}")
#     exit(1)

# === Step 3: Modify placeholder text in the new presentation ===
requests = [
    {
        'replaceAllText': {
            'containsText': {
                'text': '{{placeholder}}',
                'matchCase': True
            },
            'replaceText': 'Edited from duplicated template!'
        }
    }
]

try:
    response = slides_service.presentations().batchUpdate(
        presentationId=copied_presentation_id,
        body={'requests': requests}
    ).execute()
    print("✔ Duplicated presentation edited successfully.")
except HttpError as e:
    print(f"Error editing presentation: {e}")
    exit(1)

# === Step 4: List files to help locate the presentation ===
# try:
#     results = drive_service.files().list(
#         q="name='Jordan Meeting - Auto Copy' and mimeType='application/vnd.google-apps.presentation'",
#         fields="files(id, name, webViewLink)"
#     ).execute()
#     files = results.get('files', [])
#     if files:
#         print("\nFound presentations with name 'Jordan Meeting - Auto Copy':")
#         for file in files:
#             print(f"- ID: {file['id']}, Name: {file['name']}, Link: {file['webViewLink']}")
#     else:
#         print("\nNo presentations found with name 'Jordan Meeting - Auto Copy'.")
# except HttpError as e:
#     print(f"Error listing files: {e}")