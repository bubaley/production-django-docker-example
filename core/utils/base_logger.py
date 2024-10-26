import sys

from loguru import logger

from core.settings import common

format_values = [
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>',
    '<level>{level: <8}</level>',
    '{message}',
    '<cyan>{file.name}<red>:</red>{function}<red>:</red>{line}</cyan>',
]
_format = ' <red>|</red> '.join(format_values)

logger.remove()
logger.add(sys.stdout, format=_format)
logger.add(
    common.BASE_DIR / 'data' / 'logs' / 'today.log',
    format=_format,
    rotation='00:00',
    retention='1 week',
    compression='zip',
    backtrace=True,
    diagnose=True,
)
