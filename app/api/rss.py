import datetime
import re
from typing import Any, Dict, List, Union

from flask import Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

from app.extensions import (FlaskAPIForm, MultipleResultsFound, NoResultFound,
                            db, login_manager)
from app.model import RssContentModel, RssModel, User
from app.utils import response_success, parse_params_from_request, get_logger
from app.utils.errors import (ConflictExeception, NotFoundExeception,
                              ParameterException, UnknownExeception,
                              PermissionException)
from common import get_random_num, getmd5


logger = get_logger(__name__)

prefix: str = "rss"
api: Blueprint = Blueprint(prefix, __name__)


class _AddRssForm(FlaskAPIForm):
    source = StringField('source', validators=[DataRequired()])


@api.post("/add/")
def add_rss_resource():
    form = _AddRssForm()
    if not form.validate():
        raise ParameterException(message=form.errors)
    rss: RssModel = RssModel.get_by_link(form.source.data)
    if not rss:
        # 查看是否可用
        regex = r'(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
        result = re.match(regex, source)
        if not result:
            raise ParameterException(toast="网址不太对吧？请检查下连接哦",
                                     message="参数正则验证失败")
        rss = RssModel(form.source.data)
        rss.save(commit=True)

    payload = rss.get_info()
    return response_success(body=payload)


@api.get("/list/")
def list_rss():
    params = parse_params_from_request()
    # pages
    pages = params.get('pages') or 0
    limit = params.get('limit') or 10
    payload = [
        item.get_info() for item in RssModel.query.filter(
            RssModel.rss_state != 1).limit(limit).offset(pages * limit).all()
    ]
    return response_success(payload)


"""
用于子任务模块拉取任务
"""


@api.post("/toggle_state/<int:rss_id>/")
@login_required
def diable_rss(rss_id: int):
    user: User = current_user
    if not user.get_role().is_admin:
        raise PermissionException(message="权限错误")
    rss: RssModel = RssModel.query.get(rss_id)
    if not rss:
        raise NotFoundExeception()
    if rss.rss_state == 1:
        raise ParameterException(message="资源还未验证过,不可操作")
    rss.rss_state = 3 if rss.rss_state == 2 else 2
    rss.save(commit=True)
    return response_success(body=rss.get_info())


@api.get("/after/<int:timestamp>/")
@login_required
def list_after(timestamp: int):
    user: User = current_user
    if not user.get_role().is_admin:
        raise PermissionException(message="权限错误")
    condition: Dict[str, Any] = {}
    create_after = datetime.datetime.fromtimestamp(timestamp)
    rsses = RssModel.query.filter(RssModel.create_date > create_after).all()
    paylod = [item.get_info() for item in rsses]
    return response_success(paylod)


"""
订阅的内容
"""


class _AddRssContentForm(FlaskAPIForm):
    link = StringField("link", validators=[DataRequired()])
    title = StringField("title", validators=[DataRequired()])
    based = StringField("based", validators=[DataRequired()])
    description = StringField("description")
    image_cover = StringField("image_cover")
    published_timestamp = StringField("published_timestamp")
    rss_id = IntegerField("rss_id")


@api.post("/content/add/")
def add_rss_content():
    form = _AddRssContentForm()
    if not form.validate():
        raise ParameterException(message=form.errors)
    content = RssContentModel.query.filter(
        RssContentModel.content_link == form.link.data,
        RssContentModel.content_base == form.based.data).first()
    if not content:
        content = RssContentModel(form.link.data, form.based.data,
                                  form.title.data)
        content.content_description = form.description.data
        content.content_image_cover = form.image_cover.data
        stamp = form.published_timestamp.data
        if stamp:
            date = datetime.datetime.fromtimestamp(stamp)
            content.published_time = date
        rss_id = form.rss_id.data
        if rss_id:
            content.rss_id = int(rss_id)
        content.save(commit=True)
    payload = content.get_info()
    return response_success(body=payload)


@api.get("/content/list/")
def query_rss_content():

    params = parse_params_from_request()
    # pages
    pages = int(params.get('pages') or '0')
    limit = int(params.get('limit') or '10')
    query = RssContentModel.query.filter().order_by(
        RssContentModel.published_time.desc()).limit(limit).offset(pages *
                                                                   limit)
    items = query.all()
    payload = [item.get_info() for item in items]
    return response_success(payload)


def setup_urls(api: Blueprint):
    ...


setup_urls(api)