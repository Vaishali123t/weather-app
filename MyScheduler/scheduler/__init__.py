from flask import Flask
from celery import Celery
from datetime import timedelta

from firebase_connect import get_users
from weather import getweather
from mail import send_email

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config['CELERY_BACKEND'] = "redis://redis:6379/0"
app.config['CELERY_BROKER_URL'] = "redis://redis:6379/0"

app.config['CELERYBEAT_SCHEDULE'] = {
    'say-every-5-seconds': {
        'task': 'send_mail',
        'schedule': timedelta(seconds=5)
    },
}

app.config['CELERY_TIMEZONE'] = 'UTC'
celery_app = make_celery(app)

@celery_app.task(name='send_mail')
def send_mail():
    users=get_users()
    for user in users:
        weather = getweather(user[1])
        if weather:
            send_email(user[0],weather)
    return 'Sent'
