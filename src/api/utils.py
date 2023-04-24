import random
from urllib import parse
from src.singer.singer import sign

CHARACTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
NUMBER: str = "1234567890"
USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52"


def random_string(length: int) -> str:
    return "".join(random.choice(CHARACTERS) for _ in range(length))


def random_number(length: int) -> str:
    return "".join(random.choice(NUMBER) for _ in range(length))


# 创建details query
def detail_params(id: str) -> str:
    search_params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "aweme_id": id,
        "pc_client_type": "1",
        "version_code": "190500",
        "version_name": "19.5.0",
        "cookie_enabled": "true",
        "screen_width": "1440",
        "screen_height": "900",
        "browser_language": "zh-CN",
        "browser_platform": "MacIntel",
        "browser_name": "Edge",
        "browser_version": "110.0.1587.69",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "110.0.0.0",
        "os_name": "Mac+OS",
        "os_version": "10.15.7",
        "cpu_core_num": "4",
        "device_memory": "8",
        "platform": "PC",
        "downlink": '3.6',
        "effective_type": '4g',
        "round_trip_time": '100',
        "webid": random_number(30),
        "msToken": random_string(128),
        "_signature": "_" + random_string(20)
    }
    search_params["X-Bogus"] = sign(parse.urlencode(search_params), USER_AGENT)

    return parse.urlencode(search_params)
