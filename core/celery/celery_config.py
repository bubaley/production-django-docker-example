from core.celery.celery_enums import CeleryTaskQueues, CeleryTasks
from core.settings import common

task_serializer = 'json'
task_default_queue = CeleryTaskQueues.DEFAULT
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000
worker_disable_rate_limits = False
broker_transport_options = {'queue_order_strategy': 'priority'}
beat_schedule_filename = common.BASE_DIR / 'data' / 'celerybeat-schedule.db'

task_routes = {
    # urgent
    CeleryTasks.USER_EXAMPLE: {'queue': CeleryTaskQueues.URGENT},
}

beat_schedule = {
    'example': {
        'task': CeleryTasks.USER_EXAMPLE,
        'schedule': 5,
    },
}

task_queues = {
    CeleryTaskQueues.LOW: {
        'exchange': CeleryTaskQueues.LOW,
        'routing_key': CeleryTaskQueues.LOW,
        'exchange_type': 'direct',
        'queue_arguments': {'x-max-priority': 2},
    },
    CeleryTaskQueues.DEFAULT: {
        'exchange': CeleryTaskQueues.DEFAULT,
        'routing_key': CeleryTaskQueues.DEFAULT,
        'exchange_type': 'direct',
        'queue_arguments': {'x-max-priority': 5},
    },
    CeleryTaskQueues.URGENT: {
        'exchange': CeleryTaskQueues.URGENT,
        'routing_key': CeleryTaskQueues.URGENT,
        'exchange_type': 'direct',
        'queue_arguments': {'x-max-priority': 9},
    },
}
