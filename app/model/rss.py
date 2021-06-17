from datetime import datetime
from typing import Any, Dict, Union

from flask import session
from flask_login import UserMixin
from sqlalchemy import (INTEGER, SMALLINT, TEXT, Column, DateTime, Sequence,
                        String)
from sqlalchemy.orm import relationship

from app.extensions import db, login_manager
from app.utils import parse_params_from_request
from common import get_unix_time_tuple

from .base import BaseModel
from .user import User


class RssModel(db.Model, BaseModel):

    __tablename__ = "rss"

    # 订阅的模型
    rss_id = Column(INTEGER,
                    Sequence(start=1, increment=1, name="rss_id_sep"),
                    primary_key=True,
                    autoincrement=True)
    rss_link = Column(String(255), nullable=True, unique=True)
    rss_title = Column(String(255), nullable=True, comment='订阅的标题')
    rss_subtitle = Column(String(255), nullable=True)
    create_date = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rss_version = Column(String(10), nullable=True)
    rss_contents =  relationship("RssContentModel", backref="rss", lazy="dynamic")
    rss_state = Column(SMALLINT, nullable=True)  # 1 创建(未验证) 2 有效 3 失效

    def __init__(self,
                 link: str,
                 title: Union[None, str] = None,
                 subtitle: Union[None, str] = None):
        self.rss_link = link
        self.rss_title = title
        self.rss_subtitle = subtitle
        self.rss_state = 1

    @staticmethod
    def get_by_link(link: str) -> Union[None, 'RssModel']:
        return RssModel.query.filter_by(rss_link=link).first()

    def get_info(self) -> Dict[str, Any]:
        paylaod: Dict[str, Any] = {}
        paylaod.setdefault("id", self.rss_id)
        paylaod.setdefault("link", self.rss_link)
        paylaod.setdefault("title", self.rss_title)
        paylaod.setdefault("subtitle", self.rss_subtitle)
        paylaod.setdefault("create_at", self.create_date)
        return paylaod


class RssContentModel(db.Model, BaseModel):
    __tablename__ = "rss_content"
    # 订阅抓取的内容
    content_id = Column(INTEGER,
                        Sequence(start=1, increment=1, name="content_id_sep"),
                        primary_key=True,
                        autoincrement=True)
    # from which rss subscript
    content_base = Column(String(255), nullable=True)
    content_link = Column(String(512), unique=True, nullable=True)
    content_title = Column(String(255), nullable=True)
    content_description = Column(TEXT, nullable=True)
    content_image_cover = Column(String(255), nullable=True)
    published_time = Column(db.DateTime, nullable=True)
    create_date = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rss_id = Column(INTEGER, db.ForeignKey('rss.rss_id'))

    def __init__(self,
                 link: str,
                 baseurl: str,
                 title: str,
                 description: Union[str, None] = None,
                 cover_img: Union[str, None] = None,
                 published_time: Union[float, int, str, None] = None):
        self.content_link = link
        self.content_base = baseurl
        self.content_title = title
        self.published_time = published_time
        self.content_image_cover = cover_img
        self.content_description = description
        self.published_time = float(
            published_time) if published_time else datetime.utcnow()

    def get_info(self):
        paylaod: Dict[str, Any] = {}
        paylaod.setdefault("id", self.content_id)
        paylaod.setdefault("link", self.content_link)
        paylaod.setdefault("title", self.content_title)
        paylaod.setdefault("description", self.content_description)
        paylaod.setdefault("image", self.content_image_cover)
        paylaod.setdefault("based", self.content_base)
        paylaod.setdefault("create_at", get_unix_time_tuple(self.create_date))
        return paylaod