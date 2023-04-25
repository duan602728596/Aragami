import unittest
import time
from src.call.call import detail, post, live_enter, call_api, call_live_api


class CallTest(unittest.TestCase):
    def detail_assert(self, data):
        self.assertEqual(data['aweme_detail']['desc'], '#闺蜜 #姐妹 陪一个女孩长大 不如陪奶奶说说心里话')

    def post_assert(self, data):
        self.assertEqual(data['aweme_list'][0]['aweme_id'], '7209619920986885432')

    def call_live_api_assert(self, url: str):
        data = call_live_api(url)
        room_status: int = data['data']['room_status']
        self.assertEqual(room_status == 0 or room_status == 2, True)

    def test_detail(self):
        self.detail_assert(detail('7141964711570066722'))

    def test_post(self):
        self.post_assert(post("MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM", int(time.time() * 1_000)))

    def test_live_enter(self):
        data = live_enter('9409272172')
        room_status: int = data['data']['room_status']
        self.assertEqual(room_status == 0 or room_status == 2, True)

    def test_call_api_detail(self):
        self.detail_assert(call_api('https://www.douyin.com/video/7141964711570066722'))
        self.detail_assert(call_api('7141964711570066722'))

    def test_call_api_post(self):
        self.post_assert(
            call_api('https://www.douyin.com/user/MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'))
        self.post_assert(call_api('MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'))

    def test_call_live_api(self):
        self.call_live_api_assert('https://live.douyin.com/9409272172')
        self.call_live_api_assert('9409272172')


if __name__ == '__main__':
    unittest.main()
