import os

from django.core.asgi import get_asgi_application

from core.settings import common

os.environ.setdefault('DJANGO_SETTINGS_MODULE', common.SETTINGS_MODULE)

application = get_asgi_application()
