import os
from logging.config import dictConfig

from celery import Celery, signals
from django import conf, setup

from core.settings import common

os.environ.setdefault('DJANGO_SETTINGS_MODULE', common.SETTINGS_MODULE)
setup()

app = Celery(
    main='app',
    broker=conf.settings.CELERY_BROKER_URL,
    backend=conf.settings.CELERY_BACKEND_URL,
    broker_connection_retry_on_startup=True,
)
app.config_from_object('core.celery.celery_config')
app.autodiscover_tasks()

if conf.settings.TESTING:
    app.conf.update(task_always_eager=True)


@signals.setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(conf.settings.LOGGING)
