import unittest
from src.call.parser import parse


class ParserTest(unittest.TestCase):
    def parse_assert_equal(self, parse_result, p_type, p_id):
        self.assertEqual(parse_result['type'], p_type)
        self.assertEqual(parse_result['id'], p_id)

    def parse_assert_equal_none(self, parse_result):
        self.assertEqual(parse_result, None)

    def test_parse(self):
        # 视频或图文
        self.parse_assert_equal(
            parse('https://www.douyin.com/user/MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'
                  '?modal_id=7184782545546939709'), 'video', '7184782545546939709')
        self.parse_assert_equal(
            parse('https://www.douyin.com/video/7141964711570066722'), 'video', '7141964711570066722')
        self.parse_assert_equal(parse('7184782545546939709'), 'video', '7184782545546939709')
        self.parse_assert_equal(
            parse('https://www.douyin.com/note/7160299412965657888'), 'video', '7160299412965657888')

        # 用户
        self.parse_assert_equal(
            parse('https://www.douyin.com/user/MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'),
            'user', 'MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM')
        self.parse_assert_equal(parse('MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'),
                                'user', 'MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM')



if __name__ == '__main__':
    unittest.main()
