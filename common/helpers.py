# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional
import logging
import urllib
import sys
from app import config
"""
Helper functions
"""


def parse_params(request: Any) -> Dict[str, Any]:
    """  从一个Request实例中解析params参数
    Args:
        request: flask.request 实例对象
    Return: 一个解析过的字典对象，如果没有解析出，则返回一个空的字典对象
    """
    r = request
    d: Dict[str, Any] = {}
    if r.method == "GET":
        if json := r.args or r.get_json():
            d = dict(json)

    if r.method == "POST":
        if json := r.get_json() or r.args:
            d = dict(json)

    if not d:
        d = dict(r.values)
    return d


def get_current_user() -> Any:
    """  尝试从当前服务实例中获得附加的用户实例
    g: flask 的 g 对象
    Return:
        如果其中附加了用户实例，则返回，如果没有就返回None
    """
    from flask import g

    return getattr(g, "current_user", None)


class PageInfo:
    page: int = 0
    limit: int = 11
    offset: int = 0

    def __init__(self, page: int, limit: int):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit


def get_page_info() -> Optional[PageInfo]:
    """  尝试从当前服务实例中获得附加的页面实例
    g: flask 的 g 对象
    Return:
        如果其中附加了页面实例，则返回，如果没有就返回None
    """
    from flask import g

    return getattr(g, "pageinfo", None)


loggers: Dict[str, logging.Logger] = {}


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """  获得一个logger 实例，用来打印日志
    Args:
        name: logger的名称
    Return:
        返回一个logger实例
    """
    global loggers

    if not name:
        name = __name__

    has = loggers.get(name)
    if has:
        return has

    logger = logging.getLogger(name=name)
    stream_handler = logging.StreamHandler(sys.stdout)

    logger.setLevel(config.LOG_LEVEL)
    stream_handler.setLevel(config.LOG_LEVEL)
    formatter = logging.Formatter(config.LOGGING_FORMATTER)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    loggers[name] = logger

    return logger


def parser_url_path_rule1(old: str, replace: str) -> str:

    if not old:
        return old
    if old.startswith('http'):
        return old
    ret = urllib.parse.urlparse(replace)
    _link = str(ret.scheme) + "://" + str(ret.netloc) + old

    return _link
