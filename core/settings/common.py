import datetime
import environ
from loguru import logger

env = environ.Env()
environ.Env.read_env()
root = environ.Path(__file__) - 3
BASE_DIR = root()

logger.add(f'{BASE_DIR}/logs/today.log',
           rotation='00:00',
           compression='tar.gz',
           format='{time:YYYY-MM-DD HH:mm} | {level} | {message} | {file.path}:{function}')

SECRET_KEY = env.str('SECRET_KEY', 'secret_key')
ALLOWED_HOSTS = env.list('ALLOWED_HOST', default=['*'])
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=['http://localhost:8080'])
DEBUG = env.bool('DEBUG', default=True)

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
    'user',
    'django_filters',
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
        'DIRS': [root('templates')],
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
        }
    }
else:
    DATABASES = {
        'default': env.db_url('DATABASE_URL', 'sqlite:///' + root('db.sqlite3'))
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
USE_L10N = True
USE_TZ = False
LOCALE_PATHS = [
    'core/locale',
]

STATIC_URL = '/static/'
STATIC_PATH = root('static')
MEDIA_URL = '/media/'
MEDIA_ROOT = root('media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_PAGINATION_CLASS': 'core.utils.pagination.MainPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
}

AUTH_USER_MODEL = 'user.User'

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB_NUMBER = env.int('REDIS_DB_NUMBER', 0)
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + f'/{REDIS_DB_NUMBER}'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + f'/{REDIS_DB_NUMBER}'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'app_cache',
        'TIMEOUT': 604800
    }
}
