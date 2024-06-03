import requests
import json
from .context import get_by_headers


def get_http_session(token: str = '') -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": token,
        "biz_id": "spring",
        "Content-Type": "application/json",
        "Rpc-Persist-AUTH-TYPE": "user",
    })

    tt_env = get_by_headers("x-tt-env")
    if tt_env:
        s.headers.update({'x-tt-env': tt_env})

    user = get_by_headers("x-kunlun-initiator")
    if user:
        user_id = json.loads(user)['_id']
        s.headers.update({'User': str(user_id)})

    return s
