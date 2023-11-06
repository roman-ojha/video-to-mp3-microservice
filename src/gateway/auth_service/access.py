import os
import requests
from decouple import config


def login(request):
    # getting authorization header
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    # if username and password exist
    basicAuth = (auth.username, auth.password)

    # Now here we will going to do a post request on auth service
    response = requests.post(
        # f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
        f"http://{config('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
