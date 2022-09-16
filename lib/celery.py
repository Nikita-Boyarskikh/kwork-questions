import os
from celery import Celery
from celery.schedules import crontab
from constance.signals import config_updated
from django.dispatch import receiver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'change_questions_status': {
        'task': 'questions.tasks.publish_questions',
        'schedule': crontab(hour=3, minute=0),
    }
}


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    if key == 'PUBLISH_QUESTION_COUNTDOWN_HOURS':
        app.conf.beat_schedule['change_questions_status']['schedule'] = new_value
