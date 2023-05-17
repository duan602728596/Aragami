"""
对地址的解析
"""
import re
from os import path
from urllib.parse import urlparse, ParseResult
import execjs

with open(path.dirname(__file__) + '/parser.js', 'r', encoding='utf-8') as f:
    parserJsText: str = f.read()

parserJs = execjs.compile(parserJsText)


def parse(url: str) -> map or None:
    parse_result = parserJs.call('parse', url)

    return parse_result


# 解析分享链接
def share_parse(url: str) -> map or None:
    url_parse_result: ParseResult = urlparse(url)

    if re.search(r'/share/(video|note)', url_parse_result.path):
        return parserJs.call('douyinShareVideoParse', url_parse_result.path)
    elif re.search(r'/share/user', url_parse_result.path):
        return parserJs.call('douyinShareUserParse', url_parse_result.path)
