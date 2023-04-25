import time
from src.api.api import request_ttwid_cookie, request_detail, request_post, request_live_enter
from src.api.utils import random_string
from src.call.parser import parse


# 生成cookie
def get_cookie() -> str:
    passport_csrf_token: str = random_string(32)
    ttwid: str = request_ttwid_cookie()

    return '; '.join((
        ttwid,
        'passport_csrf_token=' + passport_csrf_token,
        'passport_csrf_token_default=' + passport_csrf_token
    ))


# 请求video或note的信息
def detail(aweme_id: str):
    return request_detail(aweme_id, get_cookie())


# 请求user的信息
def post(sec_user_id: str, max_cursor: int):
    return request_post(sec_user_id, max_cursor, get_cookie())


# 请求直播的信息
def live_enter(live_id: str):
    return request_live_enter(live_id, get_cookie())


# 输入url，返回对应的信息
def call_api(url: str, **kwargs):
    parse_result = parse(url)
    max_cursor = kwargs.get('max_cursor')

    if not parse_result:
        return None

    if parse_result['type'] == 'video':
        return detail(parse_result['id'])

    elif parse_result['type'] == 'user':
        return post(parse_result['id'], max_cursor or int(time.time() * 1_000))
