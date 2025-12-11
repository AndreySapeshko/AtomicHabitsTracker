from pathlib import Path

import environ
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

# Загружаем .env ТОЛЬКО если он существует
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY", default="unsafe-secret")

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

WEB_APP_URL = "https://sapeshkoas.ru"

# ---------------------------
# Applications
# ---------------------------

INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_celery_beat",
    "django-extensions",
    # Project apps
    "users",
    "habits",
    "habit_instances",
    "telegrambot",
    "core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "atomic_habits_tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "atomic_habits_tracker.wsgi.application"
ASGI_APPLICATION = "atomic_habits_tracker.asgi.application"

# ---------------------------
# Database in base.py NOT defined!
# (each environment has its own)
# ---------------------------

DATABASES = {}

# ---------------------------
# Password validation
# ---------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

AUTH_USER_MODEL = "users.User"

# ---------------------------
# CSRF
# ---------------------------


# ---------------------------
# Static & Media
# ---------------------------

USE_X_FORWARDED_HOST = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------
# DRF
# ---------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ---------------------------
# SPECTACULAR
# ---------------------------

SPECTACULAR_SETTINGS = {
    "TITLE": "Atomic Habits Tracker API",
    "DESCRIPTION": "API для трекера привычек",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [{"BearerAuth": []}],
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY_DEFINITIONS": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
}

# ---------------------------
# Redis
# ---------------------------


# ---------------------------
# Celery (base defaults, override in env-specific settings)
# ---------------------------

CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False

# CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
# CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/1")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "generate_daily_instances_every_midnight": {
        "task": "habit_instances.tasks.generate_daily_instances",
        "schedule": crontab(minute=0, hour=0),  # каждый день в 00:00
    },
}

# ---------------------------
# Logging (base, override in prod)
# ---------------------------

# LOG_DIR = Path(BASE_DIR) / "logs"
# os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] {name}: {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {  # всё, у чего нет своего логгера
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "habit": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "habit_instances": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "users": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.worker": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "telegrambot": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# ---------------------------
# Telegram
# ---------------------------

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", default=None)
TELEGRAM_BIND_URL = env("TELEGRAM_BIND_URL", default="http://testserver/api/telegram/bind/")
