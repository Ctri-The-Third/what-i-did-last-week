import sys
import logging

from bottle import route, run, request, response, post
from src.workItem import WorkItem
from src.main_page_functions import *


PORT = 8080
HOSTNAME = "127.0.0.1"


@route("/")
def index():
    params = request.query
    params: dict
    if "code" in params:
        try:
            creds = get_credentials(params["code"])
            if isinstance(creds, str):
                return creds
            user = get_user(creds)
            name = user["given_name"]
            email = user["email"]

        except Exception as err:
            return "something weird happened %s" % (err)

        # user is logged in and there are no issues yet - deploy!
        
        return output_work_items(do_the_big_thing(creds, email))

    else:

        return run_auth_flow()


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)], level=logging.INFO
    )

    print("Preparing to host")
    run(
        port=PORT,
        host=HOSTNAME,
        # server="gunicorn",
        certfile="src/widlw.pem",
        keyfile="src/widlw.key",
    )
