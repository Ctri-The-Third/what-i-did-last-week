
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

scopes = ["https://www.googleapis.com/auth/gmail.metadata"
, "https://www.googleapis.com/auth/userinfo.profile"
, "https://www.googleapis.com/auth/calendar.events.readonly"]


creds = Credentials(None)
flow = Flow.from_client_secrets_file(
    "src/gcredentials.secret",
    scopes=scopes,
    redirect_uri="https://widlw.ctri.co.uk/"
    )

url = flow.authorization_url(prompt="consent")


