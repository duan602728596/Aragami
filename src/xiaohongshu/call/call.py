import platform
from src.xiaohongshu.api.api import request_init, request_sign, request_cookie

if platform.system() == 'Windows':
    default_executable_path: str = 'C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe'
elif platform.system() == 'Darwin':
    default_executable_path: str = '/Applications/Microsoft Edge Dev.app/Contents/MacOS/Microsoft Edge Dev'
else:
    default_executable_path: str = ''

request_init(32050, default_executable_path)


def call_sign(url: str, data: str or None):
    return request_sign(url, data)


def call_cookie():
    return request_cookie()
