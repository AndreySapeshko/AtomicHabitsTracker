# Архитектура проекта: Atomic Habits Tracker

## 1. Общее описание

Atomic Habits Tracker — это фуллстек-приложение для трекинга привычек с глубокой интеграцией с Telegram.

Проект состоит из трёх основных частей:

1. **Backend (Django + DRF + Celery + Redis + PostgreSQL)**  
2. **Telegram-бот (Aiogram 3, отдельный worker)**  
3. **Frontend (React + Vite + TypeScript)**

Каждая часть изолирована, но связана через чётко определённые интерфейсы (HTTP API, Redis, JWT-токены).

---

## 2. Общая схема системы

Высокоуровневая схема компонентов:

- **Клиент (браузер)**  
  - React + Vite + TS
  - JWT авторизация
  - Общение с backend по HTTP (REST API)

- **Backend (Django + DRF)**  
  - Авторизация и управление пользователями (`CustomUser`)
  - CRUD для привычек (`Habit`)
  - Инстансы привычек (`HabitInstance`)
  - Telegram-профиль (`TelegramProfile`)
  - API для аналитики и статистики
  - Публичные привычки
  - Кэширование статистики в Redis
  - Генерация инстансов через Celery beat

- **Telegram-бот (Aiogram 3)**  
  - Асинхронный бот в отдельном процессе
  - DI-архитектура (Sender + Formatter + API клиент)
  - Команды для просмотра привычек, задач, статистики
  - Управление статусами `HabitInstance`
  - Привязка Telegram-профиля к пользователю

- **Инфраструктура**  
  - PostgreSQL — основная БД
  - Redis — кэш + брокер для Celery + канал общения с ботом
  - Celery worker + Celery beat — фоновые задачи и планировщик
  - Nginx — обратный прокси и статика
  - Docker — контейнеризация всех сервисов

---

## 3. Backend

### 3.1. Технологии

- **Django** — основной web-фреймворк
- **Django REST Framework (DRF)** — реализация REST API
- **PostgreSQL** — реляционная база данных
- **Redis** — кэш и брокер задач
- **Celery** — фоновая обработка и планирование задач
- **DRF Spectacular (планируется)** — генерация API-спеки (OpenAPI/Swagger)

### 3.2. Основные модели

- **CustomUser**
  - Логин по `email`
  - `username` отключён
  - Используется во всех связях (`Habit.user`, `TelegramProfile.user`)

- **Habit**
  - `action` — что делать
  - `place` — где
  - `time_of_day` — время суток (morning/evening/…)
  - `is_pleasant` — приятная или полезная привычка
  - `related_pleasant_habit` — ссылка на приятную привычку, если текущая — полезная
  - `reward_text` — текст награды
  - `periodicity_days` — периодичность (1, 2, 3, 5, 7)
  - `repeat_limit` — ограничение (21, 30, 45)
  - `grace_minutes`, `fix_minutes` — дедлайны (автоматически считаются)
  - `is_public` — публичная привычка
  - `is_active` — активна или нет
  - `created_at` — дата создания  
  - **Валидации**:
    - Если `is_pleasant = True` → нельзя указывать `reward_text` или `related_pleasant_habit`
    - Если `is_pleasant = False` → должно быть либо `reward_text`, либо `related_pleasant_habit`

- **HabitInstance**
  - `habit` — ссылка на Habit
  - `scheduled_datetime` — запланированное время
  - `status` — статус выполнения:
    - `scheduled`
    - `pending`
    - `completed`
    - `completed_late`
    - `missed`
    - `fix_expired`
  - Методы:
    - `mark_completed()`
    - `mark_failed()`

- **TelegramProfile**
  - Связь пользователя с Telegram
  - telegram_id, username
  - код для привязки/подтверждения

### 3.3. Основные API-модули

- **Auth API**
  - `/auth/register`
  - `/auth/login`
  - `/auth/me`
  - JWT авторизация

- **Habit API**
  - CRUD для привычек
  - Логика фильтрации по пользователю
  - Валидация pleasant/useful привычек

- **HabitInstance API**
  - Список инстансов
  - Инстансы по привычке
  - Инстансы на сегодня (`/today`)
  - Статусы меняются не через API, а через Telegram или автоматические дедлайны

- **Stats / Analytics API**
  - `/habits/{id}/stats/` — статистика по привычке:
    - streak (current, max)
    - total (count, completed, missed)
    - pie data (по статусам)
    - weekly data (для bar chart)
  - Кэширование результатов в Redis

- **Public Habits API**
  - `/public` — список публичных привычек:
    - только `is_public = True`
    - только `is_active = True`
    - исключаем привычки текущего пользователя

### 3.4. Celery и фоновые задачи

- **Celery beat**:
  - Раз в день генерирует `HabitInstance` на основе `Habit.periodicity_days`
  - Учитывает `repeat_limit`
  - Ставит дедлайны (grace/fix)
  - При необходимости отправляет уведомления в Telegram (через Redis)

- **Celery worker**:
  - Выполняет задачи генерации
  - Обновляет кэш статистики
  - Служит связкой между Django и Telegram-ботом (через Redis)

---

## 4. Telegram-бот (Aiogram 3)

### 4.1. Технологии

- **Aiogram 3.x** — асинхронный Telegram-фреймворк
- Архитектура на основе **Router** и **Handler**
- Внедрение зависимостей (DI):
  - Sender — единая точка отправки сообщений
  - Formatter — форматирование текста, блоков, кнопок
  - API-клиент — запросы к Django backend

### 4.2. Основные команды

- `/start` — приветствие и базовая информация
- `/help` — список команд и возможностей
- `/profile` — профиль пользователя + состояние привязки Telegram
- `/habits` — список привычек
- `/today` — задания на сегодня
- `/habit_<id>` — детали конкретной привычки
- `/stats_<id>` — статистика привычки
- `/bind` — привязка Telegram к аккаунту
- `/unbind` — отвязка Telegram

### 4.3. Inline-кнопки

- Кнопки управления инстансами:
  - выполнить
  - пропустить
  - отменить выполнение (если предусмотрено)
- Кнопки навигации:
  - детали привычки
  - статистика
  
### 4.4. Связь с Django

- Бот не ходит напрямую в базу данных
- Использует HTTP API и Redis:
  - HTTP для запросов к backend (получение привычек, инстансов, статистики)
  - Redis для:
    - обмена событиями
    - возможной pub/sub-модели уведомлений
- Изменение статуса `HabitInstance` происходит через Telegram:
  - пользователь нажимает кнопку
  - бот отправляет запрос к backend
  - backend обновляет статус и инвалидирует кеш статистики

---

## 5. Frontend (React + Vite + TypeScript)

### 5.1. Технологии

- **React** + **TypeScript**
- **Vite** — сборщик
- **Zustand** — стейт-менеджмент для авторизации и, при необходимости, других сущностей
- **React Router** — роутинг
- **Recharts** — графики и диаграммы
- CSS/стили:
  - современный UI
  - grid-layout для карточек
  - единый стиль по всему приложению

### 5.2. Основные страницы

- `/login` — логин
- `/register` — регистрация
- `/habits` — список привычек
- `/habits/create` — создание привычки
- `/habits/:id` — детали привычки
- `/habits/:id/edit` — редактирование
- `/habits/:id/instances` — инстансы привычки
- `/habits/:id/analytics` — аналитика (streak, прогресс, графики)
- `/public` — публичные привычки других пользователей
- `/today` — задачи на сегодня
- `/profile` — профиль пользователя + Telegram bind

### 5.3. Авторизация

- JWT (`access` + `refresh`)
- **Zustand**:
  - хранит `access` и `refresh` токены
  - синхронизация с `localStorage`
- **axios apiClient**:
  - добавляет `Authorization: Bearer <access>` во все запросы
  - при `401`:
    - очищает токены
    - делает redirect на `/login`

### 5.4. UI/UX

- Единый стиль карточек
- Адаптивный дизайн
- Аккуратная типографика
- Блоки:
  - streak
  - прогресс-бар
  - pie chart
  - weekly bar chart
- Разумные empty-состояния:
  - “Пока нет привычек”
  - “Пока нет публичных привычек”
  - “На сегодня заданий нет”

---

## 6. Кэширование и аналитика

### 6.1. Redis

- Используется для:
  - кэширования статистики по привычке
  - обмена сообщениями между Django и Telegram
  - потенциально для rate limiting и других задач

### 6.2. Кэш статистики

- При запросе `/habits/{id}/stats/`:
  - сначала пробуем взять данные из Redis
  - если кэша нет — считаем статистику, сохраняем в Redis, возвращаем клиенту

- Инвалидация:
  - при изменении `Habit` (например, смена периодичности)
  - при изменении `HabitInstance` (выполнение/пропуск)

---

## 7. Поток данных (user journey)

1. Пользователь регистрируется и логинится через frontend
2. Создаёт полезные и приятные привычки
3. Celery ежедневно создаёт `HabitInstance`
4. Пользователь:
   - видит задачи на сегодня в веб-интерфейсе (`/today`)
   - получает уведомления через Telegram
5. Отмечает выполнение привычек через Telegram-бота
6. Backend обновляет статусы инстансов, пересчитывает / инвалидирует кэш
7. Пользователь видит прогресс и аналитику на `/habits/:id/analytics`
8. Пользователь может делиться своими привычками как публичными (`/public`)

---

## 8. Тестирование

Проект покрыт тестами на всех уровнях:

- **Backend (pytest + pytest-django)**:
  - модели (`Habit`, `HabitInstance`, `TelegramProfile`)
  - API (auth, habits, instances, stats, public)
  - Celery-задачи
  - кеш статистики

- **Telegram (Aiogram 3 + pytest-asyncio)**:
  - команды
  - callback-кнопки
  - привязка Telegram
  - Sender + Formatter
  - интеграция с backend через моки

- **Frontend (Vitest + React Testing Library + MSW)**:
  - компоненты
  - страницы
  - Zustand store
  - API client (axios interceptors)
  - интеграция с backend через mock-сервер

---

## 9. Дальнейшее развитие

- Webhook режим для Telegram (вместо long polling)
- Полная OpenAPI-документация (DRF Spectacular)
- Улучшенная аналитика (heatmap, календарь привычек)
- Дополнительные интеграции (например, email-уведомления)

