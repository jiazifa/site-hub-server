from flask import Flask
from flask_sqlalchemy import get_debug_queries
from app.utils import db
from common import get_logger
from model.website import WebSite, Category  # noqa
from model.one_word import OneWord  # noqa

logger = get_logger(__file__)


def init_app(app: Flask):
    @app.before_first_request
    def create_all_models():

        db.create_all(app=app)

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
