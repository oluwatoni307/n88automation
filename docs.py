from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# === Set up ===
SERVICE_ACCOUNT_FILE = 'service.json'
FOLDER_ID = '1tm8mpJgD0_MYuIjsXfyMRVZFCFdVDepG'  # Folder ID from your personal Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

text = """
# The Clockmaker's Secret

## Chapter 1: The Town of Tickenvale

Nestled between two silent mountains and a forest that whispered secrets, the town of **Tickenvale** was best known for two things: its timeless sunsets and an old clock tower that hadn't worked in 102 years. No one remembered who had built the clock—except for one man: **Elijah Grinshaw**, the clockmaker.

Elijah was 87, half-blind, and spoke more to gears than to people. His workshop smelled of rust and lavender, a combination only he seemed to find comforting. For decades, he tinkered with clocks of all sizes—but never the tower clock.

## Chapter 2: A Curious Visitor

One chilly autumn morning, a girl named **Lina** wandered into Tickenvale. She was a traveler, guided by instinct and a pocket compass that never pointed north. She asked the townsfolk, _"Why doesn't the clock tower work?"_ They only shrugged.

But Elijah, standing nearby, froze.

> “Because it’s waiting,” he whispered.

## Chapter 3: The Midnight Clue

That night, Lina followed a dim glow from the tower. She climbed the narrow spiral staircase, each step groaning with age. At the top, a curious sight met her eyes: a note pinned to the central cogwheel.

> “Only when heart and time align shall the town breathe anew.”

As the clock struck midnight, for the first time in a century, a faint *tick* echoed.

## Chapter 4: Heart and Time

Lina returned to Elijah’s workshop. There, she learned the truth: the clock ran not on gears, but on **memories**. Long ago, Elijah had built it for his lost love, embedding their shared memories in its core. But when she passed, the clock stopped.

Tears in his eyes, Elijah handed Lina an old locket.

> “Place this in the heart of the tower.”

## Chapter 5: Time Restored

Lina climbed the tower once more. She placed the locket inside the mechanism. The gears groaned, shivered, and then roared to life. Bells rang out across Tickenvale. The sky, as if awakened, burned gold with the rising sun.

Elijah smiled for the first time in years. And the town of Tickenvale remembered how to listen to the rhythm of time once more.

---

*Sometimes, it takes a stranger to wind up an old heart.*
"""

try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)
    docs_service = build('docs', 'v1', credentials=credentials)
except FileNotFoundError:
    print("Error: Service account file 'service.json' not found.")
    exit(1)
except Exception as e:
    print(f"Error setting up credentials: {e}")
    exit(1)

# === Step 1: Create a new Google Docs document ===
try:
    file_metadata = {
        'name': 'Hello Document',
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [FOLDER_ID]
    }
    new_doc = drive_service.files().create(
        body=file_metadata
    ).execute()
    document_id = new_doc['id']
    print(f"✔ Created Document ID: {document_id}")
    print(f"Access it here: https://docs.google.com/document/d/{document_id}/edit")
except HttpError as e:
    print(f"Error creating document: {e}")
    if e.resp.status == 404:
        print("Check if FOLDER_ID is correct and shared with the service account.")
    exit(1)

# === Step 2: Insert "hello" into the document ===
try:
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': text
            }
        }
    ]
    response = docs_service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()
    print("✔ Added 'hello' to the document.")
except HttpError as e:
    print(f"Error adding text to document: {e}")
    exit(1)

# === Step 3: Make the document editable by anyone with the link ===
try:
    permission = {
        'type': 'anyone',
        'role': 'writer'
    }
    drive_service.permissions().create(
        fileId=document_id,
        body=permission
    ).execute()
    print("✔ Set permissions: Anyone with the link can edit.")
except HttpError as e:
    print(f"Error setting permissions: {e}")
    exit(1)

