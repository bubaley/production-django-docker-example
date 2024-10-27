from .common import *

SENTRY_DSN = env.str('SENTRY_DSN', None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        integrations=[DjangoIntegration()],
        dsn=SENTRY_DSN,
        environment=env.str('SENTRY_ENV', 'production'),
        traces_sample_rate=0.0,
        send_default_pii=True,
    )
