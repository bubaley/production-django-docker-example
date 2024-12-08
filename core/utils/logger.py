import inspect
import json
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

CRITICAL = 'CRITICAL'
ERROR = 'ERROR'
WARNING = 'WARNING'
INFO = 'INFO'
DEBUG = 'DEBUG'


class Logg:
    """Class for logging events in JSON format.

    Arguments::
        args : don't use unnamed arguments
        e : indicate the event with a dot
        msg : always set by the second argument. Use short string

    Usage::
        Logg.info(e='balance.updated', msg='guest balance increased', sum=322)
    """

    @staticmethod
    def info(*args, **kwargs):
        Logg._log(INFO, *args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        Logg._log(WARNING, *args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        Logg._log(ERROR, *args, **kwargs)

    @staticmethod
    def debug(*args, **kwargs):
        Logg._log(DEBUG, *args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        Logg._log(CRITICAL, *args, **kwargs)

    @staticmethod
    def _log(level: str, *args, **kwargs):
        message = Logg._serialize_message(*args, **kwargs)
        logger.opt(depth=2).log(level, message)

    @staticmethod
    def _serialize_message(*args, **kwargs):
        data = {'e': str(kwargs.pop('e')).lower() if 'e' in kwargs else 'message'}
        if len(args) > 0 and isinstance(args[0], str) and 'msg' not in kwargs:
            data['msg'] = args[0]
            args = args[1:]
        elif 'msg' in kwargs:
            data['msg'] = str(kwargs.pop('msg'))
        data.update(kwargs)
        if args:
            data['args'] = args
        return json.dumps(data, default=str, ensure_ascii=False)


def init_logging(log_dir: Path, debug: bool, *args, **kwargs):
    _init_logger(log_dir, debug, *args, **kwargs)
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': INFO,
                'class': logging.StreamHandler,
            },
            'loguru': {
                'level': INFO,
                'class': LoguruHandler,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': INFO,
            },
            'django.server': {  # Log requests - GET /api/v1/users/me HTTP/1.1 500. Disabled in container
                'handlers': ['loguru'],
                'level': INFO,
                'propagate': False,
            },
            'django.request': {
                'handlers': ['loguru'],
                'level': ERROR,  # Log request errors
                'propagate': False,
            },
            'celery': {
                'handlers': ['loguru'],
                'level': INFO,
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
    message = Logg._serialize_message(e='exception.hook', type=exc_type.__name__)
    logger.opt(exception=exc_value).log(ERROR, message)


class LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        message = self._prepare_message(record)
        depth = self._get_depth(record)
        logger.opt(exception=record.exc_info, depth=depth).log(level, message)

    @staticmethod
    def _get_depth(record: logging.LogRecord):
        for depth, frame in enumerate(inspect.stack()):
            if record.pathname == frame.filename:
                return depth - 1
        return 2

    @staticmethod
    def _prepare_message(record: logging.LogRecord):
        if not record.name.startswith('celery.'):
            return Logg._serialize_message(e='app.trace', msg=record.getMessage())

        if not hasattr(record, 'data'):
            return Logg._serialize_message(e='celery.trace', msg=record.getMessage())
        celery_log_types = {
            LOG_RECEIVED: 'received',
            LOG_SUCCESS: 'success',
            LOG_FAILURE: 'failure',
            LOG_INTERNAL_ERROR: 'internal_error',
            LOG_IGNORED: 'ignored',
            LOG_REJECTED: 'rejected',
            LOG_RETRY: 'retry',
        }
        data = getattr(record, 'data') or {}
        return Logg._serialize_message(
            e='celery.task',
            type=celery_log_types.get(record.msg, 'unhandled'),
            task=str(data.get('name')),
            task_id=data.get('id'),
            args=data.get('args'),
            kwargs=data.get('kwargs'),
            runtime=f'{round(data['runtime'], 3)}s' if data.get('runtime') else None,
            return_value=data.get('return_value'),
        )
