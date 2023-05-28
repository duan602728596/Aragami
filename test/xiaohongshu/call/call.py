import unittest
from src.xiaohongshu.call.call import xiaohongshu_header


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


if __name__ == '__main__':
    unittest.main()
