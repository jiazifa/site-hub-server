from typing import Dict
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, SMALLINT, TEXT, INTEGER, Sequence
from common import get_random_num, getmd5, get_unix_time_tuple
from app.utils import db

# 角色
class RoleType(Enum):
    # 管理员
    ADMIN = 0x01
    # 用户
    USER = 0x02
    # 匿名
    ANONYMOUS = 0x04


# 权限列表
class PermissionType(Enum):
    # 个人信息管理
    USER_MANAGE = 0x01
    # 发布信息
    POST_MESSAGE = 0x02

class Role(db.Model):
    id = Column(INTEGER, primary_key=True)
    name = Column(String(32), unique=True, comment="角色名")
    description = Column(String(128), nullable=True, comment="说明")
    permissions = Column(INTEGER, comment="权限总值")

    @staticmethod
    def name_of(role: RoleType) -> str:
        """
        获得权限角色的名称
        """
        switcher: Dict[int, str] = {
            RoleType.ANONYMOUS.value: "anonymous",
            RoleType.USER.value: "user",
            RoleType.ADMIN.value: "admin"
        }
        return switcher.get(role.value, 'unknown')