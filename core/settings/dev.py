from .common import *

STATIC_DIR = root('static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

USE_SILK = env.bool('USE_SILK', False)

if USE_SILK:
    INSTALLED_APPS.append('silk.apps.SilkAppConfig')
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
