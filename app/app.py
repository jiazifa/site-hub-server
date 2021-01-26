import os
from typing import Union
from flask import Flask
import model
from . import config
from common import get_logger
from app import views, api
from app.utils import redis_client

__root_dir = os.path.dirname(os.path.abspath(__name__))

logger = get_logger(__name__)


def app_env_log(app: Flask):
    mode_: str = "开发环境"
    if app.debug == False:
        mode_ = "正式环境"
    logger.info("当前处于{}".format(mode_))


def create_app() -> Flask:
    app = Flask(__name__,
                static_url_path="/s",
                static_folder="static",
                template_folder="templates")
    # 应用配置文件
    app.config.from_object(config)
    if hasattr(config, "TESTING"):
        app.is_testing = bool(getattr(config, "TESTING"))

    app_env_log(app)
    # 配置数据库
    model.init_app(app)
    # 配置redis客户端
    redis_client.init_app(app)
    # 配置接口以及视图
    views.init_app(app)
    api.init_app(app)
    return app
