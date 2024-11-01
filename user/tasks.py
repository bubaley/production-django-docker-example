from celery import shared_task

from core.celery.celery_enums import CeleryTasks
from core.utils.logger import Logg


@shared_task(name=CeleryTasks.USER_EXAMPLE)
def user_example():
    Logg.info(e=CeleryTasks.USER_EXAMPLE)
    return {'success': True}
