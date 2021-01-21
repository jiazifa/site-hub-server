from typing import Union, List, Dict, Any
from random import choice
from flask import Blueprint, request
from flask.views import MethodView
from common import get_logger, parse_params
from model.one_word import OneWord as OneWordModel
from app.utils import db, CommonError, ResponseErrorType, response_success, NoResultFound, MultipleResultsFound

logget = get_logger(__name__)

prefix: str = "oneword"
api: Blueprint = Blueprint(prefix, __name__)


class OneWordMethod(MethodView):
    """
    对one_word 资源的增删改查
    """
    def get(self):
        list_result: Union[List[OneWordModel],
                           None] = db.session.query(OneWordModel).all()
        if not list_result:
            return CommonError.error_toast(ResponseErrorType.NOT_FOUND,
                                           message="资源未找到")
        result: OneWordModel = choice(list_result)
        return response_success(body=result.content)

    def post(self):
        params: Dict[str, Any] = parse_params(request)
        keys: List[str] = ["content"]
        for key in keys:
            if not params.get(key):
                toast: str = "key: {} not found in params".format(key)
                return CommonError.error_enum(ResponseErrorType.REQUEST_ERROR,
                                              message=toast)

        content: str = params.get("content")
        # 根据content字符判断是否重复
        exists_model: Union[OneWordModel, None] = None
        payload: Dict[str, int] = {}
        try:
            exists_model = db.session.query(OneWordModel).filter_by(
                content=content).one()
            payload.setdefault("id", exists_model.id)
        except NoResultFound:
            translate: Union[str, None] = params.get("translate")
            picture: Union[str, None] = params.get("picture")
            model: OneWordModel = OneWordModel(content=content,
                                               translate=translate,
                                               picture=picture,
                                               author=params.get("author"))
            db.session.add(model)
            db.session.commit()
            payload.setdefault("id", model.id)
        except MultipleResultsFound:
            exists_model = db.session.query(OneWordModel).filter_by(
                content=content).first()

        return response_success(body=payload)


def get_word_by_id(word_id: int):
    result: OneWordModel = OneWordModel.query.get(word_id)
    return response_success(body=result.content)


def setup_urls(api: Blueprint):
    one_word_view_func = OneWordMethod.as_view("one_word")
    # 通过id获取具体的句子或修改
    api.add_url_rule(rule="/<int:word_id>",
                     view_func=get_word_by_id,
                     methods=["GET"])

    # 新增句子或者随机获取一个句子
    api.add_url_rule(rule="/", view_func=one_word_view_func)


setup_urls(api)
