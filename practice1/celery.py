from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'practice1.settings')
app = Celery('practice1')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'every-minute': {
        'task': 'User.tasks.health_check_task',
        'schedule': crontab(),
    },
    'every-day': {
        'task': 'User.tasks.list_user_signed_up_today_task',
        'schedule': crontab(minute='*/5'),
    },
}
app.conf.timezone = 'UTC'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
