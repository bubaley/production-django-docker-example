ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif

MANAGE := python manage.py
DOCKER_COMPOSE := docker compose

GUNICORN_WORKERS ?= 4
CELERY_CONCURRENCY ?= 4
CELERY_BEAT_ENABLED ?= false
CELERY_BEAT_FLAG = $(if $(filter true True TRUE,$(CELERY_BEAT_ENABLED)),-B,)

# ----------- SHORT COMMANDS -----------

r: run ## short run runserver
m: migrate ## short run migrate
mm: makemigrations ## short run makemigrations
mr: migrate run ## short run migrate && runserver

# ----------- BASE COMMANDS -----------

run: ## run runserver
	$(MANAGE) runserver

shell: ## run shell_plus
	$(MANAGE) shell_plus

lint: ## run lint
	pre-commit run --all-files

migrate: ## run migrate
	$(MANAGE) migrate

makemigrations: ## run makemigrations
	$(MANAGE) makemigrations

createsuperuser: ## run createsuperuser
	$(MANAGE) createsuperuser

test: ## run test --keepdb
	$(MANAGE) test --keepdb

coverage: ## run coverage
	coverage run manage.py test --keepdb
	coverage report

gunicorn: ## run gunicorn
	gunicorn core.wsgi:application --forwarded-allow-ips="*" --timeout=300 --workers=$(GUNICORN_WORKERS) --bind 0.0.0.0:8000

celery: ## run celery workers with beat
	celery -A core worker $(CELERY_BEAT_FLAG) -E -n worker --loglevel=INFO --concurrency=$(CELERY_CONCURRENCY)

compilemessages: ## run compilemessages
	@echo "💬 Compiling messages..."
	django-admin compilemessages -l ru --ignore=env

collectstatic: ## run compilemessages
	@echo "📌 Collecting static files..."
	python manage.py collectstatic --noinput

secret: ## generate secret_key
	@python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key().replace('#', '+'))"

# ----------- PRODUCTION COMMANDS -----------

prod-migrate: ## run migrate in production
	@echo "📦 Waiting for services..."
	@wait-for db:5432 -- echo "Postgres ready"
	@wait-for redis:6379 -- echo "Redis ready"
	@echo "⚙️ Running migrations"
	$(MANAGE) migrate


# prod-gunicorn: prod-migrate collectstatic compilemessages ## run gunicorn in production with compilemessages
prod-gunicorn: collectstatic prod-migrate ## run gunicorn in production
	@echo "🚀 Starting gunicorn..."
	$(MAKE) gunicorn

prod-celery: prod-migrate ## run celery in production
	@echo "💣 Starting celery..."
	$(MAKE) celery

help:
	@echo "Usage: make <target>"
	@awk 'BEGIN {FS = ":.*##"} /^[0-9a-zA-Z_-]+:.*?## / { printf "  * %-20s -%s\n", $$1, $$2 }' $(MAKEFILE_LIST)
