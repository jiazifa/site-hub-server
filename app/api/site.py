from typing import Union, List, Any, Dict
from flask import Blueprint
from common import get_logger, parse_params
from model.website import Category, WebSite
from app.utils import db, NoResultFound, MultipleResultsFound, CommonError, ResponseErrorType, response_success

logger = get_logger(__name__)

prefix: str = "site"
api: Blueprint = Blueprint(prefix, __name__)


def get_categories():
    # 获得所有的分类
    models: List[Category]
    try:
        models = db.session.query(Category).all()
    except NoResultFound:
        return CommonError.error_enum(type=ResponseErrorType.UNKNOWN_ERROR)

    payload: List[Dict[str, Union[str, int]]] = [{"id": r.id} for r in models]
    return response_success(body=payload)


def create_category():
    params: Dict[str, Any] = parse_params(request)
    keys: List[str] = ["name"]
    if not all([k in params for k in keys]):
        return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR)

def get_site(site_id: int):
    # 根据传入的id获得对应的站点信息
    site: WebSite = WebSite.query.get(site_id)
    if not site:
        return CommonError.error_enum(ResponseErrorType.NOT_FOUND)

    payload: Dict[str, Union[str, int]] = {
        "id": site.id,
        "name": site.name,
        "description": site.description,
        "url": site.url,
    }
    return response_success(body=payload)


def get_site_by_categories():
    # 根据传入的分类id，来获得分页的网站数据
    params: Dict[str, Any] = parse_params(request)
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