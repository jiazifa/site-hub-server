from typing import Any, List, Tuple

from flask import Blueprint, Flask


def regist_blueprint_to_app(app: Flask, info: Tuple[Blueprint, str]):
    prefix: str = "/api/" + info[1].lstrip("/")
    app.register_blueprint(info[0], url_prefix=prefix)


def init_app(app: Flask):
    flush_blueprint: List[Blueprint]
    info: Tuple[Blueprint, str]
    from . import file as file_
    from . import one_word, rss, site, user
    modules: List[Any] = [one_word, site, file_, user, rss]
    for m in modules:
        info = (m.api, m.prefix)
        regist_blueprint_to_app(app, info)