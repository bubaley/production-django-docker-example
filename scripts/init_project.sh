uv add Django \
      django-cors-headers \
      django-environ \
      djangorestframework \
      djangorestframework-simplejwt \
      loguru \
      requests \
      sentry-sdk \
      gunicorn \
      air-drf-relation \
      django-filter \
      redis \
      celery \
      "psycopg[binary]"
uv add ruff pre-commit --group dev
pre-commit install
