from typing import Optional, Dict
from flask import request, current_app, g, Blueprint
from app.utils import NoResultFound, ResponseErrorType
from common import (get_logger, get_unix_time_tuple, getmd5, get_random_num,
                    is_phone, is_email)
from app.utils import (parse_params, session, CommonError, response_success,
                       login_require, db, redis_client, get_current_user)
from model.user import User, LoginRecordModel

api = Blueprint('user', __name__)
logger = get_logger(__name__)

# def register():
#     params = parse_params(request)

#     email: str = params.get('email')
#     password: str = params.get('password')
#     q = session.query(User).filter(User.email == email,
#                                    User.password == password)
#     exsist_user = session.query(q.exists()).scalar()
#     if exsist_user:
#         return CommonError.get_error(error_code=40200)
#     user = User(email, password=password)
#     try:
#         session.add(user)
#         session.commit()
#         payload: Dict[str, int] = {'user_id': user.id}
#         # 注册的用户，创建默认的文件夹与note
#         from tasks.user import on_user_register
#         on_user_register.delay(user.id)
#         return response_success(body=payload)
#     except Exception as e:
#         logger.error('===' + str(e))
#         return CommonError.get_error(error_code=9999)
