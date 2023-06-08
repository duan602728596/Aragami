import requests
import certifi

certify_pem: str = certifi.where()


def request_init(port, executable_path):
    res: requests.Response = requests.post('http://localhost:32000/api/init', json={
        'port': port,
        'executablePath': executable_path,
    }, verify=certify_pem)

    return res.json()


def request_sign(url, data):
    res: requests.Response = requests.post('http://localhost:32000/api/sign', json={
        'url': url,
        'data': data,
    }, verify=certify_pem)

    return res.json()


def request_cookie():
    res: requests.Response = requests.post('http://localhost:32000/api/cookie', json={}, verify=certify_pem)

    return res.json()
