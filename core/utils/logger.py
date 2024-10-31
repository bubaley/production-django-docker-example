import logging
import sys
from pathlib import Path

from celery.app.trace import (
    LOG_FAILURE,
    LOG_IGNORED,
    LOG_INTERNAL_ERROR,
    LOG_RECEIVED,
    LOG_REJECTED,
    LOG_RETRY,
    LOG_SUCCESS,
)
from loguru import logger


def init_logging(log_dir: Path, debug: bool, *args, **kwargs):
    _init_logger(log_dir, debug, *args, **kwargs)
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': logging.StreamHandler,
            },
            'loguru': {
                'level': 'INFO',
                'class': LoguruHandler,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django.server': {  # Log requests - GET /api/v1/users/me HTTP/1.1 500. Disabled in container
                'handlers': ['loguru'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['loguru'],
                'level': 'ERROR',  # Log request errors
                'propagate': False,
            },
            'celery': {
                'handlers': ['loguru'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }


def _init_logger(log_dir: Path, debug: bool, *args, **kwargs):
    sys.excepthook = _log_exceptions

    format_values = [
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>',
        '<level>{level: <8}</level>',
        '{message}',
        '<cyan>{name}<red>:</red>{function}<red>:</red>{line}</cyan>',
    ]
    params = {'format': ' <red>|</red> '.join(format_values), 'backtrace': False, 'diagnose': False}

    logger.remove()
    logger.add(
        sys.stdout,
        **params,
    )
    if debug:  # Disabled write log to files in production mode
        logger.add(
            log_dir / 'today.log',
            rotation='00:00',
            retention='1 week',
            **params,
        )


def _log_exceptions(exc_type, exc_value, exc_traceback):
    logger.opt(exception=exc_value).log('ERROR', {'event': 'UNHANDLED', 'type': exc_type.__name__})


CELERY_LOG_FORMATS = {}


class LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        if record.name.startswith('celery.'):
            msg = self._get_celery_message(record)
        else:
            msg = record.getMessage()
        logger.opt(exception=record.exc_info, depth=6).log(level, msg)

    @staticmethod
    def _get_celery_message(record: logging.LogRecord):
        if not hasattr(record, 'data'):
            return str({'event': 'CELERY_TRACE', 'message': record.getMessage()})
        celery_log_types = {
            LOG_RECEIVED: 'RECEIVED',
            LOG_SUCCESS: 'SUCCESS',
            LOG_FAILURE: 'FAILURE',
            LOG_INTERNAL_ERROR: 'INTERNAL_ERROR',
            LOG_IGNORED: 'IGNORED',
            LOG_REJECTED: 'REJECTED',
            LOG_RETRY: 'RETRY',
        }
        data = getattr(record, 'data') or {}
        message_data = {
            'event': 'CELERY_LOG',
            'type': celery_log_types.get(record.msg, 'UNHANDLED'),
            'task': str(data.get('name')),
            'task_id': data.get('id'),
            'args': data.get('args'),
            'kwargs': data.get('kwargs'),
            'runtime': f'{round(data['runtime'], 3)}s' if data.get('runtime') else None,
            'return': data.get('return_value'),
        }
        return str(message_data)
