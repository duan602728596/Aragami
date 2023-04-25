"""
对地址的解析
"""
from os import path
import execjs

with open(path.dirname(__file__) + '/parser.js', 'r', encoding='utf-8') as f:
    parserJsText = f.read()

parserJs = execjs.compile(parserJsText)


def parse(url: str):
    parse_result = parserJs.call('parse', url)

    return parse_result
