import os

from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atomic_habits_tracker.settings.dev")

# Создание экземпляра объекта Celery
app = Celery("atomic_habits_tracker")

# Загрузка настроек из файла Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
