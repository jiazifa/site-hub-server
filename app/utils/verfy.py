# -*- coding: utf-8 -*-

from typing import Union, Any, Callable, Tuple, Dict, List
from functools import wraps
from flask import request, Request, g, current_app, session
from app.utils import (CommonError, ResponseErrorType, redis_client, db,
                       parse_params, PageInfo)
from common import get_date_from_time_tuple, getmd5, get_logger
from model.user import User

logger = get_logger(__name__)


def login_require(func: Callable):
    """
    检测登录权限
    在执行 func 之前，会检查权限
    :param func:  被执行的 router_func
    """
    @wraps(func)
    def decorator_view(*args, **kwargs):
        user_or_error: any = get_user_from_request(request, True)
        if not user_or_error:
            return CommonError.error_enum(ResponseErrorType.NEED_PERMISSION)
        # if not matched_encryption(request):
        #     return CommonError.error_enum(ResponseErrorType.NEED_PERMISSION)
        if isinstance(user_or_error, User):
            g.current_user = user_or_error
        else:
            return user_or_error
        return func(*args, **kwargs)

    return decorator_view


def get_token_from_request(request: Request) -> Union[str, None]:
    params = parse_params(request)
    alice: str = "token"
    token: Union[str, None] = params.get(alice)
    if not token:
        token = session.get(alice) or request.cookies.get(alice)
    if not token:
        token = request.headers.get(alice)
    return token


def get_user_from_request(
    request: Request, is_force: bool
) -> Union[Union["User", None], Tuple[str, int, Dict[str, str]]]:
    """  尝试从请求中获得用户
    Args:
        request: 一个请求的实例
        is_force: 是否是强制需要用户信息， 如果是强制的，在没有获得用户的时候会返回一个错误报文
    Return: 获得的用户实例，如果根据信息无法获得用户实例，则返回 None
    """
    token: Union[str, None] = get_token_from_request(request)
    if not token and is_force:
        return CommonError.error_enum(ResponseErrorType.NEED_PERMISSION)
    if not token:
        return None

    user_id: str = str(redis_client.client.get(token) or b"", encoding="utf8")
    identifier = user_id.replace("sky_user_cache_key_", "")
    if user := User.get_user(token=token):
        logger.info("user id ::" + str(user.id or None) +
                    " loging with token:: " + str(token))
        return user
    return None


def pages_info_requires(func):
    """ 页面信息请求；分页等 """
    @wraps(func)
    def decorator_view(*args, **kwargs):
        params = parse_params(request)
        pages: int = int(params.get("page") or 1)
        limit: int = int(params.get("limit") or 11)
        info: PageInfo = PageInfo(max(pages, 1), max(limit, 1))
        g.pageinfo = info
        return func(*args, **kwargs)

    return decorator_view


def matched_encryption(request: Any) -> bool:
    if current_app.is_testing:
        return current_app.is_testing
    header: Dict[str, str] = dict(request.headers)
    target: str = header.get("V") or ''

    params: Dict[str, Any] = parse_params(request)
    noices: str = ""

    if token := get_token_from_request(request):
        noices += token

        if user := User.get_user(token=token):
            noices += str(user.id)

    sorted_params_keys: str = "".join(sorted(params.keys()))
    date_minute: str = get_date_from_time_tuple(formatter="%Y%m%d%H%M")

    code: str = "{}:{}:{}".format(noices, sorted_params_keys, date_minute)
    logger.info("{}".format(code))
    if not target:
        return False
    full_md5 = getmd5(code)
    if full_md5:
        return full_md5.startswith(target)
    return True


def valid_require_params(keys: List[str],
                         params: Dict[str, Any]) -> Union[str, None]:
    """
    验证必要参数
    keys: 必须的参数
    params: 请求的参数
    Return:
        如果缺失了参数，会将缺失的参数返回
    """
    for k in keys:
        if k not in params:
            return k
    return None