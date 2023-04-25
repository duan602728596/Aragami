"""
对地址的解析
"""
import re
from os import path
from urllib.parse import urlparse
import execjs

with open(path.dirname(__file__) + '/parser.js', 'r', encoding='utf-8') as f:
    parserJsText = f.read()

parserJs = execjs.compile(parserJsText)


def parse(url: str):
    parse_result = parserJs.call('parse', url)

    return parse_result


# 解析分享链接
def share_parse(url: str):
    url_parse_result = urlparse(url)

    if re.search(r'/share/(video|note)', url_parse_result.path):
        return parserJs.call('douyinShareVideoParse', url_parse_result.path)
    elif re.search(r'/share/user', url_parse_result.path):
        return parserJs.call('douyinShareUserParse', url_parse_result.path)
