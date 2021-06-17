from flask import request

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm

from sqlalchemy.orm.exc import (MultipleResultsFound, NoResultFound,

                                UnmappedColumnError)

from app.utils import parse_params_from_request

from vendor.ext_redis import FlaskRedis


__all__ = ['db', 'redis_client', 'login_manager']


db = SQLAlchemy()


redis_client = FlaskRedis(config_key="REDIS_URI")


login_manager = LoginManager()

  

 # request data 基础验证器

class FlaskAPIForm(FlaskForm):

      # 解析请求参数

    def __init__(self):

        params = parse_params_from_request()

        super(FlaskAPIForm, self).__init__(data=params)
    

    @property

    def errors(self):

        errors = {name: ";".join(f.errors) for name, f in self._fields.items() if f.errors}
        return errors
    