from src.api.api import request_ttwid_cookie, request_detail
from src.api.utils import random_string


def detail(id: str):
    passport_csrf_token: str = random_string(32)
    ttwid: str = request_ttwid_cookie()
    cookie = '; '.join((
        ttwid,
        'passport_csrf_token=' + passport_csrf_token,
        'passport_csrf_token_default=' + passport_csrf_token
    ))
    return request_detail(id, cookie)
