# -*- coding: utf-8 -*-

from typing import Any, Union, Dict, Tuple
from enum import Enum
from app.utils.response import response_error


class ResponseErrorType(Enum):
    # 用户发出的请求有错误
    REQUEST_ERROR = 40000
    # 表示用户没有权限（令牌、用户名、密码错误）
    NEED_PERMISSION = 40100
    # 禁止访问
    FORBIDDEN = 40300
    # 资源不存在
    NOT_FOUND = 40400
    # 资源被永久删除
    GONE = 41000
    # 服务器错误
    UNKNOWN_ERROR = 50000


class ApiError:
    @classmethod
    def get_error(cls, error_code: int):
        pass


class CommonError(ApiError):
    @classmethod
    def get_error(
        cls,
        error_code: int = 50000,
        message: Union[str, None] = None,
        data: Any = None,
        http_code: int = 400,
        header: Union[Dict[str, str], None] = None
    ) -> Tuple[str, int, Dict[str, str]]:
        switcher: Dict[int, str] = {
            ResponseErrorType.REQUEST_ERROR.value: "请求异常",
            ResponseErrorType.NEED_PERMISSION.value: "权限异常，请检查权限",
            ResponseErrorType.FORBIDDEN.value: "禁止访问",
            ResponseErrorType.NOT_FOUND.value: "请求资源不存在",
            ResponseErrorType.UNKNOWN_ERROR.value: "未知错误"
        }
        msg: str = switcher.get(error_code) or "未知错误"
        assert msg is not None
        http_code = int(error_code / 100)
        return response_error(error_code=error_code,
                              msg=msg,
                              http_code=http_code)

    @classmethod
    def error_toast(cls,
                    type: ResponseErrorType = ResponseErrorType.REQUEST_ERROR,
                    message: str = "",
                    data: Any = None):
        assert message is not None

        error_code = type.value
        code = int(error_code / 100)
        return response_error(error_code=error_code,
                              msg=message,
                              data=data,
                              http_code=code)

    @classmethod
    def error_enum(
        cls,
        type: ResponseErrorType,
        message: Union[str, None] = None,
        data: Any = None,
        http_code: int = 400,
        header: Union[Dict[str, str], None] = None
    ) -> Tuple[str, int, Dict[str, str]]:
        return cls.get_error(type.value,
                             message=message,
                             data=data,
                             http_code=http_code,
                             header=header)
