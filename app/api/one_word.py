from random import choice
from typing import Any, Dict, List, Union

from flask import Blueprint
from flask.views import MethodView
from wtforms import StringField
from wtforms.validators import Required

from app.extensions import (FlaskAPIForm, MultipleResultsFound, NoResultFound,
                            db)
from app.model.one_word import OneWord as OneWordModel
from app.utils import response_success, get_logger, parse_params_from_request
from app.utils.errors import (NotFoundExeception, ParameterException,
                              UnknownExeception)

logget = get_logger(__name__)

prefix: str = "oneword"
api: Blueprint = Blueprint(prefix, __name__)


class _OneWrodForm(FlaskAPIForm):

    content = StringField('content', validators=[Required()])


class OneWordMethod(MethodView):
    """
    对one_word 资源的增删改查
    """
    def get(self):
        list_result: Union[List[OneWordModel],
                           None] = db.session.query(OneWordModel).all()
        if not list_result:
            raise NotFoundExeception(message="未发现资源")
        result: OneWordModel = choice(list_result)
        return response_success(body=result.content)

    def post(self):
        contentForm = _OneWrodForm()
        if not contentForm.validate():
            raise ParameterException(unique_data=contentForm.errors)
        params: Dict[str, Any] = parse_params_from_request()

        content: str = contentForm.content.data
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
            payload.setdefault("id", exists_model.id)
        except Exception as e:
            raise e

        return response_success(body=payload)


def get_word_by_id(word_id: int):
    result: OneWordModel = OneWordModel.query.get(word_id)
    return response_success(body=result.content)


def setup_urls(api: Blueprint):
    one_word_view_func = OneWordMethod.as_view("one_word/")
    # 通过id获取具体的句子或修改
    api.add_url_rule(rule="/<int:word_id>/",
                     view_func=get_word_by_id,
                     methods=["GET"])

    # 新增句子或者随机获取一个句子
    api.add_url_rule(rule="/", view_func=one_word_view_func)


setup_urls(api)
