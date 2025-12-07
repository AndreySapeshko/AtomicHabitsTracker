# Backend Documentation — Atomic Habits Tracker

Backend проекта реализован на Django + DRF с использованием Celery, Redis и PostgreSQL.  
Этот документ описывает структуру backend-кода, логику приложений, потоки данных, интеграции и обработку фоновых задач.

---

# 1. Общая архитектура backend

Backend расположен в директории:

atomic_habits_tracker/

markdown
Копировать код

Он представляет собой модульное Django-приложение, разделённое на независимые домены:

| Директория             | Назначение |
|------------------------|------------|
| `settings/`            | конфигурация Django, Celery, ASGI/WSGI |
| `core/`                | общие утилиты, middleware, base-классы |
| `users/`               | пользователи, авторизация, JWT |
| `habits/`              | модели привычек, CRUD, правила валидации |
| `habit_instances/`     | генерация, хранение и управление инстансами привычек |
| `telegrambot/`         | интеграция с Telegram (webhook/polling, API, связи) |
| `docs/`                | документация backend → (этот файл здесь) |
| `logs/`                | логирование Celery/Django |

Инфраструктура:

- **PostgreSQL** — основная база данных
- **Redis** — кеш и брокер сообщений для Celery
- **Celery worker + Celery beat** — фоновые задачи и планировщик
- **Nginx** (на продакшене) — терминатор SSL и reverse-proxy

---

## 2. Django Settings

Настройки проекта организованы в модульной структуре:

- atomic_habits_tracker/settings/
- base.py — базовые настройки для всех окружений
- dev.py — настройки для разработки
- prod.py — настройки продакшена
- ci.py — настройки для CI/CD (GitHub Actions, тесты)
- urls.py — корневой роутинг
- celery.py — конфигурация Celery
- asgi.py — ASGI-приложение
- wsgi.py — WSGI-приложение
- init.py — автоподключение настроек и Celery

markdown
Копировать код

### Архитектура конфигурации

#### `base.py`
Содержит все общие настройки:

- INSTALLED_APPS
- DATABASES
- AUTH_USER_MODEL
- REST_FRAMEWORK
- CACHES (Redis)
- CELERY настройки
- STATIC/MEDIA
- прочие параметры

#### `dev.py`
Наследуется от base.py и включает:

- `DEBUG = True`
- расширенный логирование
- настройки разработки
- локальные override-переменные

#### `prod.py`
Боевые настройки:

- `DEBUG = False`
- PostgreSQL
- Redis как кеш
- HTTPS/SECURE параметры
- CORS/CSRF периметр безопасности
- отключённый Django Debug Toolbar

#### `ci.py`
Используется при запуске тестов:

- выключено или уменьшено логирование
- тестовая БД
- отключение фоновых задач Celery

---

## 3. Приложение `users/`

Расположено в:

atomic_habits_tracker/users/

markdown
Копировать код

Содержит:

- модель кастомного пользователя `User`
- сериализаторы и схемы регистрации/логина
- JWT аутентификацию
- эндпоинты `/auth/register`, `/auth/login`, `/auth/me`

> ⚠️ **Примечание:**  
> Хотя модель называется `User`, это **полностью кастомная модель**, заменяющая `django.contrib.auth.models.User`.  
> Для ясности мы будем называть её `CustomUser` в документации.

---

## 3.1. Модель CustomUser (User)

Особенности:

- логин происходит по **email**
- поле `username` отключено
- совместима с Django Permissions/Groups
- используется в:
  - Habit.user  
  - TelegramProfile.user  
  - Auth API  

Поля модели:

| Поле | Тип | Описание |
|------|------|----------|
| `email` | EmailField | уникальный логин, обязательное поле |
| `password` | CharField | хэшируемый пароль |
| `is_active` | Boolean | активность пользователя |
| `is_staff` | Boolean | доступ в админку |
| `date_joined` | DateTime | дата регистрации |
| дополнительные поля (при необходимости) |

---

## 3.2. API аутентификации

| Метод | Путь | Описание |
|--------|--------|-------------|
| POST | `/auth/register/` | регистрация нового пользователя |
| POST | `/auth/login/` | выдача JWT токенов |
| GET | `/auth/me/` | получить информацию о текущем пользователе |

Используемые токены: **access** и **refresh**  
Хранятся на frontend в Zustand и автоматически добавляются в каждый запрос через axios-interceptors.

---

# 4. Приложение `habits/`

Расположено в:

atomic_habits_tracker/habits/

markdown
Копировать код

Содержит:

- модель `Habit`
- CRUD API
- бизнес-валидации
- публичные привычки (`/public/`)

## 4.1. Модель Habit

Ключевые поля:

- `action`
- `place`
- `time_of_day`
- `is_pleasant`
- `reward_text`
- `related_pleasant_habit`
- `periodicity_days` — 1, 2, 3, 5, 7
- `repeat_limit` — 21, 30, 45
- `grace_minutes`, `fix_minutes`
- `is_public`
- `is_active`

## 4.2. Правила валидации

**Приятная привычка** (`is_pleasant = True`)  
✔ нельзя иметь `reward_text`  
✔ нельзя иметь `related_pleasant_habit`

**Полезная привычка** (`is_pleasant = False`)  
✔ должна иметь либо:
- `reward_text`, либо
- `related_pleasant_habit`  
✘ нельзя иметь оба поля одновременно

## 4.3. Публичные привычки (`/public/`)

Выдаются привычки:

- `is_public=True`

---

# 5. Приложение `habit_instances/`

Расположено в:

atomic_habits_tracker/habit_instances/

markdown
Копировать код

Отвечает за:

- модель `HabitInstance`
- статусы выполнения
- API эндпоинты:
  - инстансы по привычке
  - инстансы за сегодня (`/today/`)
- изменение статусов (через Telegram или Celery)

## 5.1. Статусы HabitInstance

Определены в `HabitInstanceStatus`:

- `scheduled`
- `pending`
- `completed`
- `completed_late`
- `missed`
- `fix_expired`

## 5.2. Методы

| Метод | Описание |
|--------|----------|
| `mark_completed()` | отмечает выполнение, учитывает дедлайны |
| `mark_failed()` | отмечает пропуск (missed или fix_expired) |

## 5.3. Логика работы `/today/`

Возвращает список инстансов на текущий день:

- отфильтровано по пользователю
- сортировка по времени
- включает только активные привычки

---

# 6. Приложение `telegrambot/`

Расположено в:

atomic_habits_tracker/telegrambot/

markdown
Копировать код

Содержит:

- модель `TelegramProfile`
- обработку привязки Telegram к аккаунту
- API для бота (если нужно)
- сервисы общения через Redis

## 6.1. TelegramProfile

Поля:

- `user`
- `telegram_id`
- `telegram_username`
- `bind_code` — код привязки
- `is_bound`

Привязка происходит так:

1. Пользователь открывает `/profile` в вебе → жмёт "сгенерировать код"
2. На странице отображается `bind_code`
3. В Telegram вводит `/bind`
4. Отправляет код → бот связывает TelegramID с CustomUser

## 6.2. Интеграция Django ↔ Telegram Bot

Через Redis:

- события отправляются в канал (pub/sub)
- Celery может уведомлять бота о новых инстансах
- Telegram-бот может обновлять статусы через API

---

# 7. Celery (worker + beat)

Файл конфигурации:

atomic_habits_tracker/settings/celery.py

markdown
Копировать код

## 7.1. Celery Beat

Отвечает за периодические задачи:

- **ежедневная генерация HabitInstance**
- очистка старых кэшей
- проверка дедлайнов
- возможное уведомление бота

## 7.2. Celery Worker

Отвечает за:

- обработку задач генерации
- установку статусов (если автоматическое выполнение)
- обновление статистики
- отправку событий в Redis

---

# 8. Redis

Redis используется для двух задач:

## 8.1. Кэш статистики Habit

- При запросе `/habits/<id>/stats/`
- Результаты вычислений кешируются в Redis
- Структура кеша:

habit_stats:<habit_id>

markdown
Копировать код

### Инвалидация происходит при:

- изменении Habit
- изменении HabitInstance
- генерации новых инстансов

## 8.2. Канал связки Django ↔ Telegram

Используется для:

- уведомлений боту
- синхронизации состояний

---

# 9. Статистика и аналитика

API `/habits/<id>/stats/` предоставляет:

- streak (current, max)
- выполнено / пропущено
- pie-chart по статусам
- weekly bar chart по дням недели
- проценты успешности

### Архитектура:

stats_service.py
├── получает инстансы из БД
├── вычисляет статистику
├── сохраняет результат в Redis
└── возвращает клиенту

yaml
Копировать код

---

# 10. Логирование

Каталог:

atomic_habits_tracker/logs/

yaml
Копировать код

Используется для:

- Celery worker logs
- Celery beat logs
- Django error logs
- HTTP-запросов (если включено)

---

# 11. Тестирование backend

Используется:

- pytest
- pytest-django
- pytest-asyncio (telegram tests)

Покрыто тестами:

| Раздел | Покрытие |
|--------|----------|
| Модели habits | ✔ |
| Модели habit_instances | ✔ |
| Модели telegrambot | ✔ |
| CRUD API | ✔ |
| Public API | ✔ |
| Stats API | ✔ |
| Celery tasks | ✔ |
| Redis caching | ✔ |
| Telegram bot ↔ backend | ✔ |

---

# 12. Поток данных (жизненный цикл привычки)

1. Пользователь создаёт привычку  
2. Celery beat создаёт ежедневные инстансы  
3. Пользователь получает уведомление через Telegram  
4. Выполняет задание → статус обновляется в Django  
5. Redis-инвалидация статистики  
6. Фронтенд показывает обновлённую аналитику  

---

# 13. Точки расширения

Backend легко расширить:

- webhook для Telegram вместо long polling
- дополнительные виды аналитики (heatmap, календарь)
- напоминания по email/SMS
- интеграции с Apple Watch / Google Fit
- social feed публичных привычек

---

# 14. Итог

Backend Atomic Habits Tracker представляет собой:

- чистую модульную архитектуру
- разделение доменов (`habits`, `habit_instances`, `users`, `telegrambot`)
- устойчивый сервисный слой
- продуманную бизнес-валидацию
- фоновые процессы через Celery
- кеширование Redis
- продакшен-готовую интеграцию с Telegram

```md