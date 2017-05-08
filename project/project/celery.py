'''Celery 4.x
    Reference: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
'''
from __future__ import absolute_import, unicode_literals

import os
import time

from celery import Celery
from celery.decorators import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django
django.setup()

app = Celery(__name__)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True, name="hitchhiker")
def get_answer(self):
    time.sleep(5)
    logger.info('The answer is: {}'.format(42))
    return 42

# Too complicated right now to move to dashboard.tasks
@app.task(bind=True, name="add_bc")
def add_bc(self):
    from dashboard.views import _populate_build_config_objects as populate_bc
    populate_bc()
    logger.info('attempted to populate db with bc')
    return 'attempted to populate db with bc'

@app.task()
@periodic_task(
    run_every=(crontab(minute=5, hour=0)),
    name="add_bc_periodic",
    ignore_result=True
)
def add_bc_periodic():
    from dashboard.views import _populate_build_config_objects as populate_bc
    import django
    django.setup()
    populate_bc()
    logger.info('attempted to populate db with bc')
    return 'attempted to populate db with bc'

# vim: ai et ts=4 sw=4 sts=4 ru nu
