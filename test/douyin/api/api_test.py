import unittest
from src.douyin.api.api import request_ttwid_cookie, request_share_url
from src.douyin.api.utils import random_string, detail_params


class ApiTest(unittest.TestCase):
    def test_ttwid_cookie(self):
        res = request_ttwid_cookie()
        self.assertEqual(isinstance(res, str), True)

    def test_share_url(self):
        res = request_share_url('https://v.douyin.com/kt5s7j4/', '')
        self.assertEqual(isinstance(res, str), True)

    def test_ms_token(self):
        token = random_string(128)
        self.assertEqual(isinstance(token, str), True)

    def test_detail_params(self):
        params = detail_params('7141964711570066722')
        self.assertEqual(isinstance(params, str), True)


if __name__ == '__main__':
    unittest.main()
