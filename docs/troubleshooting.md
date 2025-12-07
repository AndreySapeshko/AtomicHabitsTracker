# Troubleshooting — Atomic Habits Tracker

В этом документе собраны наиболее частые проблемы, которые могут возникнуть при разработке, тестировании и деплое проекта Atomic Habits Tracker, а также способы их устранения.

---

## 1. Backend (Django)

### 1.1. Ошибка: Django не запускается

Симптомы:

- контейнер backend падает сразу после старта
- в логах ошибка SECRET_KEY или DEBUG

Решение:

- проверить наличие переменных в `.env`:
  - SECRET_KEY
  - DEBUG
- проверить, что `.env` действительно подхватывается docker-compose

---

### 1.2. Ошибка: 500 Internal Server Error

Симптомы:

- API возвращает 500
- Swagger не открывается

Решение:

- посмотреть логи:
docker compose logs -f backend

- проверить миграции:
docker compose exec backend python manage.py migrate

- проверить подключение к PostgreSQL

---

### 1.3. Ошибка: CSRF / CORS

Симптомы:

- frontend не может отправить POST
- ошибка CORS в браузере

Решение:

- проверить переменные:
- DJANGO_CORS_ALLOWED_ORIGINS
- DJANGO_CSRF_TRUSTED_ORIGINS
- убедиться, что домен frontend совпадает

---

## 2. PostgreSQL

### 2.1. Ошибка подключения к БД

Симптомы:

- OperationalError: could not connect to server

Решение:

- проверить переменные:
```
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```
- убедиться, что контейнер postgres запущен:
`docker compose ps`

---

### 2.2. Потеря данных

Симптомы:

- база данных пустая после перезапуска

Решение:

- проверить volume postgres_data
- убедиться, что volume не удаляется при `docker compose down`

---

## 3. Redis

### 3.1. Celery не получает задачи

Симптомы:

- задачи не выполняются
- нет логов в celery_worker

Решение:

- проверить Redis:
`docker compose logs -f redis`
- проверить:
`REDIS_HOST`
`REDIS_PORT`
- проверить `CELERY_BROKER_URL`

---

## 4. Celery

### 4.1. Celery worker не стартует

Симптомы:

- контейнер celery_worker падает

Решение:

- проверить:
```
CELERY_BROKER_URL
CELERY_RESULT_BACKEND
```
- убедиться, что Redis доступен
- проверить импорты задач

---

### 4.2. Celery beat не создаёт инстансы

Симптомы:

- HabitInstance не создаются автоматически

Решение:

- проверить контейнер celery_beat:
`docker compose logs -f celery_beat`
- проверить celerybeat-schedule
- убедиться, что задача зарегистрирована

---

## 5. Telegram Bot

### 5.1. Бот не отвечает

Симптомы:

- бот не реагирует на команды
- нет сообщений

Решение:

проверить: `TELEGRAM_BOT_TOKEN`

проверить режим:
* long polling
* webhook
* посмотреть логи:
`docker compose logs -f telegrambot`

---

### 5.2. Webhook не работает

Симптомы:

- бот не получает события
- Telegram пишет WebHook is not set

Решение:

проверить:
- `TELEGRAM_USE_WEBHOOK`
- `TELEGRAM_WEBHOOK_URL`
- убедиться, что Nginx проксирует webhook
- перезапустить контейнер telegrambot

---

### 5.3. Проблемы с привязкой Telegram

Симптомы:

- bind-код не принимается
- профиль не создаётся

Решение:

- проверить TelegramProfile в БД
- проверить API `/telegram/bind/`
- проверить валидность bind_code

---

## 6. Frontend

### 6.1. Frontend не может подключиться к API

Симптомы:

- ошибка Network Error
- нет данных

Решение:

проверить:
- `VITE_API_URL`
- убедиться, что backend доступен по этому адресу
- проверить CORS

---

### 6.2. JWT не сохраняется

Симптомы:

- после логина сразу logout

Решение:

- проверить localStorage
- проверить Zustand store
- проверить axios-интерцептор

---

### 6.3. Ошибки сборки Vite

Симптомы:

- npm run build падает

Решение:

- проверить TypeScript-ошибки
- проверить импорты
- проверить версии зависимостей

---

## 7. Docker

### 7.1. Контейнеры не стартуют

Симптомы:

- docker compose up падает

Решение:

- проверить .env
- проверить свободное место на диске
- выполнить:
`docker system prune -f`

---

### 7.2. Конфликт портов

Симптомы:

- address already in use

Решение:

- проверить, что порты 80, 443, 8000, 5432, 6379 свободны
- при необходимости изменить маппинг портов

---

## 8. Nginx и HTTPS

### 8.1. HTTPS не работает

Симптомы:

- сайт доступен только по HTTP

Решение:

- проверить certbot
- проверить сертификаты
- проверить конфигурацию Nginx
- выполнить:
`sudo certbot renew`

---

### 8.2. 502 Bad Gateway

Симптомы:

- сайт открывается, но API нет

Решение:

- проверить backend контейнер
- проверить proxy_pass в nginx
- проверить внутренние порты

---

## 9. Swagger / OpenAPI

### 9.1. Swagger не открывается

Симптомы:

- 404 на /api/docs/swagger/

Решение:

- проверить, что drf_spectacular в `INSTALLED_APPS`
- проверить urls.py
- перезапустить backend

---

## 10. CI/CD

### 10.1. Тесты падают в GitHub Actions

Симптомы:

- ошибки PostgreSQL
- ошибки Redis

Решение:

- проверить сервисы databases в workflow
- проверить `TEST_DATABASE_URL`
- проверить `TEST_REDIS_URL`

---

### 10.2. Деплой по SSH не проходит

Симптомы:

- Permission denied
- Host unreachable

Решение:

- проверить `SSH_KEY`
- проверить `SSH_HOST`
- проверить `SSH_USER`
- проверить firewall

---

## 11. Итог

Документ troubleshooting позволяет:

- быстро диагностировать проблемы
- устранить типовые ошибки
- сократить время простоя
- повысить надёжность production-системы

При сложных ситуациях рекомендуется: 

- включать детальные логи
- проверять Redis, PostgreSQL, Celery
- смотреть все docker-логи
- проверять переменные окружения
