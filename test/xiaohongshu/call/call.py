import unittest
import requests
import certifi
import json
from src.xiaohongshu.call.call import xiaohongshu_header, xiaohongshu_cookie

certify_pem: str = certifi.where()


class CallTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xiaohongshu_cookies = [
            {
                'name': 'a1',
                'value': '188293a128980yj74fx4bior8rgkmagz1hvae47ot7350000155545',
            },
            {
                'name': 'web_session',
                'value': '030037a357fd6b55f18753ef1c234a7be23742',
            },
        ]

    def test_xiaohongshu_get_header(self):
        headers = xiaohongshu_header('/api/sns/web/v1/user_posted?num=30&cursor=&user_id=594099df82ec393174227f18',
                                     cookies=self.xiaohongshu_cookies)
        self.assertEqual(isinstance(headers['X-s'], str), True)
        self.assertEqual(isinstance(headers['X-t'], int), True)

    def test_xiaohongshu_post_header(self):
        headers = xiaohongshu_header('/api/sns/web/v1/feed',
                                     cookies=self.xiaohongshu_cookies,
                                     json={'source_note_id': '643df5670000000013003189'})
        self.assertEqual(isinstance(headers['X-s'], str), True)
        self.assertEqual(isinstance(headers['X-t'], int), True)

    def test_xiaohongshu_get_cookie(self):
        cookie = xiaohongshu_cookie()
        self.assertEqual(isinstance(cookie, list), True)

    def test_xiaohongshu_get_data(self):
        cookie = xiaohongshu_cookie()
        cookie_str: str = ''

        for cookie_item in cookie:
            cookie_str += cookie_item['name'] + '=' + cookie_item['value'] + ';'

        path: str = '/api/sns/web/v1/user_posted?num=30&cursor=&user_id=5c5043f80000000011004a6d'
        headers = xiaohongshu_header(path, cookies=cookie)
        res: requests.Response = requests.get('https://edith.xiaohongshu.com' + path,
                                              verify=certify_pem,
                                              headers={
                                                  'origin': 'https://www.xiaohongshu.com',
                                                  'Referer': 'https://www.xiaohongshu.com/',
                                                  'Cookie': cookie_str
                                              }.update(headers))
        res_json = json.loads(res.text)
        self.assertEqual(res_json['success'], True)


if __name__ == '__main__':
    unittest.main()
