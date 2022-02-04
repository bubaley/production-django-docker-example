from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

STATIC_DIR = root('static')
STATIC_ROOT = root('static')

SENTRY_DSN = env.str('SENTRY_DSN', None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
