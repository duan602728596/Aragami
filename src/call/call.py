from src.api.api import request_ttwid_cookie, request_detail, request_post
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


def detail(aweme_id: str):
    return request_detail(aweme_id, get_cookie())


def post(sec_user_id: str, max_cursor: int):
    return request_post(sec_user_id, max_cursor, get_cookie())
