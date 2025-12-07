# CI/CD — Atomic Habits Tracker

В проекте Atomic Habits Tracker используется CI/CD на основе GitHub Actions для автоматизации:

- запуска тестов
- проверки кода
- сборки Docker-образов
- деплоя на production-сервер

---

## 1. Общая схема CI/CD

Каждый push или pull request в ветку `main` запускает pipeline:

1. Установка зависимостей
2. Backend тесты (pytest)
3. Frontend тесты (Vitest)
4. Линтинг
5. Docker build
6. Деплой на сервер

---

## 2. Структура workflow

Каталог:

`.github/workflows/`

Файлы:

| Файл | Назначение |
|------|------------|
| `tests.yml` | Тесты backend и frontend |
| `lint.yml` | Линтинг |
| `build.yml` | Сборка Docker |
| `deploy.yml` | Деплой |

---

## 3. Secrets GitHub

В настройках репозитория задаются секреты:

| Secret | Назначение |
|--------|------------|
| `SSH_HOST` | IP сервера |
| `SSH_USER` | Пользователь сервера |
| `SSH_KEY` | Приватный ключ |
| `ENV_PROD` | Production `.env` |
| `DOCKER_USERNAME` | DockerHub логин |
| `DOCKER_PASSWORD` | DockerHub пароль |

---

## 4. Backend CI

Процесс:

- установка Python
- установка poetry
- установка зависимостей
- запуск pytest

Команда:

`pytest`

Используется:

- PostgreSQL (service)
- Redis (service)
- тестовое окружение `ENV=ci`

---

## 5. Frontend CI

Процесс:

- установка Node.js
- установка npm-зависимостей
- запуск vitest

Команды:
```
npm install
npm run test
```

---

## 6. Линтинг

Используется:

| Инструмент | Назначение |
|------------|------------|
| flake8 | Python |
| eslint | TypeScript |

Команды:

`flake8 .`

`npm run lint`

---

## 7. Docker Build

После успешных тестов:

- собираются образы:
  - backend
  - frontend
  - telegrambot

- образы пушатся в DockerHub

---

## 8. Автоматический деплой

При push в `main`:

1. GitHub Actions:
   - подключается по SSH
   - делает `git pull`
   - применяет `docker compose down`
   - выполняет `docker compose up -d --build`

---

## 9. Ручной деплой

Ручной запуск pipeline возможен через:

- GitHub → Actions → Run workflow

---

## 10. Стратегия веток

| Ветка | Назначение |
|-------|------------|
| `main` | Production |
| `develop` | Разработка |
| `feature/*` | Новые фичи |
| `fix/*` | Исправления |

---

## 11. Уведомления

Возможные интеграции:

- Telegram
- Slack
- Email

Для уведомления:

- о провале сборки
- о падении тестов
- об успешном деплое

---

## 12. Ограничения безопасности

- секреты не хранятся в репозитории
- SSH-ключ ограничен по IP
- доступ к workflow ограничен владельцем репозитория
- деплой доступен только из main

---

## 13. Итог

CI/CD в Atomic Habits Tracker обеспечивает:

- стабильность
- проверку качества кода
- автоматическое тестирование
- автоматическую сборку
- контролируемый деплой
- минимизацию человеческого фактора

Это позволяет безопасно и быстро выпускать новые версии проекта.