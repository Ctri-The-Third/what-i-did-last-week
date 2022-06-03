import sys
import logging

from bottle import route, run, request, response, post

from src.main_page_functions import (
    do_the_big_thing,
    get_credentials,
    get_user,
    run_auth_flow,
)


@route("/")
def index():
    params = request.query
    if "code" in params:
        try:
            creds = get_credentials(params["code"])
            user = get_user(creds)
            name = user["given_name"]
            email = user["email"]

            do_the_big_thing(creds, email)
        except Exception as err:
            return "something weird happened %s" % (err)
        return f"""Hey {name} Looks like you're logged in okay: <br/> I see we've consent for the following scopes...<br/>{scope_str}<br/>
        """
    else:
        return run_auth_flow()


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)], level=logging.INFO
    )

    port = 8080
    host = "127.0.0.1"
    print("PReparing to host")
    run(port=port, host=host, certfile="src/widlw.pem", keyfile="src/widlw-key.pem")
