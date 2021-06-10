from tasks import celery_app
from app import config

celery_app.config_from_object(config)

app = celery_app
