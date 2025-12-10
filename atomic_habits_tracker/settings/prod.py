from corsheaders.defaults import default_headers

from .base import *

DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["backend"])

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

TELEGRAM_BIND_URL = env("TELEGRAM_BIND_URL", default="http://backend:8000/api/telegram/bind/")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("POSTGRES_HOST", default="postgres"),
        "PORT": env("POSTGRES_PORT", default=5432),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "NAME": env("POSTGRES_DB"),
    }
}

REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_PORT = env("REDIS_PORT", default=6379)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=f"redis://{REDIS_HOST}:{REDIS_PORT}/1")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Security
USE_HTTPS = env.bool("USE_HTTPS", default=False)
SECURE_SSL_REDIRECT = USE_HTTPS
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env("JWT_ACCESS_LIFETIME", default=15)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env("JWT_REFRESH_LIFETIME", default=7)),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}


# Logging
LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING["handlers"]["file"] = {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": LOG_DIR / "django.log",
    "maxBytes": 10 * 1024 * 1024,  # 10 MB
    "backupCount": 5,
    "formatter": "verbose",
}
LOGGING["root"]["handlers"] = ["console","file"]
