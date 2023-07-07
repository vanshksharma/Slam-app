import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SLAM_APP.settings")
app = Celery("SLAM_APP")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()