# Environment Variables — Atomic Habits Tracker

В проекте Atomic Habits Tracker все чувствительные данные и конфигурации выносятся в файл `.env`.  
Это необходимо для безопасности, гибкости деплоя и поддержки нескольких окружений (dev, prod, ci).

Файл `.env` не хранится в репозитории. Для примера используется `env.example`.

---

## 1. Общие переменные проекта

| Переменная | Назначение |
|------------|------------|
| `ENV` | Тип окружения: dev / prod / ci |
| `DEBUG` | Включение режима отладки |
| `SECRET_KEY` | Секретный ключ Django |

Пример:
```
ENV=dev
DEBUG=True
SECRET_KEY=super-secret-key
```

---

## 2. Django Settings

| Переменная | Назначение |
|------------|------------|
| `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Домены для CORS |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Источники для CSRF |

Пример:
```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:5173
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:5173
```

---

## 3. База данных (PostgreSQL)

| Переменная | Назначение |
|------------|------------|
| `POSTGRES_DB` | Имя базы данных |
| `POSTGRES_USER` | Пользователь БД |
| `POSTGRES_PASSWORD` | Пароль БД |
| `POSTGRES_HOST` | Хост БД |
| `POSTGRES_PORT` | Порт БД |

Пример:
```
POSTGRES_DB=atomic_habits
POSTGRES_USER=atomic_user
POSTGRES_PASSWORD=atomic_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

## 4. Redis

| Переменная | Назначение |
|------------|------------|
| `REDIS_HOST` | Хост Redis |
| `REDIS_PORT` | Порт Redis |
| `REDIS_DB` | Номер БД |

В .env не включены, установлены в sittings.dev settings.prod settings.ci
в соответствии с режимом запуска.

---

## 5. Celery

| Переменная | Назначение |
|------------|------------|
| `CELERY_BROKER_URL` | URL брокера (Redis) |
| `CELERY_RESULT_BACKEND` | Backend результатов |
| `CELERY_ACCEPT_CONTENT` | Типы данных |
| `CELERY_TASK_SERIALIZER` | Сериализация задач |
| `CELERY_TIMEZONE` | Таймзона |

В .env не включены, установлены в sittings.base и settings.ci
в соответствии с режимом запуска.


---

## 6. JWT

| Переменная | Назначение |
|------------|------------|
| `JWT_ACCESS_LIFETIME` | Время жизни access токена |
| `JWT_REFRESH_LIFETIME` | Время жизни refresh токена |

Пример:
```
JWT_ACCESS_LIFETIME=15
JWT_REFRESH_LIFETIME=7
```

(Минимальные значения в минутах / днях соответственно.)

Используются в режиме prod и применяются в settings.prod.

В режиме dev используются настройки по умолчанию.

---

## 7. Telegram Bot

| Переменная | Назначение |
|------------|------------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота |
| `TELEGRAM_WEBHOOK_URL` | URL webhook (production) |
| `TELEGRAM_USE_WEBHOOK` | Включение webhook |
| `TELEGRAM_ADMIN_ID` | ID администратора |

Пример:
```
TELEGRAM_BOT_TOKEN=123456:ABCDEF
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook/
TELEGRAM_USE_WEBHOOK=True
TELEGRAM_ADMIN_ID=88005553535
```

---

## 8. Frontend (Vite)

Frontend использует собственные переменные окружения:

| Переменная | Назначение |
|------------|------------|
| `VITE_API_URL` | URL backend API |
| `VITE_TELEGRAM_BOT_URL` | Ссылка на Telegram-бота |

Пример:
```
VITE_API_URL=http://127.0.0.1:8000/api/
VITE_TELEGRAM_BOT_URL=https://t.me/atomic_habits_bot
```

---

## 9. Production-переменные

Дополнительные переменные для боевого окружения:

| Переменная | Назначение |
|------------|------------|
| `DJANGO_SECURE_SSL_REDIRECT` | Редирект на HTTPS |
| `DJANGO_SESSION_COOKIE_SECURE` | Secure cookies |
| `DJANGO_CSRF_COOKIE_SECURE` | Secure CSRF |
| `DJANGO_HSTS_SECONDS` | Strict-Transport-Security |

Пример:
```
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_HSTS_SECONDS=31536000
```

---

## 10. CI/CD

Используется в GitHub Actions:

| Переменная | Назначение |
|------------|------------|
| `CI` | Флаг CI-окружения |
| `TEST_DATABASE_URL` | Тестовая БД |
| `TEST_REDIS_URL` | Тестовый Redis |

Пример:
```
CI=True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.db.sqlite3",
    }
}
TEST_REDIS_URL=redis://localhost:6379/1
```
---

## 11. env.example

В репозитории обязательно должен присутствовать файл:

env.example

markdown
Копировать код

Он содержит:

- все используемые переменные
- пустые или тестовые значения
- комментарии

Это необходимо для быстрого разворачивания проекта новыми разработчиками.

---

## 12. Итог

Файл `.env` является центральной точкой конфигурации проекта и управляет:

- Django
- PostgreSQL
- Redis
- Celery
- Telegram Bot
- JWT
- Frontend
- Production безопасностью
- CI/CD

Корректная настройка `.env` — обязательное условие успешного деплоя и стабильной работы проекта.
