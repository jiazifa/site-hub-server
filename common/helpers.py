# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional
import logging
from urllib import parse
import sys
from app import config
"""
Helper functions
"""

loggers: Dict[str, logging.Logger] = {}


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """  获得一个logger 实例，用来打印日志
    Args:
        name: logger的名称
    Return:
        返回一个logger实例
    """
    global loggers

    if not name:
        name = __name__

    has = loggers.get(name)
    if has:
        return has

    logger = logging.getLogger(name=name)
    stream_handler = logging.StreamHandler(sys.stdout)

    logger.setLevel(config.LOG_LEVEL)
    stream_handler.setLevel(config.LOG_LEVEL)
    formatter = logging.Formatter(config.LOGGING_FORMATTER)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    loggers[name] = logger

    return logger


def parser_url_path_rule1(old: str, replace: str) -> str:

    if not old:
        return old
    if old.startswith('http'):
        return old
    ret = parse.urlparse(replace)
    _link = str(ret.scheme) + "://" + str(ret.netloc) + old

    return _link
