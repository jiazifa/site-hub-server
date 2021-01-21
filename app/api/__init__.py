from typing import List, Tuple, Any

from flask import Flask, Blueprint


def regist_blueprint_to_app(app: Flask, info: Tuple[Blueprint, str]):
    prefix: str = "/api/" + info[1].lstrip("/")
    app.register_blueprint(info[0], url_prefix=prefix)


def init_app(app: Flask):
    flush_blueprint: List[Blueprint]
    info: Tuple[Blueprint, str]
    from . import one_word
    from . import site
    modules: List[Any] = [one_word, site]
    for m in modules:
        info = (m.api, m.prefix)
        regist_blueprint_to_app(app, info)