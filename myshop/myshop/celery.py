import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#response = app.control.enable_events(reply = True)
#app.broker_connection_retry_on_startup(True)