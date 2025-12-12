# Docker Infrastructure — Atomic Habits Tracker

Проект Atomic Habits Tracker полностью контейнеризован с помощью Docker и Docker Compose.  
Это обеспечивает:

- единое окружение для разработки и продакшена
- изоляцию сервисов
- простое масштабирование
- воспроизводимость сборки

---

## 1. Общая схема контейнеров

Проект состоит из следующих контейнеров:

| Контейнер | Назначение |
|-----------|------------|
| `backend` | Django + DRF API |
| `frontend` | Сборка React/Vite |
| `telegrambot` | Aiogram 3 бот |
| `celery_worker` | Celery worker |
| `celery_beat` | Celery beat |
| `redis` | Кэш и брокер задач |
| `postgres` | Основная БД |
| `nginx` | Reverse-proxy, HTTPS, статика |

---

## 2. Структура Docker-файлов

Рекомендуемая структура:
```
AtomicHabitsTracker/
├── docker/
│ ├── backend/
│ │ └── Dockerfile
│ ├── frontend/
│ │ └── Dockerfile
│ ├── telegrambot/
│ │ └── Dockerfile
│ └── nginx/
│ └── Dockerfile
│
├── docker-compose.yml
└── .env
```

---

## 3. Dockerfile: Backend (Django)

Контейнер backend выполняет:

- запуск Django
- миграции
- сборку статики
- обслуживание API

Основные этапы:

- установка Python
- установка зависимостей через poetry
- копирование проекта
- запуск gunicorn / uvicorn

---

## 4. Dockerfile: Frontend (React + Vite)

Контейнер frontend выполняет только:

- сборку production-версии (`npm run build`)

После сборки:

- папка `dist/` прокидывается в nginx

---

## 5. Dockerfile: Telegram Bot

Контейнер telegrambot выполняет:

- запуск aiogram 3 бота
- обработку long polling или webhook
- работу с Redis и Backend API

---

## 6. Dockerfile: Nginx

Nginx выполняет:

- отдачу frontend статики
- проксирование запросов к backend
- SSL-терминацию
- проксирование Telegram webhook

---

## 7. Docker Compose (docker-compose.yml)

Основной файл оркестрации:

Сервисы:

- postgres
- redis
- backend
- celery_worker
- celery_beat
- telegrambot
- frontend
- nginx

Типовые зависимости:

- backend зависит от postgres и redis
- celery_worker зависит от backend и redis
- celery_beat зависит от backend и redis
- telegrambot зависит от backend и redis
- nginx зависит от backend и frontend

---

## 8. Сети и тома

### Сети:

- `backend_network` — связь backend, celery, redis, postgres
- `frontend_network` — связь nginx и frontend

### Тома:

- `postgres_data` — данные БД
- `redis_data` — данные Redis
- `static_volume` — Django статика
- `media_volume` — пользовательские файлы

---

## 9. Переменные окружения в Docker

Все сервисы используют переменные из `.env`:

- база данных
- redis
- celery
- telegram
- jwt
- frontend api url

Никакие секреты не хранятся в Dockerfile.

---

## 10. Запуск проекта в Docker

Запуск всех контейнеров:

`docker compose up -d --build`

Остановка:

`docker compose down`

Пересборка без кеша:

`docker compose build --no-cache`

---

## 11. Работа с миграциями

Применение миграций:

`docker compose exec backend python manage.py migrate`

Создание суперпользователя:

`docker compose exec backend python manage.py createsuperuser`

Сборка статики:

`docker compose exec backend python manage.py collectstatic`

---

## 12. Логи контейнеров

Просмотр логов:
```
docker compose logs -f backend
docker compose logs -f celery_worker
docker compose logs -f telegrambot
```
---

## 13. Production-особенности

В production режиме:

- используется gunicorn/uvicorn
- выключен DEBUG
- включён Nginx
- включён HTTPS
- используется внешний домен
- Telegram работает через webhook

---

## 14. Итог

Docker-инфраструктура Atomic Habits Tracker обеспечивает:

- раздельные сервисы
- безопасную конфигурацию
- масштабируемость
- удобный локальный и production-запуск
- готовность к CI/CD

Проект полностью готов к деплою в облаке или на собственном сервере.
