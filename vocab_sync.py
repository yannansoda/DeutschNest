import json
import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDS_FILE = 'credentials.json'
DRIVE_FILE_NAME = 'deutschnest_vocab.json'
LOCAL_FILE = 'vocab.json'

def get_gdrive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

def download_vocab():
    service = get_gdrive_service()
    results = service.files().list(q=f"name='{DRIVE_FILE_NAME}'", spaces='drive').execute()
    files = results.get('files', [])
    if files:
        file_id = files[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(LOCAL_FILE, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    else:
        with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def upload_vocab():
    service = get_gdrive_service()
    results = service.files().list(q=f"name='{DRIVE_FILE_NAME}'", spaces='drive').execute()
    files = results.get('files', [])
    media = MediaFileUpload(LOCAL_FILE, mimetype='application/json')
    if files:
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
    else:
        file_metadata = {'name': DRIVE_FILE_NAME}
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def load_vocab():
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_vocab(vocab_list):
    with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab_list, f, ensure_ascii=False, indent=2)
    upload_vocab()
