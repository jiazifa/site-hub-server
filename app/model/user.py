from typing import Any, Dict, Union

from flask import session
from flask_login import UserMixin
from sqlalchemy import INTEGER, SMALLINT, TEXT, Column, Sequence, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from app.extensions import db, login_manager
from app.utils import get_user_from_request_if_could

from .base import BaseModel


class User(db.Model, UserMixin, BaseModel):

    user_id = Column(INTEGER, primary_key=True)
    identifier = Column(String(64), unique=True)
    nickname = Column(String(64), nullable=True)
    password = Column(String(255), nullable=True)
    status = Column(SMALLINT, default=0)  # 用户状态
    # 用本地的 token ，用来重新获得请求 token 的 token
    token = Column(String(64), nullable=True)
    role_id = Column(INTEGER, nullable=True)

    def __init__(self,
                 identifier: Union[None, str] = None,
                 password: Union[None, str] = None,
                 nickname: Union[None, str] = None):
        self.identifier = identifier
        self.password = password
        self.nickname = nickname
        self.status = 0
        self.token = None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self) -> int:
        return self.user_id

    @staticmethod
    def create_user(identifier: str, password: str) -> 'User':
        user = User(identifier=identifier, password=password)
        user.role_id = RoleModel.default_role().role_id
        return user

    @staticmethod
    def get_user(uid: Union[None, int] = None,
                 identifier: Union[None, str] = None,
                 token: Union[None, str] = None) -> Union[None, 'User']:
        condition: Dict[str, Any] = {}
        if uid:
            condition.setdefault("user_id", uid)
        elif identifier:
            condition.setdefault("identifier", identifier)
        elif token:
            condition.setdefault("token", token)
        return User.query.filter_by(**condition).first()

    def get_info(self, want_token: bool = False) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        payload.setdefault("user_id", self.user_id)
        payload.setdefault("identifier", self.identifier)
        payload.setdefault("nickname", self.nickname)
        if want_token:
            payload.setdefault("token", self.token)
        return payload

    def get_role(self) -> 'RoleModel':
        return RoleModel.query.get(self.role_id)


class Permission():
    READ_ONLY = 0x00_00_00
    ADMIN = 0x11_11_11


class RoleModel(db.Model, BaseModel):
    """ 角色表 """
    __tablename__ = "role"

    role_id = Column(INTEGER,
                     Sequence(start=1, increment=1, name="role_id_sep"),
                     primary_key=True,
                     autoincrement=True)
    permission_scrop = Column(INTEGER,
                              nullable=False,
                              default=0,
                              comment="用户的权限")
    description = Column(String(255), nullable=False, comment="角色的描述")

    @staticmethod
    def default_role() -> 'RoleModel':
        return RoleModel.query.filter(
            RoleModel.permission_scrop == Permission.READ_ONLY).first()

    @staticmethod
    def admin_role() -> 'RoleModel':
        return RoleModel.query.filter(
            RoleModel.permission_scrop == Permission.ADMIN).first()
    
    @property
    def is_admin(self) -> bool:
        return self.permission_scrop == Permission.ADMIN


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(uid=user_id)


@login_manager.request_loader
def load_user_from_request_if_could(request: Any) -> Union[None, 'User']:
    return get_user_from_request_if_could()
    