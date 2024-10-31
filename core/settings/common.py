# https://github.com/bubaley/production-django-docker-example
# version: 1.0.5 | Increase the version after changes from the template, this will make it easier to make new ones

import datetime
import sys
from pathlib import Path

import environ

from core.utils.logger import init_logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env.bool('DEBUG', True)
TESTING = sys.argv[1:2] == ['test']
SETTINGS_MODULE = 'core.settings.dev' if DEBUG else 'core.settings.prod'
SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOST', default=['*'])
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=['http://localhost:8080'])

LOGGING = init_logging(log_dir=BASE_DIR / 'data' / 'logs', debug=DEBUG)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'user',
    'django_extensions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

if env.str('SQL_ENGINE', None):
    DATABASES = {
        'default': {
            'ENGINE': env.str('SQL_ENGINE'),
            'NAME': env.str('SQL_DATABASE'),
            'USER': env.str('SQL_USER'),
            'PASSWORD': env.str('SQL_PASSWORD'),
            'HOST': env.str('SQL_HOST'),
            'PORT': env.str('SQL_PORT'),
            'TEST': {
                'NAME': 'test_' + env.str('SQL_DATABASE'),  # database for tests
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'data' / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False

STATICFILES_DIRS = [Path(BASE_DIR / 'data' / 'static')]
STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / 'data' / 'media'
MEDIA_URL = 'media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_PAGINATION_CLASS': 'core.utils.pagination.BasePagination',
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
}

AUTH_USER_MODEL = 'user.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False

CACHE_LOCATION_URL = env.str('CACHE_LOCATION_URL', None)
backends = 'django.core.cache.backends'
CACHES = {
    'default': {
        'BACKEND': f'{backends}.redis.RedisCache' if CACHE_LOCATION_URL else f'{backends}.db.DatabaseCache',
        'LOCATION': CACHE_LOCATION_URL or 'app_cache',
        'TIMEOUT': 86400 * 7,  # 7 days
    }
}

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', None)
CELERY_BACKEND_URL = env.str('CELERY_BACKEND_URL', None)

# --- CUSTOM_SETTINGS ---
