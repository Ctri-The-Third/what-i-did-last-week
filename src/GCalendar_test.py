import json
import logging
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport import Request
import pickle


ALL_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]


creds = None
if os.path.exists("creds.secret"):
    creds = Credentials.from_authorized_user_file("creds.secret", ALL_SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:

        flow = InstalledAppFlow.from_client_secrets_file(
            "src/gcredentials.secret", ALL_SCOPES
        )
        print(flow.authorization_url())
        creds = flow.run_local_server(port=8888)

        with open("creds.secret", "w+") as creds_file:
            creds_file.write(creds.to_json())
