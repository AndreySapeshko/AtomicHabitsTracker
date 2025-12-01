from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default=5432),
        "USER": env("POSTGRES_USER", default="my_user"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="my_password"),
        "NAME": env("POSTGRES_DB", default="atomic_habits_tracker"),
    }
}

REDIS_HOST = env("REDIS_HOST", default="localhost")
REDIS_PORT = env("REDIS_PORT", default=6379)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

# CELERY_WORKER_LOG_FILE = None  # Отключаем файловые логи Celery
# CELERY_WORKER_REDIRECT_STDOUTS = False  # Не перенаправлять stdout
# CELERY_WORKER_HIJACK_ROOT_LOGGER = False  # Не перехватывать root logger
