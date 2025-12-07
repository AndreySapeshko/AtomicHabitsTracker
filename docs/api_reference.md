# API Reference — Atomic Habits Tracker (v1)

Данный документ описывает REST API backend-сервиса Atomic Habits Tracker.  
API используется веб-клиентом (React), Telegram-ботом и любыми внешними интеграциями.

---

## 1. Общая информация

Все методы API доступны по базовому URL:

http://<server>/api/

markdown
Копировать код

### 1.1. Формат данных

- Все запросы — `application/json`
- Все ответы — `application/json`
- Часовые зоны — UTC
- Даты и время в формате ISO 8601:

2025-01-31T09:00:00Z

yaml
Копировать код

---

### 1.2. Аутентификация (JWT)

Используются два токена:

- **access токен** — короткоживущий  
- **refresh токен** — длительный для обновления access токена

Оба токена выдаются при `/auth/login/`.

Access токен необходимо передавать в каждом запросе:

Authorization: Bearer <access>

yaml
Копировать код

Если access токен просрочен, фронтенд вызывает refresh или выполняет logout.

---

### 1.3. Формат ошибок

Все ошибки возвращаются следующим образом:

```json
{
  "detail": "Ошибка"
}
```
Или список ошибок по полям:
```
{
  "email": ["Пользователь с таким email уже существует"],
  "password": ["Слишком короткий пароль"]
}
```
Коды ошибок:

Код	Значение
- 400	Некорректные данные
- 401	Неавторизован
- 403	Нет доступа
- 404	Не найдено
- 409	Конфликт
- 500	Ошибка сервера

### 1.4. Версии API
Текущая версия: v1

Пока использует стабильные эндпоинты:

/api/...    (без versioning в URL)

## 2. Auth API

Эндпоинты регистрации, логина и получения информации о пользователе.

### 2.1. POST /auth/register/

Регистрирует нового пользователя.

Тело запроса:
```
{
  "email": "user@mail.com",
  "password": "stringpassword"
}
```
Успешный ответ:
```
{
  "id": 5,
  "email": "user@mail.com"
}
```
Возможные ошибки:

- email уже существует

- неправильный формат email

- слишком простой/короткий пароль

### 2.2. POST /auth/login/

Авторизация пользователя и получение JWT токенов.

Тело запроса:
```
{
  "email": "user@mail.com",
  "password": "stringpassword"
}
```
Успешный ответ:
```
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```
Ошибки:

- неверный пароль

- пользователь не существует

- пользователь деактивирован

### 2.3. GET /auth/me/

Получение информации о текущем пользователе.
Требует авторизации через Bearer access токен.

Пример запроса:

`Authorization: Bearer <token>
`

Успешный ответ:
```
{
  "id": 5,
  "email": "user@mail.com",
  "date_joined": "2025-01-25T10:15:43Z"
}
```
Ошибки:

401 — токен просрочен или отсутствует


---
## 3. Habits API

Эндпоинты для работы с привычками пользователя: создание, редактирование, удаление, получение списка, публикация и привязка наград.

Все методы требуют авторизации, кроме публичного списка привычек.

Базовый путь:

/api/habits/

yaml
Копировать код

---

## 3.1. GET /habits/

Получить список всех привычек текущего пользователя.

### Пример успешного ответа:

```json
[
  {
    "id": 12,
    "action": "Drink water",
    "place": "Kitchen",
    "time_of_day": "morning",
    "is_pleasant": false,
    "reward_text": "Take a 5-minute break",
    "related_pleasant_habit": null,
    "periodicity_days": 1,
    "repeat_limit": 21,
    "is_public": true,
    "is_active": true,
    "created_at": "2025-01-31T09:22:00Z"
  }
]
```
### 3.2. POST /habits/
Создание новой привычки.

Тело запроса:
```
{
  "action": "Drink water",
  "place": "Kitchen",
  "time_of_day": "morning",
  "is_pleasant": false,
  "reward_text": "Watch YouTube 5 minutes",
  "related_pleasant_habit": null,
  "periodicity_days": 1,
  "repeat_limit": 21,
  "is_public": true
}
```
Успешный ответ:
```
{
  "id": 15,
  "action": "Drink water",
  "is_pleasant": false
}
```
Ошибки:
- полезная привычка должна иметь либо reward_text, либо related_pleasant_habit

- приятная привычка не может иметь награду

- periodicity_days вне разрешённых значений

### 3.3. GET /habits/{id}/
Получить детальную информацию о привычке.

Пример ответа:

```
{
  "id": 12,
  "action": "Drink water",
  "place": "Kitchen",
  "time_of_day": "morning",
  "is_pleasant": false,
  "reward_text": "Watch YouTube",
  "periodicity_days": 1,
  "repeat_limit": 21,
  "is_public": false,
  "created_at": "2025-01-31T09:22:00Z"
}
```
Ошибки:

404 — привычка не найдена или не принадлежит пользователю

### 3.4. PATCH /habits/{id}/
Изменение привычки (частичное обновление).

Пример запроса:
```
{
  "place": "Office",
  "reward_text": "Drink coffee"
}
```
Пример успешного ответа:
```
{
  "id": 12,
  "place": "Office",
  "reward_text": "Drink coffee"
}
```
Ошибки:
- правила валидации pleasant/useful

- нельзя сделать полезную привычку pleasant без изменения других полей

### 3.5. DELETE /habits/{id}/
Удаляет привычку.

Все связанные HabitInstance удаляются каскадно.

Пример успешного ответа:
```
{
  "status": "deleted"
}
```
### 3.6. GET /habits/public/
Публичные привычки других пользователей.

Используется на frontend в разделе /public.

Пример ответа:
```
[
  {
    "id": 77,
    "action": "Meditate",
    "is_pleasant": true,
    "periodicity_days": 1
  },
  {
    "id": 91,
    "action": "Read 10 pages",
    "is_pleasant": false,
    "reward_text": "Play 10 minutes",
    "periodicity_days": 1
  }
]
```
Публичные привычки:

- не содержат приватных данных

- не включают место выполнения и time_of_day

- показываются всем

### 3.7. GET /habits/{id}/related/
Получение списка приятных привычек, которые могут использоваться как награды.

Используется в формах создания/редактирования полезной привычки.

Пример ответа:
```
[
  {
    "id": 40,
    "action": "Drink coffee",
    "is_pleasant": true
  },
  {
    "id": 41,
    "action": "Eat chocolate",
    "is_pleasant": true
  }
]
```
### 3.8. Особенности работы Habit API
1. Валидация pleasant/useful
Система строго проверяет:

- приятные привычки не могут иметь reward_text

- полезные обязаны иметь награду

- нельзя указать обе награды одновременно

2. Автоматический расчёт временных параметров
Backend определяет:

- grace_minutes

- fix_minutes

основанные на time_of_day и общих правилах.

3. Инвалидация кэша статистики
При любом изменении Habit:

- обновлении

- удалении

- кэш статистики привычки очищается.

## 4. HabitInstance API

Эндпоинты HabitInstance отвечают за ежедневные задания, выполнение, пропуски, просмотр инстансов и получение списка задач на сегодня.

Базовый путь:

/api/habit-instances/

yaml
Копировать код

---

## 4.1. GET /habit-instances/

Получение списка всех инстансов текущего пользователя.

Используется редко (обычно используются фильтры или конкретная привычка).

### Пример ответа:

```json
[
  {
    "id": 3001,
    "habit": 12,
    "scheduled_datetime": "2025-02-01T09:00:00Z",
    "status": "pending"
  }
]
```
### 4.2. GET /habit-instances/today/
Список инстансов, запланированных на сегодня.

Используется:

- на frontend странице /today

- в Telegram-боте по команде /today

Пример ответа:
```
[
  {
    "id": 3001,
    "habit": {
      "id": 12,
      "action": "Drink water",
      "time_of_day": "morning"
    },
    "status": "pending",
    "scheduled_datetime": "2025-02-01T09:00:00Z"
  }
]
```
### 4.3. GET /habits/{habit_id}/instances/
Получение всех инстансов конкретной привычки.

Используется на странице /habits/:id/instances.

Пример ответа:
```
[
  {
    "id": 3000,
    "status": "completed",
    "scheduled_datetime": "2025-01-31T09:00:00Z"
  },
  {
    "id": 3001,
    "status": "pending",
    "scheduled_datetime": "2025-02-01T09:00:00Z"
  }
]
```
### 4.4. GET /habit-instances/{id}/
Получение полной информации об одном инстансе.

Пример ответа:
```
{
  "id": 3001,
  "habit": {
    "id": 12,
    "action": "Drink water",
    "is_pleasant": false
  },
  "scheduled_datetime": "2025-02-01T09:00:00Z",
  "status": "pending",
  "completed_at": null
}
```
### 4.5. POST /habit-instances/{id}/complete/
Отметить выполнение инстанса.

Backend автоматически определяет правильный статус:

- completed

- completed_late

- fix_expired

Логика зависит от grace_minutes и fix_minutes привычки.

Пример успешного ответа:
```
{
  "id": 3001,
  "status": "completed",
  "completed_at": "2025-02-01T09:05:12Z"
}
```
Возможные ошибки:
- 409 — уже выполнено

- 409 — fix-период истёк

- 404 — инстанс не найден

### 4.6. POST /habit-instances/{id}/miss/
Принудительно отметить инстанс как пропущенный.

Используется в Telegram-боте кнопкой «Пропустить».

Пример успешного ответа:
```
{
  "id": 3001,
  "status": "missed"
}
```
### 4.7. POST /habit-instances/{id}/cancel/
Отменить выполнение и вернуть статус в pending.

Используется в Telegram («Отменить выполнение»).

Успешный ответ:
```
{
  "id": 3001,
  "status": "pending"
}
```
### 4.8. Автоматическое обновление статусов (Celery)
Celery периодически обновляет инстансы, чьи дедлайны истекли:

- если истёк grace → missed

- если истёк fix → fix_expired

Эндпоинтов для этого нет — это фоновая логика.

### 4.9. Особенности HabitInstance API
1. Проверка прав доступа
Инстанс принадлежит привычке, которая принадлежит пользователю.
Пользователь может изменять только свои инстансы.

2. Авто-инвалидация кэш статистики
При любом изменении статуса инстанса:

- выполнить

- пропустить

- отменить выполнение

- кэш статистики привычки очищается.

3. Telegram-first API
4. 
Инстансы часто используются через Telegram, поэтому:

- все ответы короткие

- статусы всегда актуальные

- ошибки максимально информативные

## 5. Statistics API

Эндпоинты статистики используются для получения аналитики по привычкам и общей активности пользователя.  
Все методы требуют авторизации.

Базовый путь:

/api/stats/

yaml
Копировать код

---

## 5.1. GET /habits/{habit_id}/stats/

Получение полной статистики по конкретной привычке.

Используется:

- на frontend странице аналитики привычки  
- в Telegram-боте по команде `/stats_<id>`

### Пример успешного ответа:

```json
{
  "habit_id": 12,
  "total_instances": 21,
  "completed": 16,
  "completed_late": 2,
  "missed": 2,
  "fix_expired": 1,
  "success_rate": 76.19,
  "current_streak": 5,
  "max_streak": 9,
  "weekly_distribution": {
    "completed": 2,
    "missed": 3
  },
  "status_distribution": {
    "completed": 16,
    "completed_late": 2,
    "missed": 2,
    "fix_expired": 1
  }
}
```
### 5.2. GET /stats/summary/
Получение общей сводной статистики по всем привычкам пользователя.

Используется на главной странице приложения.

Пример ответа:
```
{
  "total_habits": 6,
  "active_habits": 5,
  "total_instances": 128,
  "total_completed": 97,
  "total_missed": 19,
  "total_fix_expired": 12,
  "overall_success_rate": 75.78,
  "best_habit": {
    "id": 12,
    "action": "Drink water",
    "success_rate": 88.4
  },
  "worst_habit": {
    "id": 19,
    "action": "Meditate",
    "success_rate": 52.1
  }
}
```
### 5.3. GET /habits/{habit_id}/streak/
Получение только информации о streak для конкретной привычки.

Используется в:

- streak-блоках на frontend

- быстрых Telegram-ответах

Пример ответа:
```
{
  "habit_id": 12,
  "current_streak": 5,
  "max_streak": 9
}
```
### 5.4. Кэширование статистики
Статистика привычек кэшируется в Redis для ускорения ответов.

Кэш используется для:

- /habits/{id}/stats/

- /habits/{id}/streak/

### 5.5. Инвалидация кэшa
Кэш статистики сбрасывается автоматически при:

- выполнении инстанса (complete)

- пропуске инстанса (miss)

- отмене выполнения (cancel)

- создании нового HabitInstance (Celery)

- редактировании Habit

- удалении Habit

После инвалидации статистика пересчитывается при следующем запросе.

5.6. Вычисляемые показатели
Statistics API рассчитывает следующие метрики:

- общее количество инстансов

- количество выполненных вовремя

- количество выполненных с опозданием

- количество пропущенных

- процент успешности

- текущий streak

- максимальный streak

- распределение по статусам (pie chart)

- количество выполненных и пропущенных за неделю (bar chart)

### 5.7. Использование в Telegram-боте
Статистика используется в Telegram-командах:

- /stats_<habit_id> — детальная аналитика привычки

- краткие streak-сообщения после выполнения привычек

- уведомления о рекордах streak

Ответы оптимизированы для быстрого текстового отображения.

## 6. Telegram API

Telegram API используется Telegram-ботом для привязки аккаунта, получения данных пользователя, просмотра привычек, инстансов и статистики, а также для изменения статусов HabitInstance.

Часть эндпоинтов является публичной, часть — используется только Telegram-ботом как internal API.

Базовый путь:

- /api/telegram/



---

## 6.1. POST /telegram/bind/

Привязка Telegram-пользователя к аккаунту Django по одноразовому коду.

Используется Telegram-ботом после команды `/bind`.

### Тело запроса:

```json
{
  "bind_code": "A7K9Q2",
  "telegram_id": 88005553535,
  "telegram_username": "habits_master"
}
```
Успешный ответ:
```
{
  "status": "ok"
}
```
Возможные ошибки:
- неверный bind_code

- код уже использован

- пользователь деактивирован

### 6.2. POST /telegram/unbind/
Отвязка Telegram-аккаунта от пользователя.

Используется командой /unbind.

Тело запроса:
```
{
  "telegram_id": 88005553535
}
```
Успешный ответ:
```
{
  "is_active" = False
}
```
### 6.3. GET /telegram/profile/
Получение профиля TelegramProfile, связанного с telegram_id.

Параметры запроса:
* Параметр:	telegram_id	
* Тип:	integer	
* Описание: ID пользователя Telegram

Пример ответа:
```
{
  "id": 3,
  "user": 7,
  "telegram_id": 88005553535,
  "telegram_username": "habits_master",
  "is_bound": true
}
```
### 6.4. GET /telegram/habits/
Получение списка привычек пользователя через Telegram.

Используется в командах:

- /habits

- /habit_<id>

Пример ответа:
```
[
  {
    "id": 12,
    "action": "Drink water",
    "is_pleasant": false,
    "time_of_day": "morning",
    "periodicity_days": 1
  }
]
```
### 6.5. GET /telegram/today/
Получение списка заданий на сегодня для Telegram.

- Используется командой /today.

Пример ответа:
```
[
  {
    "id": 3001,
    "habit_id": 12,
    "action": "Drink water",
    "status": "pending",
    "scheduled_datetime": "2025-02-01T09:00:00Z"
  }
]
```
### 6.6. POST /telegram/habit-instances/{id}/complete/
Отметить выполнение инстанса через Telegram.

- Используется inline-кнопкой «Выполнить».

Пример ответа:
```
{
  "id": 3001,
  "status": "completed"
}
```
### 6.7. POST /telegram/habit-instances/{id}/miss/
Отметить инстанс как пропущенный через Telegram.

- Используется кнопкой «Пропустить».

Пример ответа:
```
{
  "id": 3001,
  "status": "missed"
}
```
### 6.8. POST /telegram/habit-instances/{id}/cancel/
Отмена выполнения (возврат в pending).

- Используется кнопкой «Отменить».

Пример ответа:
```
{
  "id": 3001,
  "status": "pending"
}
```
### 6.9. GET /telegram/stats/{habit_id}/
Получение краткой статистики привычки для Telegram.

Используется командой:

- /stats_<habit_id>

Пример ответа:
```
{
  "current_streak": 12,
  "max_streak": 5,
  "total_completed": 9,
  "total_missed": 7,
  "total_pending": 5
}
```
### 6.10. Внутренние события через Redis
Telegram-бот получает события от backend через Redis:

- создание новых HabitInstance

- изменение статуса инстанса

- сброс статистики

Эти события не имеют HTTP-эндпоинтов и используются только для push-уведомлений.

### 6.11. Ограничения безопасности
- Все Telegram-эндпоинты требуют проверки telegram_id.

- Бот не имеет доступа к данным других пользователей.

- Все операции проходят проверку связки TelegramProfile ↔ User.

## 7. Примеры запросов и типовые ошибки

В этом разделе приведены типовые сценарии использования API, а также примеры стандартных ошибок, которые может возвращать backend.

---

## 7.1. Полный поток: регистрация → логин → создание привычки → получение заданий

### 1. Регистрация пользователя

POST /auth/register/

```json
{
  "email": "test@mail.com",
  "password": "strongpassword123"
}
```
Ответ:

```
{
  "id": 10,
  "email": "test@mail.com"
}
```
2. Логин пользователя
POST /auth/login/

```
{
  "email": "test@mail.com",
  "password": "strongpassword123"
}
```
Ответ:

```
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```
3. Создание привычки
POST /habits/

- Заголовок:

```
Authorization: Bearer <access>
```
- Тело запроса:

```
{
  "action": "Drink water",
  "place": "Kitchen",
  "time_of_day": "morning",
  "is_pleasant": false,
  "reward_text": "Watch YouTube 5 minutes",
  "periodicity_days": 1,
  "repeat_limit": 21,
  "is_public": true
}
```
- Ответ:

```
{
  "id": 15,
  "action": "Drink water",
  "is_pleasant": false
}
```
4. Получение заданий на сегодня
GET /habit-instances/today/

Ответ:

```
[
  {
    "id": 3010,
    "habit": {
      "id": 15,
      "action": "Drink water"
    },
    "status": "pending",
    "scheduled_datetime": "2025-02-01T09:00:00Z"
  }
]
```
5. Выполнение задания
POST /habit-instances/3010/complete/

Ответ:

```
{
  "id": 3010,
  "status": "completed",
  "completed_at": "2025-02-01T09:03:14Z"
}
```
### 7.2. Пример ошибок валидации Habit
Ошибка: полезная привычка без награды
POST /habits/

```
{
  "action": "Read book",
  "is_pleasant": false,
  "periodicity_days": 1
}
```
Ответ (400):

```
{
  "detail": "Useful habit must have reward_text or related_pleasant_habit."
}
```
Ошибка: приятная привычка с наградой
```
{
  "action": "Drink coffee",
  "is_pleasant": true,
  "reward_text": "Eat chocolate",
  "periodicity_days": 1
}
```
Ответ (400):

```
{
  "detail": "Pleasant habit cannot have reward_text or related_pleasant_habit."
}
```
### 7.3. Ошибки авторизации
Отсутствует токен

GET /habits/

Ответ (401):

```
{
  "detail": "Authentication credentials were not provided."
}
```
Просроченный токен

Ответ (401):

```
{
  "detail": "Given token not valid for any token type"
}
```
### 7.4. Ошибки доступа
Попытка получить чужую привычку

GET /habits/9999/

Ответ (404):

```
{
  "detail": "Not found."
}
```
### 7.5. Ошибки HabitInstance
Повторное выполнение

POST /habit-instances/3010/complete/

Ответ (409):

```
{
  "detail": "HabitInstance already completed."
}
```
Попытка выполнить после окончания fix-периода
Ответ (409):

```
{
  "detail": "Fix period expired."
}
```
### 7.6. Ошибки Telegram API
Неверный bind_code

POST /telegram/bind/

```
{
  "bind_code": "WRONG123",
  "telegram_id": 88005553535
}
```
Ответ (400):

```
{
  "detail": "Invalid bind code."
}
```
Попытка отвязать несуществующий профиль

POST /telegram/unbind/

Ответ (404):

```
{
  "detail": "Telegram profile not found."
}
```
### 7.7. Стандартные HTTP-коды

- 200	Успешный запрос
- 201	Успешное создание
- 400	Ошибка валидации
- 401	Не авторизован
- 403	Нет доступа
- 404	Не найдено
- 409	Конфликт
- 500	Внутренняя ошибка сервера

### 7.8. Итог
Раздел примеров позволяет:

- быстро протестировать API вручную

- понять типовые сценарии работы

- корректно обрабатывать ошибки на frontend и в Telegram-боте

- использовать единые коды ошибок во всей системе

