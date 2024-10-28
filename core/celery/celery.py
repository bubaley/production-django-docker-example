import os

from celery import Celery
from django import conf, setup
from loguru import logger

from core.settings import common

os.environ.setdefault('DJANGO_SETTINGS_MODULE', common.SETTINGS_MODULE)
setup()

s = conf.settings

app = Celery(
    main='app',
    broker=s.CELERY_BROKER_URL,
    backend=s.CELERY_BACKEND_URL,
    broker_connection_retry_on_startup=True,
)
app.config_from_object('core.celery.celery_config')
app.autodiscover_tasks()

if not s.CELERY_BEAT_ENABLED:
    logger.info('Celery beat disabled by settings. Set CELERY_BEAT_ENABLED=True for enable.')
    app.conf.beat_schedule = {}
if s.TESTING:
    app.conf.update(task_always_eager=True)
