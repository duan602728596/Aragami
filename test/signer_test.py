import unittest
from src.singer.singer import sign


class SingerTest(unittest.TestCase):
    def test_sign(self):
        sign_result: str = sign('a=5&b=6', '')
        self.assertEqual(isinstance(sign_result, str), True)


if __name__ == '__main__':
    unittest.main()
