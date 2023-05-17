import re
import time
import platform
from os import path
from string import Template
from urllib.parse import urlparse
from pyquery import PyQuery as pq
from playwright.sync_api import sync_playwright, Route, Request
from src.api.api import request_ttwid_cookie, request_detail, request_post, request_live_enter, request_share_url
from src.api.utils import random_string
from src.call.parser import parse, share_parse

with open(path.dirname(__file__) + '/XiaoHongShu.js', 'r', encoding='utf-8') as f:
    xiaohongshu_js_text: str = f.read()


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
def detail(aweme_id: str) -> map or None:
    return request_detail(aweme_id, get_cookie())


# 请求user的信息
def post(sec_user_id: str, max_cursor: int) -> map or None:
    return request_post(sec_user_id, max_cursor, get_cookie())


# 请求直播的信息
def live_enter(live_id: str) -> map or None:
    return request_live_enter(live_id, get_cookie())


# 请求分享链接
def share_url(url: str) -> str:
    return request_share_url(url, get_cookie())


# 输入url，返回对应的信息
def call_api(url: str, **kwargs) -> map or None:
    url_parse_result = urlparse(url)
    parse_result = None

    # 处理分享链接
    if url_parse_result.scheme == 'http' or url_parse_result.scheme == 'https':
        if re.search(r'v\.douyin\.com', url_parse_result.netloc):
            share_res = share_url(url)
            pq_html = pq(share_res)
            parse_result = share_parse(pq_html('a').attr('href'))

    if not parse_result:
        parse_result = parse(url)

    max_cursor = kwargs.get('max_cursor') or int(time.time() * 1_000)

    if not parse_result:
        return None

    if parse_result['type'] == 'video':
        return detail(parse_result['id'])

    elif parse_result['type'] == 'user':
        return post(parse_result['id'], max_cursor)


# 输入直播url，返回对应的信息
def call_live_api(url: str) -> map or None:
    url_parse_result = urlparse(url)

    if url_parse_result.scheme == 'http' or url_parse_result.scheme == 'https':
        if re.search(r'live\.douyin\.com', url_parse_result.netloc):
            live_id_match = re.findall(r'\d+', url_parse_result.path)

            if len(live_id_match) > 0:
                return live_enter(live_id_match[0])
            else:
                return None
    else:
        if re.search(r'^\d+$', url):
            return live_enter(url)


# 小红书
xiaohongshu_response_body: str = Template("""<html>
<head>
  <meta charset="utf8">
</head>
<body>
  <script> $scripts </script>
</body>
</html>""").substitute(scripts=xiaohongshu_js_text)

if platform.system() == 'Windows':
    default_executable_path: str = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
elif platform.system() == 'Darwin':
    default_executable_path: str = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'


def xiaohongshu_route_url_callable(url: str) -> bool:
    url_parse_result = urlparse(url)

    if re.search(r'www\.xiaohongshu\.com', url_parse_result.netloc):
        return True
    else:
        return False


def xiaohongshu_route_handler(route: Route, request: Request):
    route.fulfill(body=xiaohongshu_response_body)


# 计算小红书的header
def xiaohongshu_header(uri: str, **kwargs):
    with sync_playwright() as playwright:
        cookies = kwargs.get('cookies')
        json = kwargs.get('json')

        browser = playwright.chromium.launch(
            executable_path=kwargs.get('executable_path') or default_executable_path, headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.route(xiaohongshu_route_url_callable, xiaohongshu_route_handler)
        page.goto('https://www.xiaohongshu.com/user/profile/594099df82ec393174227f18', timeout=0)

        if cookies:
            for cookie in cookies:
                if not 'url' in cookie:
                    cookie['url'] = 'https://www.xiaohongshu.com/'

            context.add_cookies(cookies)

        page.wait_for_load_state('domcontentloaded', timeout=0)

        handle = page.evaluate_handle('([u, i]) => window._webmsxyw(u, i)', [uri, json or None])
        result = handle.json_value()

        page.close()
        browser.close()

        return result
