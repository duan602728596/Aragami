"""
对url的解析
"""
from urllib.parse import urlparse, parse_qs
import re
from typing import Optional


# 解析结果
class ParseInfo:
    def __init__(self, p_type: str, p_id: str):
        self.p_type = p_type
        self.p_id = p_id


douyin_regexp = r'www\.douyin\.com'             # 抖音域名
douyin_video_regexp = r'\/(video|note)\/[0-9]+' # 抖音视频
douyin_video_match_regexp = r'(?<=/video/)\d+'  # 提取视频ID
video_id_regexp = r'^[0-9]+$'                   # 纯数字，视频id


# 提取视频ID
def get_video_id(path: str) -> Optional[str]:
    match = re.search(douyin_video_match_regexp, path, flags=re.I)

    if match:
        return match.group()


# 解析抖音地址
def parser(url: str):
    url_parse_result = urlparse(url)

    # 判断为是合法的url
    if url_parse_result.scheme == 'http' or url_parse_result.scheme == 'https':
        query = parse_qs(url_parse_result.query)

        # 有modal_id，判断为视频
        if 'modal_id' in query:
            return ParseInfo('video', query['modal_id'][0])

        # 判断是否为抖音域名且为视频
        elif re.search(douyin_regexp, url_parse_result.netloc, flags=re.I) \
                and re.search(douyin_video_regexp, url_parse_result.path, flags=re.I):
            video_id = get_video_id(url_parse_result.path)

            if video_id:
                return ParseInfo('video', video_id)

    # 不是url
    else:
        if re.search(video_id_regexp, url, flags=re.I):
            p_type = 'video'
        else:
            p_type = 'user'

        return ParseInfo(p_type, url)
