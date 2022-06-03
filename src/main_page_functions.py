from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.controller import Controller, load_config
from src.workItem import WorkItem

ALL_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
    "https://www.googleapis.com/auth/calendar.events.readonly",
    "https://www.googleapis.com/auth/gmail.metadata",
]


def run_auth_flow() -> str:
    "if the user has not already logged in, run the auth flow"

    flow = Flow.from_client_secrets_file(
        "src/gcredentials.secret",
        scopes=ALL_SCOPES,
        redirect_uri="https://widlw.ctri.co.uk/",
    )

    url = flow.authorization_url(prompt="consent")[0]

    return r"""
    <script type="text/javascript">
        function redirect() {
            window.location.replace("%s")
        }
        setTimeout(redirect,1000); 
    </script>
    <p><b>hello there.</b><br/> To use WIDLW, use the google login flow link below<br/> <a href = "%s">link</a><br/> Redirecting in ~1 second</p>
    
    """ % (
        url,
        url,
    )


def get_credentials(code) -> Credentials:
    try:
        flow = Flow.from_client_secrets_file(
            "src/gcredentials.secret",
            scopes=ALL_SCOPES,
            redirect_uri="https://widlw.ctri.co.uk/",
        )

        flow.fetch_token(code=code)
    except Exception as err:
        return f"yo, something weird went wrong with that google login - best return back to the <a href = '/'> home page</a> and try again"

        # print(service)
    return flow.credentials


def get_user(creds: Credentials) -> dict:
    user_info_svc = build("oauth2", "v2", credentials=creds)
    try:
        user_info = user_info_svc.userinfo().get().execute()
        return user_info
    except Exception as err:
        name = "$ERROR"
        print(err)


def do_the_big_thing(creds: Credentials, target: str) -> str:
    cfg = load_config()
    target

    con = Controller(target)

    con.fetch_tasks()

    current_section = ""
    for log in con.work_items:
        log: WorkItem
        if log.source != current_section:
            print(f"--------------{log.source}-------------")
            current_section = log.source
        print(log)
