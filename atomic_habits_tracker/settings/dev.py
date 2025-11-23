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

CORS_ALLOW_ALL_ORIGINS = True
