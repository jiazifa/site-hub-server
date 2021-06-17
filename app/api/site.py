from typing import Any, Dict, List, Union

from flask import Blueprint

from app.extensions import MultipleResultsFound, NoResultFound, db
from app.model.website import Category, WebSite
from app.utils import response_success
from app.utils.errors import (NotFoundExeception, ParameterException,
                              UnknownExeception)
from app.utils import get_logger, parse_params_from_request

logger = get_logger(__name__)

prefix: str = "site"
api: Blueprint = Blueprint(prefix, __name__)


def get_categories():
    # 获得所有的分类
    models: List[Category]
    try:
        models = db.session.query(Category).all()
    except NoResultFound:
        return NotFoundExeception()

    payload: List[Dict[str, Union[str, int]]] = [{"id": r.id} for r in models]
    return response_success(body=payload)


def create_category():
    # 创建分类
    params: Dict[str, Any] = parse_params_from_request()
    keys: List[str] = ["name"]
    for key in keys:
        if not params.get(key):
            raise ParameterException(message="{} 缺失".format(key))

    name: str = params["name"]

    payload: Dict[str, int] = {}
    exists_model: Union[Category, None] = None
    try:
        exists_model = db.session.query(Category).filter_by(name=name)
        payload.setdefault("id", exists_model.id)
    except NoResultFound:
        exists_model = Category(name)
        db.session.add(exists_model)
        db.session.commit(exists_model)
        payload.setdefault("id", exists_model.id)
    except MultipleResultsFound:
        exists_model = db.session.query(Category).filter_by(name=name).first()
        payload.setdefault("id", exists_model.id)
    else:
        raise UnknownExeception()

    return response_success(body=payload)


def get_site(site_id: int):
    # 根据传入的id获得对应的站点信息
    site: WebSite = WebSite.query.get(site_id)
    if not site:
        raise NotFoundExeception()

    payload: Dict[str, Union[str, int]] = {
        "id": site.id,
        "name": site.name,
        "description": site.description,
        "url": site.url,
    }
    return response_success(body=payload)


def get_site_by_categories():
    # 根据传入的分类id，来获得分页的网站数据
    params: Dict[str, Any] = parse_params_from_request()
    category_ids: List[int] = params.get("category_ids") or []
    models: List[WebSite] = db.session.query(WebSite).filter(
        WebSite.category_id.in_(category_ids)).all() or []
    payload: List[Dict[str, Union[str, int]]] = [m.to_dict() for m in models]
    return response_success(body=payload)


def setup_urls(api: Blueprint):
    api.add_url_rule("/categories", view_func=get_categories, methods=["GET"])

    api.add_url_rule("/<int:site_id>", view_func=get_site, methods=["GET"])
    api.add_url_rule("/by_category",
                     view_func=get_site_by_categories,
                     methods=["POST"])


setup_urls(api)