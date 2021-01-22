from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import (NoResultFound, MultipleResultsFound,
                                UnmappedColumnError)
from vendor.ext_redis import FlaskRedis

db = SQLAlchemy()
session = db.session

redis_client = FlaskRedis(config_key="REDIS_URI")
