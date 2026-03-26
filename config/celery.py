from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

import config.settings

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Настройка периодических задач
app.conf.beat_schedule = {
    'deactivate-inactive-users-monthly': {
        'task': 'users.tasks.deactivate_inactive_users',
        'schedule': crontab(day_of_month='1', hour='3', minute='0'),  # 1-го числа каждого месяца в 3:00
    },
}
app.conf.timezone = config.settings.TIME_ZONE