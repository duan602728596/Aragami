"""
请求API时使用的一些通用方法
"""
from os import path
from urllib.parse import urlencode
import random
import execjs

# 加载js文件
with open(path.dirname(__file__) + '/Signer.js', 'r', encoding='utf-8') as f:
    SignerJsText: str = f.read()

SignerJs = execjs.compile(SignerJsText)

CHARACTERS: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
NUMBER: str = '1234567890'
USER_AGENT: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52'
DOUYIN_USER_AGENT: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'


# 计算X-Bogus
def sign(query_string: str, user_agent: str) -> str:
    return SignerJs.call('sign', query_string, user_agent)


# 随机字符串
def random_string(length: int) -> str:
    return ''.join(random.choice(CHARACTERS) for _ in range(length))


# 随机数字字符串
def random_number(length: int) -> str:
    return ''.join(random.choice(NUMBER) for _ in range(length))


system_info_params = {
    'device_platform': 'webapp',
    'aid': '6383',
    'channel': 'channel_pc_web',
    'pc_client_type': '1',
    'version_code': '170400',
    'version_name': '17.4.0',
    'cookie_enabled': 'true',
    'screen_width': '1440',
    'screen_height': '900',
    'browser_language': 'zh-CN',
    'browser_platform': 'Win32',
    'browser_name': 'Edge',
    'browser_version': '113.0.1774.57',
    'browser_online': 'true',
    'engine_name': 'Blink',
    'engine_version': '113.0.0.0',
    'os_name': 'Windows',
    'os_version': '10',
    'cpu_core_num': '4',
    'device_memory': '8',
    'platform': 'PC',
    'downlink': '10',
     'effective_type': '4g',
     'round_trip_time': '100',
}


# 创建details params
def detail_params(aweme_id: str) -> str:
    search_params = {
        'aweme_id': aweme_id,
        **system_info_params,
        'webid': random_number(30),
        'msToken': random_string(128),
        '_signature': '_' + random_string(20)
    }

    search_params['X-Bogus'] = sign(urlencode(search_params), DOUYIN_USER_AGENT)

    return urlencode(search_params)


# 创建post params
def post_params(sec_user_id: str, max_cursor: int) -> str:
    search_params = {
        'sec_user_id': sec_user_id,
        'max_cursor': max_cursor,
        'locate_query': 'false',
        'show_live_replay_strategy': '1',
        'count': '30',
        'publish_video_strategy_type': '2',
        **system_info_params,
        'webid': random_number(30),
        'msToken': random_string(128),
    }
    search_params['X-Bogus'] = sign(urlencode(search_params), DOUYIN_USER_AGENT)

    return urlencode(search_params)


# 创建live params
def live_params(live_id: str) -> str:
    search_params = {
        'aid': '6383',
        'device_platform': 'web',
        'web_rid': live_id,
        'msToken': random_string(128),
    }
    search_params['X-Bogus'] = sign(urlencode(search_params), USER_AGENT)

    return urlencode(search_params)
