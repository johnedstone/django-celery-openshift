import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    service_name = os.getenv('DATABASE_SERVICE_NAME', 'some-postgres').upper().replace('-', '_')
    if service_name:
        engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['postgresql'])
    else:
        engine = engines['postgresql']
    name = os.getenv('DATABASE_NAME', 'postgres_db')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('DATABASE_USER', 'postgres_user'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'mysecretpassword'),
        'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name), 'localhost'),
        'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name), '5432'),
    }

# vim: ai et ts=4 sw=4 sts=4 nu
