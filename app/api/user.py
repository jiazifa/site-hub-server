from typing import Any, Dict, List, Union

from flask import Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Length

from app import config
from app.extensions import (FlaskAPIForm, MultipleResultsFound, NoResultFound,
                            db, login_manager)
from app.model.user import User
from app.utils import response_success, parse_params_from_request, get_logger
from app.utils.errors import (ConflictExeception, NotFoundExeception,
                              ParameterException, UnknownExeception)
from common import get_random_num, getmd5

logger = get_logger(__name__)

prefix: str = "user"
api: Blueprint = Blueprint(prefix, __name__)


class _RegisterForm(FlaskAPIForm):
    name = StringField('name',
                       validators=[DataRequired(),
                                   Length(min=3, max=11)])
    password = StringField('password', validators=[DataRequired()])


@api.post("/register/")
def register():
    register_form = _RegisterForm()
    if not register_form.validate():
        raise ParameterException(unique_data=register_form.errors)
    name = register_form.name.data
    password = register_form.password.data
    user = User.create_user(name, password)
    if User.get_user(identifier=name):
        raise ConflictExeception(toast="用户已经存在")
    user.save(commit=True)
    payload: Dict[str, Any] = {}
    payload = user.get_info()
    return response_success(body=payload)


@api.post("/login/")
def login():
    login_form = _RegisterForm()
    if not login_form.validate():
        raise ParameterException(unique_data=register_form.errors)
    user: Union[None,
                User] = User.query.filter_by(
                    identifier=login_form.name.data,
                    password=login_form.password.data).first()
    if not user:
        raise NotFoundExeception(message="user not found")
    result: bool = login_user(user)
    if not result:
        raise UnknownExeception(message="login failed")
    salt: str = config.SECRET_KEY or "token"
    token = getmd5("{}{}{}".format(salt, user.identifier, get_random_num(5)))
    user.token = token
    user.save(commit=True)
    payload: Dict[str, Any] = {}
    payload = user.get_info(want_token=True)
    return response_success(body=payload)


class _UpdateForm(FlaskAPIForm):
    uid = IntegerField('uid', validators=[DataRequired()])
    nickname = StringField('nickname')


@api.post("/update_info/")
@login_required
def update_info():
    form = _UpdateForm()
    if not form.validate():
        return ParameterException(message=form.errors)
    uid = form.uid.data
    user = User.query.get(uid)
    if not user:
        return NotFoundExeception()
    if nickname := form.nickname.data:
        user.nickname = nickname
    user.save(commit=True)
    payload = user.get_info()
    return response_success(body=payload)


@api.post("/logout/")
def logout():
    logout_user()
    return response_success()


@api.get("/info/")
@login_required
def user_info():
    user: User = current_user
    payload: Dict[str, Any] = user.get_info()
    return response_success(body=payload)


def setup_urls(api: Blueprint):
    ...


setup_urls(api)