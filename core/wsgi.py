import os

from django.core.wsgi import get_wsgi_application

from core.settings import common

os.environ.setdefault('DJANGO_SETTINGS_MODULE', common.SETTINGS_MODULE)

application = get_wsgi_application()
