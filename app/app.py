import os
from typing import Union

from flask import Flask

from app import api, model, views
from app.extensions import login_manager, redis_client
from app.utils.errors import APIException, HTTPException, UnknownExeception
from app.utils import get_logger

from . import config

__root_dir = os.path.dirname(os.path.abspath(__name__))

logger = get_logger(__name__)


def create_app() -> Flask:
    app = Flask(__name__,
                static_url_path="/s",
                static_folder="static",
                template_folder="templates")
    # 应用配置文件
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    return app


def register_extensions(app: Flask):
    # 配置数据库
    model.init_app(app)
    # 配置redis客户端
    redis_client.init_app(app)
    # 配置用户登录
    login_manager.init_app(app)


def register_blueprints(app: Flask):
    # 配置接口以及视图
    views.init_app(app)
    api.init_app(app)


def register_errorhandlers(app: Flask):
    @app.errorhandler(Exception)
    def handle_with_exeception(error: Exception):
        if isinstance(error, APIException):
            return error
        elif isinstance(error, HTTPException):
            return APIException(error.code,
                                error.description,
                                error_code=error.code *
                                100 if error.code else 99999)
        else:
            # if app.debug:
            #     import pdb
            #     pdb.set_trace()
            return UnknownExeception(message=str(error))


def register_shellcontext(app: Flask):
    ...


def config_logger(app: Flask):
    mode_: str = "开发环境"
    if app.debug == False:
        mode_ = "正式环境"
    logger.info("当前处于{}".format(mode_))