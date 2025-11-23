from .base import *

print("⚠️ Using SQLite in CI mode")

DEBUG = False  # это CI, не dev

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.db.sqlite3",
    }
}

# Celery runs synchronously in CI
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "cache+memory://"
CELERY_TASK_ALWAYS_EAGER = True

# Disable strong password validators to speed CI
AUTH_PASSWORD_VALIDATORS = []
