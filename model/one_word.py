from typing import Union
from datetime import datetime
from sqlalchemy import Column, String
from sqlalchemy import TEXT, INTEGER
from app.utils import db


class OneWord(db.Model):
    id = Column(INTEGER, primary_key=True)
    # 主体内容
    content = Column(TEXT, nullable=False)
    # 翻译 只有外文才可能有
    translate = Column(TEXT, nullable=True)
    # 图，可选的
    picture = Column(TEXT, nullable=True)
    # 录入时间
    create_date = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 作者
    author = Column(String(64), nullable=True)

    def __init__(self,
                 content: str,
                 translate: Union[str, None] = None,
                 picture: Union[str, None] = None,
                 author: Union[str, None] = None):
        self.content = content
        self.translate = translate
        self.picture = picture
        self.author = author
