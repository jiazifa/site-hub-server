from app import config
from tasks import celery_app

celery_app.config_from_object(config)

app = celery_app
