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

USE_TELEGRAM_BOT = False
TELEGRAM_BOT_TOKEN = "ci-dummy-token"
TELEGRAM_BIND_URL = "http://testserver/api/telegram/bind/"
USE_REDIS = False

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

# Disable strong password validators to speed CI
AUTH_PASSWORD_VALIDATORS = []
