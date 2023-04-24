from src.api.api import request_ttwid_cookie, request_detail, request_post, request_live_enter
from src.api.utils import random_string


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
