"""
计算X-Bogus
"""
from os import path
import execjs


with open(path.dirname(__file__) + '/Signer.js', 'r', encoding='utf-8') as f:
    SignerJsText = f.read()

SignerJs = execjs.compile(SignerJsText)


def sign(query_string: str, user_agent: str) -> str:
    return SignerJs.call('sign', query_string, user_agent)
