# modules/gmail_api.py
import os.path
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/Users/Mac/Downloads/Coding/MMT/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_id = msg['id']
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])

        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        date_raw = next((h['value'] for h in headers if h['name'] == 'Date'), '')

        try:
            date_obj = email.utils.parsedate_to_datetime(date_raw)
            date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        except:
            date_str = date_raw

        body = ''
        parts = payload.get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode()
                    break

        emails.append({
            'id': msg_id,
            'from': sender,
            'subject': subject,
            'date': date_str,
            'body': body
        })
    return emails

def parse_command(email):
    return email['body'].strip().lower()

def mark_as_read(service, email_id):
    service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()