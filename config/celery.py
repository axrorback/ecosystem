from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import task_prerun, task_postrun
from django.db import close_old_connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@task_prerun.connect
def celery_prerun(*args, **kwargs):
    close_old_connections()

@task_postrun.connect
def celery_postrun(*args, **kwargs):
    close_old_connections()