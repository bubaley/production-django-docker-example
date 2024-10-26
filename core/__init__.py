from .celery.celery import app as celery_app
from .utils.base_logger import logger as logger_app

__all__ = ('celery_app', 'logger_app')
