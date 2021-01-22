# -*- coding: utf-8 -*-

import hashlib
import random
import datetime
import time
import re
from .regex import is_emoji
from typing import Dict, List, Optional


def get_unix_time_tuple(date: Optional[datetime.datetime] = None,
                        millisecond: bool = False) -> str:
    """ get time tuple

    get unix time tuple, default `date` is current time

    Args:
        date: datetime, default is datetime.datetime.now()
        millisecond: if True, Use random three digits instead of milliseconds

    Return:
        a str type value, return unix time of incoming time
    """
    if not date:
        date = datetime.datetime.now()
    time_tuple = time.mktime(date.timetuple())
    time_tuple = round(time_tuple * 1000) if millisecond else time_tuple
    second = str(int(time_tuple))
    return second


def get_date_from_time_tuple(unix_time: Optional[str] = None,
                             formatter: str = '%Y-%m-%d %H:%M:%S') -> str:
    """ translate unix time tuple to time

    get time from unix time

    Args:
        unix_time: unix time tuple
        formatter: str time formatter

    Return:
        a time type value, return time of incoming unix_time
    """
    if not unix_time:
        unix_time = get_unix_time_tuple()

    if len(unix_time) == 13:
        unix_time = str(float(unix_time) / 1000)
    t = int(unix_time)
    time_locol = time.localtime(t)
    return time.strftime(formatter, time_locol)


def getmd5(code: str) -> str:
    """ return md5 value of incoming code

    get md5 from code

    Args:
        code: str value

    Return:
        return md5 value of code
    """

    md5string = hashlib.md5(code.encode('utf-8'))
    return md5string.hexdigest()


def get_random_num(digit: int = 6) -> str:
    """ get a random num

    get random num

    Args:
        digit: digit of the random num, limit (1, 32)

    Return:
        return Generated random num
    """
    if digit is None:
        digit = 1
    digit = min(max(digit, 1), 32)  # 最大支持32位
    result = ""
    while len(result) < digit:
        append = str(random.randint(1, 9))
        result = result + append
    return result


def contain_emoji(content: str) -> bool:
    """ judge str contain emoji str

    Args: str type

    Return : Bool type, return True if contain Emoji, else False
    """
    for c in content:
        if is_emoji(c):
            return True
    return False


def get_domain(url: str) -> str:
    """ get domain from url by given

    Args: str type
    Return: str type, return domain if can get
    """
    from urllib.parse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def filter_all_img_src(content: str) -> List[str]:
    replace_pattern = r'<[img|IMG].*?>'  # img标签的正则式
    img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式
    img_url_list = []
    need_replace_list = re.findall(replace_pattern, content)  # 找到所有的img标签
    for tag in need_replace_list:
        imgs = re.findall(img_url_pattern, tag)
        if imgs:
            img_url_list.append(imgs[0])  # 找到所有的img_url
    return img_url_list


UA_LIST: List[str] = [
    ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
     ),
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

FAKE_HEADER: Dict[str, str] = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa
    "Accept-Charset":
    "UTF-8,*;q=0.5",
    "Accept-Encoding":
    "gzip,deflate,sdch",
    "Accept-Language":
    "en-US,en;q=0.8",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",  # noqa
}


def get_header() -> Dict[str, str]:
    new_ = FAKE_HEADER.copy()
    new_["User-Agent"] = random.choice(UA_LIST)
    new_.setdefault("Accept", "*/*")
    new_.setdefault("Accept-Encoding", 'gzip, deflate, br')
    new_.setdefault("Connection", "keep-alive")
    return new_
