import unittest
import time
from src.call.call import detail, post


class CallTest(unittest.TestCase):
    def test_detail(self):
        data = detail('7141964711570066722')
        self.assertEqual(data['aweme_detail']['desc'], '#闺蜜 #姐妹 陪一个女孩长大 不如陪奶奶说说心里话')

    def test_post(self):
        data = post("MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM", int(time.time() * 1_000))
        self.assertEqual(data['aweme_list'][0]['aweme_id'], '7209619920986885432')


if __name__ == '__main__':
    unittest.main()
