# Production Deployment — Atomic Habits Tracker

В этом документе описан полный пошаговый процесс развертывания проекта Atomic Habits Tracker в production-среде на VPS с использованием Docker, Nginx, HTTPS и Telegram Webhook.

---

## 1. Требования к серверу

Минимальные характеристики VPS:

| Параметр | Значение |
|----------|----------|
| ОС | Ubuntu 20.04+ |
| CPU | 2 vCPU |
| RAM | 4 GB |
| Disk | 40+ GB |
| Архитектура | x86_64 |

На сервере должны быть установлены:

- Docker
- Docker Compose v2
- Git
- UFW (Firewall)

---

## 2. Подготовка сервера

### 2.1. Обновление системы

`sudo apt update && sudo apt upgrade -y`

---

### 2.2. Установка Docker

`curl -fsSL https://get.docker.com | sh`

Проверка:

`docker --version`

---

### 2.3. Установка Docker Compose v2

`sudo apt install docker-compose-plugin -y`

Проверка:

`docker compose version`

---

### 2.4. Установка Git

`sudo apt install git -y`

---

## 3. Клонирование проекта
```
git clone https://github.com/<your_repo>/AtomicHabitsTracker.git
cd AtomicHabitsTracker
```

---

## 4. Настройка переменных окружения

Скопировать пример:

`cp env.example .env`

Заполнить значения:

- Django SECRET_KEY
- PostgreSQL
- Redis
- Telegram токен
- JWT
- Frontend API URL
- Production security flags

---

## 5. Настройка Firewall

Открыть необходимые порты:
```
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

Проверить:

`sudo ufw status`

---

## 6. Сборка и запуск контейнеров

`docker compose up -d --build`

Проверить запущенные контейнеры:

`docker compose ps`

---

## 7. Применение миграций и создание суперпользователя
```
docker compose exec backend python manage.py migrate

docker compose exec backend python manage.py createsuperuser
```

---

## 8. Сборка и подключение статики

`docker compose exec backend python manage.py collectstatic --noinput`

Nginx автоматически начинает обслуживать статику.

---

## 9. Настройка домена

В DNS-панели домена указать:

| Тип | Значение |
|-----|----------|
| A | IP-адрес сервера |

После применения DNS-проверить:

`ping your-domain.com`

---

## 10. Настройка HTTPS (Let's Encrypt)

Получение HTTPS-сертификатов через certbot:
```
sudo apt install certbot python3-certbot-nginx -y

sudo certbot --nginx -d your-domain.com
```

Автообновление сертификатов:

`sudo certbot renew --dry-run`

---

## 11. Настройка Telegram Webhook

В `.env`:
```
TELEGRAM_USE_WEBHOOK=True
TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook/
```

Перезапуск контейнеров:

`docker compose restart telegrambot`

Проверка:

- отправить `/start` в боте
- проверить логи telegrambot

---

## 12. Проверка работоспособности системы

Проверить:

- Frontend:  
`https://your-domain.com`

- Backend API:  
`https://your-domain.com/api/`

- Swagger:  
`https://your-domain.com/api/docs/`

- Redoc:  
`https://your-domain.com/api/redoc/`

- Telegram Bot:
- команды
- кнопки
- выполнение привычек

---

## 13. Обновление проекта (deploy новой версии)

Обновление выполняется так:
```
git pull
docker compose down
docker compose up -d --build
```

Если есть миграции:

`docker compose exec backend python manage.py migrate`

---

## 14. Резервное копирование

### 14.1. Backup базы данных

`docker compose exec postgres pg_dump -U atomic_user atomic_habits > backup.sql`

---

### 14.2. Восстановление

`docker compose exec -T postgres psql -U atomic_user atomic_habits < backup.sql`

---

## 15. Мониторинг и логи

Просмотр логов:
```
docker compose logs -f backend
docker compose logs -f celery_worker
docker compose logs -f telegrambot
```

Рекомендуется подключение:

- Sentry
- UptimeRobot
- Prometheus + Grafana (опционально)

---

## 16. Production рекомендации

- DEBUG=False
- Использовать HTTPS
- Ограничить доступ к Swagger в prod
- Ограничить доступ к админке по IP
- Регулярно обновлять сервер
- Делать бэкапы минимум раз в сутки

---

## 17. Итог

После выполнения всех шагов вы получаете:

- полностью работающий backend
- собранный frontend
- рабочий Telegram-бот
- Celery worker и beat
- Redis и PostgreSQL
- защищённый HTTPS-домен
- автоматическую генерацию документации API
- production-ready систему Atomic Habits Tracker
