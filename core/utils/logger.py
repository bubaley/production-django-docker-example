import logging
import sys
from pathlib import Path

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
                'class': LoggerHandler,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django.server': {  # Log requests - "GET /api/v1/users/me HTTP/1.1" 500. Disabled in container
                'handlers': ['loguru'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['loguru'],
                'level': 'ERROR',  # Log request errors
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


class LoggerHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        if record.exc_info:
            logger.opt(exception=record.exc_info).log(level, record.getMessage())
        else:
            logger.log(level, record.getMessage())
