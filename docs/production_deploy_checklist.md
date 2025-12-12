# ✅ Production Deploy Checklist — Atomic Habits Tracker

Этот чек-лист предназначен для полного развертывания проекта Atomic Habits Tracker  
— от «пустого сервера» до полностью рабочей production-системы.

Используется при:
- первом деплое
- полном переносе на новый сервер
- disaster recovery

---

## 1. Сервер и система

- [ ] Установлен Ubuntu 20.04+
- [ ] Обновление системы выполнено
sudo apt update && sudo apt upgrade -y

markdown
Копировать код
- [ ] Установлен Git
- [ ] Установлен Docker
- [ ] Установлен Docker Compose v2
- [ ] Включён UFW Firewall
- [ ] Открыты порты:
- 22 (SSH)
- 80 (HTTP)
- 443 (HTTPS)

---

## 2. Проект и репозиторий

- [ ] Репозиторий клонирован
`git clone <repo>`
- [ ] Переход в папку проекта
- [ ] Проверена структура проекта
- [ ] Присутствует `env.example`

---

## 3. Переменные окружения

- [ ] Создан `.env`
`cp env.example .env`
- [ ] Заполнены:
- SECRET_KEY
- POSTGRES_*
- REDIS_*
- CELERY_*
- JWT_*
- TELEGRAM_BOT_TOKEN
- VITE_API_URL
- [ ] DEBUG=False
- [ ] Установлены production security flags:
- DJANGO_SECURE_SSL_REDIRECT=True
- DJANGO_SESSION_COOKIE_SECURE=True
- DJANGO_CSRF_COOKIE_SECURE=True

---

## 4. Docker

- [ ] Проверены все Dockerfile
- [ ] Проверен docker-compose.yml
- [ ] Проверены volume:
- postgres_data
- redis_data
- static_volume
- media_volume

---

## 5. Первый запуск контейнеров

- [ ] Запуск:
`docker compose up -d --build`
- [ ] Проверка:
`docker compose ps`
- [ ] Все контейнеры в статусе `Up`

---

## 6. Backend (Django)

- [ ] Выполнены миграции
`docker compose exec backend python manage.py migrate`
- [ ] Создан суперпользователь
`docker compose exec backend python manage.py createsuperuser`
- [ ] Собрана статика
`docker compose exec backend python manage.py collectstatic --noinput`
- [ ] Swagger доступен:
`/api/docs/`
- [ ] Redoc доступен:
`/api/redoc/`

---

## 7. База данных и Redis

- [ ] PostgreSQL доступен
- [ ] Redis доступен
- [ ] Celery worker подключён к Redis
- [ ] Celery beat запущен
- [ ] Генерация HabitInstance работает

---

## 8. Frontend

- [ ] VITE_API_URL указывает на production
- [ ] Frontend доступен по домену
- [ ] Статика отдается через Nginx
- [ ] Авторизация работает
- [ ] Все основные страницы открываются:
- /login
- /habits
- /today
- /profile
- /public

---

## 9. Домен и HTTPS

- [ ] Домен привязан к IP сервера
- [ ] Установлен certbot
- [ ] Получен SSL-сертификат
`sudo certbot --nginx -d your-domain.com`
- [ ] HTTPS активен
- [ ] Сертификат обновляется автоматически

---

## 10. Telegram Bot

- [ ] TELEGRAM_BOT_TOKEN указан
- [ ] Режим:
- long polling ИЛИ webhook
- [ ] При webhook:
- TELEGRAM_USE_WEBHOOK=True
- TELEGRAM_WEBHOOK_URL корректный
- [ ] Бот отвечает на команды:
- /start
- /help
- /habits
- /today
- [ ] Привязка Telegram работает
- [ ] Кнопки выполнения работают

---

## 11. Статистика и кэш

- [ ] Redis используется для кэша
- [ ] Кэш инвалидируется:
- при выполнении
- при пропуске
- при изменении привычек
- [ ] Статистика корректно пересчитывается

---

## 12. CI/CD

- [ ] Secrets добавлены:
- SSH_HOST
- SSH_USER
- SSH_KEY
- ENV_PROD
- [ ] Тесты проходят в GitHub Actions
- [ ] Линт проходит
- [ ] Docker образы собираются
- [ ] Автодеплой работает
- [ ] Push в main обновляет production

---

## 13. Мониторинг и логи

- [ ] Проверены логи:
- backend
- celery_worker
- celery_beat
- telegrambot
- [ ] Добавлен мониторинг (опционально):
- Sentry
- UptimeRobot
- [ ] Настроены бэкапы PostgreSQL

---

## 14. Финальная проверка

- [ ] Регистрация работает
- [ ] Логин работает
- [ ] Создание привычек работает
- [ ] Генерация инстансов работает
- [ ] Telegram-уведомления приходят
- [ ] Выполнение привычек из Telegram работает
- [ ] Аналитика отображается корректно
- [ ] Public habits отображаются

---

## ✅ ПРОЕКТ ГОТОВ К PRODUCTION

Если все пункты выше отмечены —  
проект **Atomic Habits Tracker полностью готов к боевой эксплуатации**.
