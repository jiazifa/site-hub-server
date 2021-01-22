from typing import Union, Dict, Any
from flask import request, current_app, g, Blueprint
from app.utils import NoResultFound, ResponseErrorType, valid_require_params
from common import (get_logger, get_unix_time_tuple, getmd5, get_random_num,
                    is_phone, is_email)
from app.utils import (parse_params, session, CommonError, response_success,
                       login_require, db, redis_client, get_current_user)
from model.user import User, LoginRecordModel

api = Blueprint('user', __name__)
logger = get_logger(__name__)


def register():
    params: Dict[str, Any] = parse_params(request)
    keys: list[str] = ["email", "password"]
    require_key: str = valid_require_params(keys, params)
    if require_key:
        return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR)

    email: str = params.get("email")
    password: str = params.get("password")
    nickname: Union[str, None] = params.get("nickname")
    phone: Union[str, None] = params.get("phone")
    description: Union[str, None] = params.get("description")
    sex: Union[int, None] = int(params.get("sex")) or 0

    # 设置种子
    # 邮箱+密码+5位随机数
    seed: str = email + password + get_random_num(5)
    # 生成唯一标识符
    identifier: str = getmd5(seed)
    user: User = User(email=email,
                identifier=identifier,
                sex=sex,
                phone=phone,
                nickname=nickname,
                password=password,
                # 注册阶段token可以没有
                token=None,
                description=description)
    session.add(user)
    session.commit()

    payload: Dict[str, Any] = {}
    payload.setdefault("id", user.id)
    return response_success(body=payload)
