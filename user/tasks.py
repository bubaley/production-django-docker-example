from celery import shared_task
from loguru import logger

from core.celery.celery_enums import CeleryTasks


@shared_task(name=CeleryTasks.USER_EXAMPLE)
def user_example():
    logger.info({'event': CeleryTasks.USER_EXAMPLE.upper()})
    return {'success': True}
