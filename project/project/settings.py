import hashlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
     hashlib.sha1(os.urandom(128)).hexdigest(), 
)

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

INTERNAL_IPS = os.environ.get('INTERNAL_IPS', 'localhost 127.0.0.1').split() 

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'dashboard',
    'corsheaders',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Apparently not used
# WSGI_APPLICATION = 'wsgi.application'

from . import database

DATABASES = {
    'default': database.config()
}

# Notes for running postgres in a docker containor for devel
# https://hub.docker.com/_/postgres/
# docker pull postgres:9.4.11
# docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres:9.4.11
# docker run -it --rm --link some-postgres:postgres postgres:9.4.11 psql -h postgres -U postgres

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_verbose': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_verbose_prod': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'dashboard': {
            'handlers': ['console_verbose'],
            'level': 'INFO',
            'filters': ['require_debug_true']
        },
        'dashboard_prod': {
            'handlers': ['console_verbose_prod'],
            'level': 'ERROR',
            'filters': ['require_debug_false']
        },
    }
}

OPENSHIFT_API = {
  'POC': {
      'OPENSHIFT_MASTER': os.environ.get('OPENSHIFT_MASTER_POC', 'unknown'),
      'API_TOKEN': os.environ.get('API_TOKEN_POC', 'unknown'),
      'display': 'POC',
      'build_endpoint': '/oapi/v1/buildconfigs',
  },
  'NP': {
      'OPENSHIFT_MASTER': os.environ.get('OPENSHIFT_MASTER_NP', 'unknown'),
      'API_TOKEN': os.environ.get('API_TOKEN_NP', 'unknown'),
      'display': 'Non-Prod',
      'build_endpoint': '/oapi/v1/buildconfigs',
  },
  'PRD': {
      'OPENSHIFT_MASTER': os.environ.get('OPENSHIFT_MASTER_PRD', 'unknown'),
      'API_TOKEN': os.environ.get('API_TOKEN_PRD', 'unknown'),
      'display': 'Production',
      'build_endpoint': '/oapi/v1/buildconfigs',
  },
}

REMOVE_SLASH = True
CORS_ORIGIN_ALLOW_ALL = True

USING_CELERY = os.environ.get('USING_CELERY', 'no') == 'yes'
# CELERY STUFF
CELERY_BROKER_URL = 'redis://' + os.environ.get('REDIS_SERVER', 'localhost') + ':6379'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# vim: ai et ts=4 sw=4 sts=4
