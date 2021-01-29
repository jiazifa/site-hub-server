from typing import Union, List, Dict, Any
from datetime import datetime
from sqlalchemy import Column, String, SMALLINT, TEXT, INTEGER, Sequence
from common import get_random_num, getmd5, get_unix_time_tuple
from app.utils import db
from model.base import BaseModel
from model.permission import Role, RoleType


class User(db.Model, BaseModel):
    id = Column(INTEGER, primary_key=True)
    identifier = Column(String(64), nullable=True, comment="用户的唯一标识符")
    sex = Column(SMALLINT, nullable=True, default=0, comment="0 未设置 1 男性 2 女性")
    phone = Column(String(11), nullable=True, comment="手机号")
    nickname = Column(String(18), nullable=True, comment="用户昵称")
    email = Column(String(64), nullable=True, unique=True)
    description = Column(String(64), nullable=True, comment="个人简介")
    password = Column(String(64), nullable=True)
    token = Column(String(64), nullable=True)
    role = Column(INTEGER, nullable=True, comment="分配的权限角色类型")
    status = Column(SMALLINT,
                    nullable=True,
                    default=1,
                    comment="0 未激活 1 正常 2 异常 3 注销")

    def __init__(self,
                 email: Union[str, None] = None,
                 identifier: Union[str, None] = None,
                 sex: int = 0,
                 phone: Union[str, None] = None,
                 nickname: Union[str, None] = None,
                 password: Union[str, None] = None,
                 token: Union[str, None] = None,
                 description: Union[str, None] = None,
                 status: int = 1,
                 role: RoleType = RoleType.USER):
        """  初始化方法
        在注册时使用，其中 email 是必须的

        20200524:: 添加匿名用户的需求，去掉了必要的验证
        添加了 `identifier` 字段，用来区分匿名用户
        """
        self.identifier = identifier
        self.email = email
        self.nickname = nickname
        self.password = password
        self.status = status
        self.phone = phone
        self.token = token
        self.description = description
        self.sex = sex
        self.role = role

    @classmethod
    def get_user(cls,
                 uid: Union[int, None] = None,
                 token: Union[str, None] = None) -> Union["User", None]:
        """  从表中查询用户实例
        Args:
            uid: 用户id
            token: 用户id别名
        Return: 
            用户的实例，如果没有找到则返回None
        """
        user: Union[User, None] = None
        try:
            if uid:
                user = User.query.filter(User.id == uid).one()
            if token:
                user = User.query.filter(User.token == token).one()
        except Exception as e:
            print(e)
        return user

    @property
    def get_cache_key(self) -> str:
        return "user_cache_key_{user_id}".format(user_id=self.id)

    def get_token(self) -> str:

        content: List[str] = []
        if self.email and self.password:
            content.append(self.email)
            content.append(self.password)

        elif self.identifier:
            content.append(self.identifier)

        content.append(get_random_num(2))

        token: str = getmd5('-'.join(content))
        return token

    def role_name(self) -> str:
        """ 获得用户角色的名称 """
        return Role.name_of(self.role)

    def role_model(self) -> Union[Role, None]:
        """
        获得用户的角色
        """
        role: Union[Role, None] = None
        try:
            role = Role.query.filter(Role.name == self.role_name).first()
        except:
            pass
        return role

    @property
    def role_permission_key(self) -> str:
        """
        获得用户的权限key
        """
        key: str = "user::{}permission_key".format(str(self.id))
        return key

    @property
    def info_dict(self) -> Dict[str, Any]:
        """  将用户信息组装成字典
        """
        payload: Dict[str, Any] = {
            "user_id": self.id,
            "sex": self.sex or 0,
            "email": self.email or "",
            "description": self.description or "",
            "account_status": self.status or 0,
            "nickname": self.nickname,
            "phone": self.phone,
            "is_anonymous": not self.email
        }
        return payload


class LoginRecordModel(db.Model, BaseModel):

    record_id = Column(
        INTEGER,
        Sequence("login_record_id_seq", start=1, increment=1),
        primary_key=True,
        comment="用户的登录记录",
    )
    user_id = Column(INTEGER, nullable=True)
    op_time = Column(db.DateTime, nullable=True, default=datetime.utcnow)
    op_ip = Column(String(20), nullable=True)

    def __init__(
        self,
        user_id: int,
        op_ip: Union[str, None] = None,
    ):

        self.user_id = user_id
        self.op_ip = op_ip
