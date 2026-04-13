import os
from celery import Celery

# Вказуємо Django налаштування за замовчуванням для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental.settings')

app = Celery('car_rental')

# Використовуємо рядок із префіксом 'CELERY_', щоб не плутати з іншими налаштуваннями Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Шукаємо файли tasks.py у всіх додатках проекту
app.autodiscover_tasks()