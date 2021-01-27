from typing import Union, Dict, Any, List
from flask import request, current_app, g, Blueprint
from app.utils import NoResultFound, MultipleResultsFound, ResponseErrorType, valid_require_params
from common import (get_logger, get_unix_time_tuple, getmd5, get_random_num,
                    is_phone, is_email)
from app.utils import (parse_params, session, CommonError, response_success,
                       login_require, db, redis_client, get_current_user,
                       get_token_from_request)
from model.user import User, LoginRecordModel

prefix: str = "user"
api = Blueprint(prefix, __name__)
logger = get_logger(__name__)


def register():
    params: Dict[str, Any] = parse_params(request)
    keys: List[str] = ["email", "password"]
    require_key: Union[str, None] = valid_require_params(keys, params)
    if require_key:
        return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR)

    email: str = params.get("email", "")
    password: str = params.get("password", "")
    nickname: Union[str, None] = params.get("nickname")
    phone: Union[str, None] = params.get("phone")
    description: Union[str, None] = params.get("description")
    sex: int = int(params.get("sex") or 0)

    query = db.session.query(User).filter_by(email=email)
    is_exisit: bool = db.session.query(query.exists()).scalar()
    if is_exisit:
        return CommonError.error_toast(ResponseErrorType.EXISIT,
                                       message="该邮箱已经被注册了")

    # 设置种子
    # 邮箱+密码+5位随机数
    seed: str = email + password + get_random_num(5)
    # 生成唯一标识符
    identifier: str = getmd5(seed)
    user = User(
        email=email,
        identifier=identifier,
        sex=sex,
        phone=phone,
        nickname=nickname,
        password=password,
        # 注册阶段token可以没有
        token=None,
        description=description)
    user.save(commit=True)

    payload: Dict[str, Any] = {}
    payload.setdefault("id", user.id)
    return response_success(body=payload)


def login():
    params: Dict[str, Any] = parse_params(request)
    keys: List[str] = ["email", "password"]
    require_key: Union[str, None] = valid_require_params(keys, params)
    if require_key:
        return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR)

    email: str = params.get("email", "")
    password: str = params.get("password", "")
    try:
        exsist_user: User = session.query(User).filter_by(
            email=email, password=password).one()
        login_time: str = get_unix_time_tuple()
        log_ip: str = request.args.get('user_ip') or request.remote_addr
        record: LoginRecordModel = LoginRecordModel(exsist_user.id, log_ip)
        db.session.add(record)

        # update token
        token: str = exsist_user.get_token()
        exsist_user.token = token
        db.session.add(record)
        db.session.commit()
        payload: Dict[str, Any] = exsist_user.info_dict
        payload.setdefault('token', token)
        return response_success(body=payload)
    except NoResultFound:
        return CommonError.error_enum(ResponseErrorType.NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return CommonError.error_enum(ResponseErrorType.UNKNOWN_ERROR)


@login_require
def user_info():
    '''
    获得用户基本信息 
    需要登录权限
    '''
    logger.info("user_info")
    params = parse_params(request)
    user: User = get_current_user()
    payload: Dict[str, Any] = user.info_dict
    return response_success(body=payload)


@login_require
def logout():
    '''
    登出
    设置redis时间为过期
    '''
    params = parse_params(request)
    token = get_token_from_request(request)
    if token:
        redis_client.client.delete(cache_key, token)
    user: User = get_current_user()
    cache_key: str = user.get_cache_key
    user.status = 3
    user.token = ''
    db.session.commit()
    return response_success(body={})


@login_require
def modify_user_info():
    params = parse_params(request)
    user: User = get_current_user()
    # 用户昵称
    nickname = params.get('nickname')
    phone = params.get('phone')
    sex = int(params.get('sex') or 0)
    email = params.get('email')
    logger.info(params)
    if nickname:
        user.nickname = nickname
    if phone:
        if is_phone(str(phone)) and len(phone) == 11:
            user.mobilephone = phone
        else:
            return CommonError.error_toast(message='手机号码格式错误')
    if sex:
        if sex in (1, 0):
            user.sex = sex
        else:
            return CommonError.error_toast(message='性别设置错误')
    if email and not user.email:
        if is_email(email):
            user.email = email
        else:
            return CommonError.error_toast(message='邮箱格式错误')
    user.save(commit=True)
    payload: Dict[str, Any] = user.info_dict
    return response_success(body=payload)


def setup_urls(api: Blueprint):
    api.add_url_rule("/register", view_func=register, methods=["POST"])
    # 登录
    api.add_url_rule('/login', view_func=login, methods=['POST'])
    # 修改信息
    api.add_url_rule('/modify_info',
                     view_func=modify_user_info,
                     methods=['POST'])
    # 获得用户信息
    api.add_url_rule('/info', view_func=user_info, methods=['GET'])
    # 用户登出
    api.add_url_rule('/logout', view_func=logout, methods=['GET', 'POST'])


setup_urls(api)