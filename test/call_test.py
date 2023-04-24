import unittest
from src.call.call import detail


class CallTest(unittest.TestCase):
    def test_detail(self):
        data = detail('7141964711570066722')
        self.assertEqual(data['aweme_detail']['desc'], '#闺蜜 #姐妹 陪一个女孩长大 不如陪奶奶说说心里话')


if __name__ == '__main__':
    unittest.main()
