# -*- coding: utf-8 -*-

import json
from enum import Enum
from typing import Any, Dict, List, Tuple, Union

from flask import request
from werkzeug.exceptions import HTTPException

from app.utils.response import response_error


class APIException(HTTPException):

    code = 500

    message: Union[str, None] = "sr, we make a mistake"

    toast: Union[str, None] = None

    error_code: Union[int, None] = 99999

    unique_data: Any = None

    def __init__(self,
                 code: Union[int, None] = None,
                 message: Union[str, None] = None,
                 toast: Union[str, None] = None,
                 error_code: Union[int, None] = None,
                 unique_data: Any = None):
        if code:
            self.code = code
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if unique_data:
            self.unique_data = unique_data
        if toast:
            self.toast = toast

        super(APIException, self).__init__(message, None)

    def get_body(self, environ=None, scope: Union[dict, None] = None) -> str:
        body = dict(
            message=self.message or "",
            error_code=self.error_code or 50000,
            method=request.method,
            path=APIException._get_path_without_query(),
        )
        if self.unique_data:
            body.setdefault("data", self.unique_data)
        if self.toast:
            body.setdefault("toast", self.toast)
        text = json.dumps(body)
        return text

    def get_headers(self,
                    environ=None,
                    scope: Union[dict, None] = None) -> List[Tuple[str, str]]:
        return [('Content-Type', 'application/json')]

    @staticmethod
    def _get_path_without_query() -> str:
        full_url: str = str(request.full_path)
        path = full_url.split('?')
        return path[0]


#  请求错误
class ParameterException(APIException):
    # 用户请求的参数错误
    code = 400
    message = "参数错误"
    error_code = 40001


class PermissionException(APIException):
    # 缺少权限
    code = 401
    message = "权限不足"
    error_code = 40100


class ForbidenException(APIException):
    # 禁止访问
    code = 403
    message = "禁止访问"
    error_code = 40300


class NotFoundExeception(APIException):
    # 资源未发现
    code = 404
    message = "资源不存在或未找到"
    error_code = 40400

class ConflictExeception(APIException):
    # 冲突
    code = 409
    message = "由于冲突，请求无法被完成"
    error_code = 40900

class GoneExeception(APIException):
    # 资源被永久删除
    code = 410
    message = "请求资源不存在"
    error_code = 41000


class UnknownExeception(APIException):
    # 服务器未知错误
    ...