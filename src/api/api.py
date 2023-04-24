import json
import requests
import urllib3
import certifi
from src.api.utils import detail_params, USER_AGENT


# 请求ttwid的cookie
def request_ttwid_cookie() -> str:
    res = requests.post('https://ttwid.bytedance.com/ttwid/union/register/', json={
        'region': 'union',
        'aid': 1768,
        'needFid': False,
        'service': 'www.ixigua.com',
        'migrate_info': {
            'ticket': '',
            'source': 'source',
        },
        'cbUrlProtocol': 'https',
        'union': True,
    }, verify=False)

    return res.headers['Set-Cookie'] or ''


# 请求detail
def request_detail(id: str, cookie: str):
    params: str = detail_params(id)
    manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    manager.headers = {
        'Referer': 'https://www.douyin.com/video/' + id,
        'Host': 'www.douyin.com',
        'User-Agent': USER_AGENT,
        'cookie': cookie,
    }
    res = manager.request('GET', 'https://www.douyin.com/aweme/v1/web/aweme/detail/?' + params)

    return json.loads(res.data)
