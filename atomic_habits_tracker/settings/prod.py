from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "NAME": env("POSTGRES_DB"),
    }
}

REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_PORT = env("REDIS_PORT", default=6379)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING["handlers"]["file"] = {
    "level": "INFO",
    "class": "logging.FileHandler",
    "filename": env("DJANGO_LOG_FILE", default="/app/logs/django.log"),
}
LOGGING["root"]["handlers"] = ["file"]
