import os
from os import path

_here = path.dirname(__name__)
root_dir = os.path.abspath((os.path.dirname(__file__)))
workspace = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True

TESTING = False

# 开启跨站请求伪造防护
SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
"""SQLALCHEMY配置"""
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URI", "sqlite:///" + os.path.join(workspace, "test.db"))

SQLALCHEMY_COMMIT_ON_TEARDOWN = False
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
""" Logging 设置 """
LOG_LEVEL = "DEBUG"  # 日志输出等级
LOGGING_FORMATTER = "%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s"  # 每条日志输出格式 # noqa
LOGGING_DATE_FORMATTER = "%a %d %b %Y %H:%M:%S"
LOGGING_DIR = os.path.join(root_dir, "logs")
LOG_ENABLE = True  # 是否开启日志
""" Email 设置 """
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
"""  Redis 配置 """
REDIS_URI = os.environ.get("REDIS_URI", "redis://0.0.0.0:6379/")
"""Celery 配置"""

CELERY_RESULT_BACKEND = REDIS_URI

BROKER_URL = REDIS_URI + "0"

CELERY_TIMEZONE = "Asia/Shanghai"

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_ACCEPT_CONTENT = ["json"]

try:
    from local_settings import * # noqa
except ImportError:
    print("导入错误")
    pass
