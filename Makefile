ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif

timestamp = $(shell date +"%Y-%m-%d %H:%M:%S.%3N")
log = echo $(call timestamp) $(1)
wait-for = $(call log,"👀$(2) waiting...") && wait-for $(1) && $(call log,"☑️$(2) ready")

MANAGE := python manage.py
DOCKER_COMPOSE := docker compose

GUNICORN_WORKERS ?= 4
CELERY_CONCURRENCY ?= 4
CELERY_BEAT_ENABLED ?= false
CELERY_BEAT_FLAG = $(if $(filter true True TRUE,$(CELERY_BEAT_ENABLED)),-B,)

# ----------- SHORT COMMANDS ----------- #

r: run ## short run runserver
m: migrate ## short run migrate
mm: makemigrations ## short run makemigrations
mr: migrate run ## short run migrate && runserver

# ----------- BASE COMMANDS ----------- #

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

test: ## run tests
	$(MANAGE) test --keepdb

coverage: ## run coverage
	coverage run manage.py test --keepdb
	coverage report

gunicorn: ## run gunicorn
	gunicorn core.wsgi:application --forwarded-allow-ips="*" --timeout=60 --workers=$(GUNICORN_WORKERS) --bind 0.0.0.0:8000 --preload

celery: ## run celery workers with beat
	celery -A core worker $(CELERY_BEAT_FLAG) -E -n worker --loglevel=INFO --concurrency=$(CELERY_CONCURRENCY)

compilemessages: ## run compilemessages
	@$(call log, "💬 Compiling messages...")
	django-admin compilemessages -l ru --ignore=env
	@$(call log, "✅ Messages compiled")

collectstatic: ## run compilemessages
	@$(call log, "📂 Collecting static files...")
	python manage.py collectstatic --noinput
	@$(call log, "✅ Static files collected")

# ----------- PRODUCTION COMMANDS ----------- #

prod-migrate: ## run migrate in production
	@$(call wait-for, db:5432, Postgres)
	@$(call wait-for, redis:6379, Redis)

	@$(call log, "🎯 Running migrations...")
	$(MANAGE) migrate
	@$(call log, "✅ Migrations completed")

# prod-gunicorn: prod-migrate collectstatic compilemessages ## run gunicorn in production with compilemessages
prod-gunicorn: collectstatic prod-migrate ## run gunicorn in production
	@$(call log, "🚀 Starting gunicorn...")
	gunicorn core.wsgi:application --forwarded-allow-ips="*" --timeout=60 --workers=$(GUNICORN_WORKERS) --bind 0.0.0.0:8000 --preload --max-requests 1000 --max-requests-jitter 50

prod-celery: prod-migrate ## run celery in production
	@$(call log, "💣 Starting celery...")
	celery -A core worker $(CELERY_BEAT_FLAG) -E -n worker --loglevel=INFO --concurrency=$(CELERY_CONCURRENCY)

# ----------- HELPERS ----------- #

secret: ## generate secret_key
	@python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key().replace('#', '+'))"

help:
	@echo "Usage: make <target>"
	@awk 'BEGIN {FS = ":.*##"} /^[0-9a-zA-Z_-]+:.*?## / { printf "  * %-20s -%s\n", $$1, $$2 }' $(MAKEFILE_LIST)
