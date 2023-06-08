import unittest
import requests
import certifi
import json
from src.xiaohongshu.call.call import call_cookie, call_sign

certify_pem: str = certifi.where()


class CallTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_xiaohongshu_get_data(self):
        path: str = '/api/sns/web/v1/user_posted?num=30&cursor=&user_id=5c5043f80000000011004a6d'
        headers = {
            'origin': 'https://www.xiaohongshu.com',
            'Referer': 'https://www.xiaohongshu.com/',
            'Cookie': call_cookie()['data'],
            **call_sign(path, None)['data'],
        }

        headers['X-t'] = str(headers['X-t'])

        res: requests.Response = requests.get('https://edith.xiaohongshu.com' + path,
                                              verify=certify_pem,
                                              headers=headers)
        res_json = json.loads(res.text)
        self.assertEqual(res_json['success'], True)


if __name__ == '__main__':
    unittest.main()
