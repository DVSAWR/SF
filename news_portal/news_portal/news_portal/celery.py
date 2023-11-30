
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')



app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.send_last_weekly_list',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
app.autodiscover_tasks()



