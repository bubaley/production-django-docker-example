import logging
import sys
from pathlib import Path

from loguru import logger


def init_logging(log_dir: Path, debug: bool, *args, **kwargs):
    _init_logger(log_dir)

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
                'handlers': ['console'] if debug else [],
                'level': 'INFO',
            },
            'django.server': {
                'handlers': ['loguru'],
                'level': 'INFO' if debug else 'ERROR',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['loguru'],
                'level': 'INFO' if debug else 'ERROR',
                'propagate': False,
            },
        },
    }


def _init_logger(log_dir: Path):
    sys.excepthook = _log_exceptions

    format_values = [
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>',
        '<level>{level: <8}</level>',
        '{message}',
        '<cyan>{file.name}<red>:</red>{function}<red>:</red>{line}</cyan>',
    ]
    params = {'format': ' <red>|</red> '.join(format_values), 'backtrace': False, 'diagnose': False}

    logger.remove()
    logger.add(
        sys.stdout,
        **params,
    )
    logger.add(
        log_dir / 'today.log',
        rotation='00:00',
        retention='1 week',
        compression='zip',
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
