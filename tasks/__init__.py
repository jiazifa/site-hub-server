
from celery import Celery

from . import email

celery_app = Celery(__name__)
