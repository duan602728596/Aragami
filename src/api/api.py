import json
import requests
import urllib3
from src.api.utils import detail_params, USER_AGENT


# 请求ttwid的cookie
def request_ttwid_cookie() -> str:
    res = requests.post("https://ttwid.bytedance.com/ttwid/union/register/", json={
        "region": "union",
        "aid": 1768,
        "needFid": False,
        "service": "www.ixigua.com",
        "migrate_info": {
            "ticket": "",
            "source": "source",
        },
        "cbUrlProtocol": "https",
        "union": True,
    })

    return res.headers["Set-Cookie"] or ""


# 请求detail
def request_detail(id: str, cookie: str):
    params: str = detail_params(id)
    http = urllib3.PoolManager()
    http.headers = {
        "Referer": "https://www.douyin.com/video/" + id,
        "Host": "www.douyin.com",
        "User-Agent": USER_AGENT,
        "cookie": cookie
    }
    res = http.request("GET", "https://www.douyin.com/aweme/v1/web/aweme/detail/?" + params)

    return json.loads(res.data)
