# -*- coding: utf-8 -*-

from typing import Dict, Any, Union, Union
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


def get_page_info() -> Union[PageInfo, None]:
    """  尝试从当前服务实例中获得附加的页面实例
    g: flask 的 g 对象
    Return:
        如果其中附加了页面实例，则返回，如果没有就返回None
    """
    from flask import g

    info = getattr(g, "pageinfo", None)
    if isinstance(info, PageInfo):
        return info
    return None
