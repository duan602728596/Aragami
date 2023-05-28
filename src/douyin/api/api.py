"""
请求抖音的相关API
"""
import json
import urllib3
import requests
import certifi
from src.douyin.api.utils import detail_params, post_params, live_params, USER_AGENT

certify_pem: str = certifi.where()


# 请求ttwid cookie
def request_ttwid_cookie() -> str:
    res: requests.Response = requests.post('https://ttwid.bytedance.com/ttwid/union/register/', json={
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
    }, verify=certify_pem)

    return res.headers['Set-Cookie'] or ''


# 请求video或note的信息
def request_detail(aweme_id: str, cookie: str) -> map or None:
    params: str = detail_params(aweme_id)
    manager: urllib3.PoolManager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certify_pem)
    manager.headers = {
        'Referer': 'https://www.douyin.com/video/' + aweme_id,
        'Host': 'www.douyin.com',
        'User-Agent': USER_AGENT,
        'cookie': cookie,
    }
    res: urllib3.HTTPResponse = manager.request('GET', 'https://www.douyin.com/aweme/v1/web/aweme/detail/?' + params)

    try:
        return json.loads(res.data)
    except json.decoder.JSONDecodeError:
        return None


# 请求user的信息
def request_post(sec_user_id: str, max_cursor: int, cookie: str) -> map or None:
    params: str = post_params(sec_user_id, max_cursor)
    manager: urllib3.PoolManager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certify_pem)
    manager.headers = {
        'Referer': 'https://www.douyin.com/user/' + sec_user_id,
        'Host': 'www.douyin.com',
        'User-Agent': USER_AGENT,
        'cookie': cookie,
    }
    res: urllib3.HTTPResponse = manager.request('GET', 'https://www.douyin.com/aweme/v1/web/aweme/post/?' + params)

    try:
        return json.loads(res.data)
    except json.decoder.JSONDecodeError:
        return None


# 请求直播的信息
def request_live_enter(live_id: str, cookie: str) -> map or None:
    params: str = live_params(live_id)
    manager: urllib3.PoolManager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certify_pem)
    manager.headers = {
        'Referer': 'https://live.douyin.com/',
        'Host': 'live.douyin.com',
        'User-Agent': USER_AGENT,
        'cookie': cookie,
    }
    res: urllib3.HTTPResponse = manager.request('GET', 'https://live.douyin.com/webcast/room/web/enter/?' + params)

    try:
        return json.loads(res.data)
    except json.decoder.JSONDecodeError:
        return None


# 请求分享链接
def request_share_url(url: str, cookie: str) -> str:
    res: requests.Response = requests.get(url, headers={
        'Host': 'v.douyin.com',
        'User-Agent': USER_AGENT,
        'cookie': cookie,
    }, verify=certify_pem, allow_redirects=False)

    return res.text
