if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}

python manage.py migrate
# django-admin compilemessages -l ru --ignore=env
gunicorn core.wsgi:application --forwarded-allow-ips="*" --timeout=300 --workers=$GUNICORN_WORKERS --bind 0.0.0.0:8000
