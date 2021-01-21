from typing import Union
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy import TEXT, INTEGER
from app.utils import db


# 站点模型，一个站点模型可能对应一个分类模型
class WebSite(db.Model):
    id = Column(INTEGER, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)
    description = Column(String(516), nullable=True)
    url = Column(String(516), unique=True, nullable=False)
    thumb = Column(TEXT, nullable=True)
    create_date = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = Column(INTEGER, ForeignKey("category.id"), nullable=True)
    category = db.relationship("Category",
                               backref=db.backref("websites"),
                               lazy=True)

    def __init__(self, name: str, description: str, url: str, thumb: str,
                 category: Union['Category', None]):
        self.name = name
        self.description = description
        self.url = url
        self.thumb = thumb
        self.category = category

    def to_dict(self):
        payload: dict = {
            "id": self.id,  # noqa
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "thumb": self.thumb,
            "create_date": str(self.create_date),
            "category_id": self.category_id,
        }
        return payload


# 分类，与站点属于一对多关系
class Category(db.Model):
    id = Column(INTEGER, primary_key=True)
    name = Column(String(128), nullable=False)

    def __init__(self, name: str):
        self.name = name
