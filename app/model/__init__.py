from flask import Flask
from flask_sqlalchemy import get_debug_queries

from app.extensions import db
from app.utils import get_logger

from .one_word import OneWord  # noqa
from .rss import RssContentModel, RssModel
from .user import RoleModel, User
from .website import Category, WebSite  # noqa

logger = get_logger(__file__)


def prepare_data_id_needed():
    # 准备必要数据
    ...

def init_app(app: Flask):
    # 创建表
    @app.before_first_request
    def create_all_models():
        return
        db.create_all(app=app)
        prepare_data_id_needed()

    # 慢查询检测
    @app.after_request
    def query_time_out(response):

        for query in get_debug_queries():
            if query.duration >= 0.05:
                app.logger.warn(
                    "Context: {} \n SLOW QUERY: {} \n Parameters: {} \n Duration: {} \n"  # noqa
                    .format(
                        query.context,
                        query.statement,
                        query.parameters,
                        query.duration,
                    ))
        return response

    try:
        from flask_migrate import Migrate
        db.init_app(app)
        Migrate(app=app, db=db)
    except ImportError:
        pass
