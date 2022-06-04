import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.controller import Controller, load_config
from src.workItem import WorkItem
from src.common_methods import convert_jira_time_str_to_min, convert_min_to_time_str
from markdown import markdown

ALL_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]


def run_auth_flow() -> str:
    "if the user has not already logged in, run the auth flow"

    flow = Flow.from_client_secrets_file(
        "src/gcredentials.secret",
        scopes=ALL_SCOPES,
        redirect_uri="https://widlw.ctri.co.uk/",
    )

    url = flow.authorization_url(prompt="consent")[0]

    f = open(r"src/intro_page.md", "r+")
    md_content = f.read().format(url=url, envs="")
    html = markdown(md_content)

    return html


def get_credentials(code) -> Credentials:
    try:
        flow = Flow.from_client_secrets_file(
            "src/gcredentials.secret",
            scopes=ALL_SCOPES,
            redirect_uri="https://widlw.ctri.co.uk/",
        )

        flow.fetch_token(code=code)
    except Exception as err:
        return f"yo, something weird went wrong with that google login - best return back to the <a href = '/'> home page</a> and try again<br>{err}"

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


def do_the_big_thing(creds: Credentials, target: str) -> list:

    con = Controller(target, creds)

    con.fetch_tasks()

    return con


def output_work_items(cont: Controller) -> str:
    "Fill the markdown format with the content."
    work_items = cont.work_items
    total_time = 0
    table_rows = ""
    work_items.sort(reverse=True)
    for item in work_items:
        item: WorkItem

        total_time += convert_jira_time_str_to_min(item.time_str)
        status_emoji = "🟢" if item.done else "🟡"

        table_rows += f"| {item.source} | [{item.id[0:13]}]({item.url}) | {status_emoji} | {item.time_str} | {item.summary} | \n"
    total_time = convert_min_to_time_str(total_time)
    f = open(r"src/output_page.md", "r+")
    md_content = f.read().format(
        total_time=total_time, table_entries=table_rows, start_date=cont.last_week_date
    )
    html = markdown(md_content, extensions=["tables"])
    return html
