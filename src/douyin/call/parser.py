"""
对地址的解析
"""
import re
from os import path
from urllib.parse import urlparse, ParseResult
import execjs

with open(path.dirname(__file__) + '/parser.js', 'r', encoding='utf-8') as f:
    parser_js_text: str = f.read()

parser_js = execjs.compile(parser_js_text)


def parse(url: str) -> map or None:
    parse_result = parser_js.call('parse', url)

    return parse_result


# 解析分享链接
def share_parse(url: str) -> map or None:
    url_parse_result: ParseResult = urlparse(url)

    if re.search(r'/share/(video|note)', url_parse_result.path):
        return parser_js.call('douyinShareVideoParse', url_parse_result.path)
    elif re.search(r'/share/user', url_parse_result.path):
        return parser_js.call('douyinShareUserParse', url_parse_result.path)
