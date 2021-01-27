from typing import Union, List, Any, Dict
from flask import Blueprint, request
from common import get_logger
from model.website import Category, WebSite
from app.utils import (db, NoResultFound, MultipleResultsFound, CommonError,
                       ResponseErrorType, response_success, parse_params,
                       valid_require_params, login_require)

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


@login_require
def create_category():
    """
    创建分类
    """
    params: Dict[str, Any] = parse_params(request)
    keys: List[str] = ["name"]
    if not all([k in params for k in keys]):
        return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR)

    name: str = params.get("name", "")
    query = db.session.query(Category).filter_by(name=name)

    is_exisit: bool = db.session.query(query.exists()).scalar()
    if is_exisit:
        return CommonError.error_toast(ResponseErrorType.EXISIT,
                                       message="该分类已经存在")

    category: Category = Category(name)
    category.save(commit=True)

    payload: Dict[str, Any] = {}
    payload.setdefault("id", category.id)
    return response_success(body=payload)


@login_require
def create_site():
    params: Dict[str, Any] = parse_params(request)
    keys: List[str] = ["name", "url", "category_id"]
    require_key = valid_require_params(keys, params)
    if require_key:
        return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR)

    name: str = params.get("name", "")
    url: str = params.get("url", "")
    category_id: int = params.get("category_id", 0)

    description: Union[str, None] = params.get("description")
    thumb: Union[str, None] = params.get("thumb")

    exisit_category: Category
    try:
        exisit_category = db.session.query(Category).filter_by(
            id=category_id).one()
    except NoResultFound:
        return CommonError.error_toast(ResponseErrorType.REQUEST_ERROR,
                                       message="没有找到对应分类")
    except MultipleResultsFound:
        exisit_category = db.session.query(Category).filter_by(
            id=category_id).first()

    query = db.session.query(WebSite).filter_by(url=url, category_id=category_id)
    is_exisit: bool = db.session.query(query.exists()).scalar()

    if not is_exisit:
        return CommonError.error_enum(ResponseErrorType.EXISIT)

    site: WebSite = WebSite(name=name,
                            description=description,
                            url=url,
                            thumb=thumb,
                            category=exisit_category)
    site.save(commit=True)

    paylod: Dict[str, Any] = {}
    paylod.setdefault("id", site.id)
    return response_success(body=paylod)


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
    # 获得分类
    api.add_url_rule("/categories", view_func=get_categories, methods=["GET"])
    # 创建分类
    api.add_url_rule("/category", view_func=create_category, methods=["POST"])
    # 创建
    api.add_url_rule("/create", view_func=create_site, methods=["POST"])
    # 获得网站
    api.add_url_rule("/<int:site_id>", view_func=get_site, methods=["GET"])
    # 根据分类获得网站列表
    api.add_url_rule("/by_category",
                     view_func=get_site_by_categories,
                     methods=["POST"])


setup_urls(api)