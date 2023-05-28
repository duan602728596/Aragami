import re
import platform
from os import path
from string import Template
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, Route

with open(path.dirname(__file__) + '/XiaoHongShu.js', 'r', encoding='utf-8') as f:
    xiaohongshu_js_text: str = f.read()

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


def xiaohongshu_header_route_url_callable(url: str) -> bool:
    url_parse_result = urlparse(url)

    if re.search(r'www\.xiaohongshu\.com', url_parse_result.netloc):
        return True
    else:
        return False


def xiaohongshu_header_route_handler(route: Route):
    route.fulfill(body=xiaohongshu_response_body)


def xiaohongshu_cookie_route_url_callable(url: str) -> bool:
    url_parse_result = urlparse(url)

    if re.search(r'/\.(png|j?peg|webp|avif|icon?|gif)/', url_parse_result.path):
        return True
    else:
        return False


def xiaohongshu_cookie_route_handler(route: Route):
    route.abort()


# 计算小红书的header
def xiaohongshu_header(uri: str, **kwargs):
    with sync_playwright() as playwright:
        cookies = kwargs.get('cookies')
        json = kwargs.get('json')
        executable_path = kwargs.get('executable_path') or default_executable_path

        browser = playwright.chromium.launch(executable_path=executable_path, headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.route(xiaohongshu_header_route_url_callable, xiaohongshu_header_route_handler)
        page.goto('https://www.xiaohongshu.com/user/profile/594099df82ec393174227f18', timeout=0)

        if cookies:
            for cookie in cookies:
                if not (('url' in cookie) or ('domain' in cookie)):
                    cookie['url'] = 'https://www.xiaohongshu.com/'

            context.add_cookies(cookies)

        page.wait_for_load_state('domcontentloaded', timeout=0)

        handle = page.evaluate_handle('([u, i]) => window._webmsxyw(u, i)', [uri, json or None])
        result = handle.json_value()

        page.close()
        browser.close()

        return result


# 获取小红书的cookie
def xiaohongshu_cookie(**kwargs):
    with sync_playwright() as playwright:
        executable_path = kwargs.get('executable_path') or default_executable_path

        browser = playwright.chromium.launch(executable_path=executable_path, headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.route(xiaohongshu_cookie_route_url_callable, xiaohongshu_cookie_route_handler)
        page.goto('https://www.xiaohongshu.com/user/profile/594099df82ec393174227f18', timeout=0)
        page.wait_for_selector('.user-name', timeout=0)

        cookie = context.cookies() or []
        page.close()
        browser.close()

        return cookie
