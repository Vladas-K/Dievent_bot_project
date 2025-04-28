# 📅 DIEVENT_BOT_PROJECT — Django Backend + Telegram Bot

**Dievent_bot_project** — это веб-сервис на Django + Telegram-бот, который позволяет пользователям получать подробную информацию о мероприятиях, в которых они участвуют.

Проект состоит из:
- **Eventplanner** для хранения и предоставления информации о мероприятиях.
- **Telegram-бота**, который взаимодействует с пользователями через команды и кнопки.
- **Docker-компоновки** для развёртывания всех сервисов.

---

## 📂 Структура проекта

- `eventplanner/` — Django-приложение с API для событий и пользователей Telegram.
- `bot/` — код Telegram-бота на Python с использованием библиотеки `python-telegram-bot`.
- `gateway/` — настройка прокси-сервера Nginx.
- `docker-compose.yml` — контейнеризация backend, бота, базы данных и nginx.
- `.env` — файл с переменными окружения.

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Vladas-K/Dievent_bot_project.git
cd eventplanner
```

### 2. Настроить `.env` файл

Создайте файл `.env` на корневом уровне проекта:

```env
# Переменные для Django
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Переменные для Telegram Bot
TOKEN=your_telegram_bot_token
API_URL=http://gateway/api/events/
USER_API_URL=http://gateway/api/users/
```

---

### 3. Собрать и запустить контейнеры

```bash
docker-compose up --build
```

Контейнеры:
- `db` — база данных PostgreSQL
- `eventplanner` — Django-приложение (backend)
- `gateway` — nginx-сервер
- `eventbot` — Telegram-бот

---

### 4. Миграции и создание суперпользователя (опционально)

Войдите в контейнер `eventplanner`:

```bash
docker-compose exec eventplanner bash
```

Выполните миграции:

```bash
python manage.py migrate
```

Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

---

## 📡 Описание работы

### Django Backend
- Эндпоинты API:
  - `/api/events/` — список всех мероприятий.
  - `/api/users/` — регистрация пользователей Telegram.
- Используется `Django REST Framework`.
- Защита API через пермишен `AllowTelegramOrAuthenticated`.

### Telegram Bot
- `/start` — регистрация пользователя в базе данных и приветственное сообщение.
- `/events` — список ближайших мероприятий с возможностью получения подробной информации:
  - 📖 Описание
  - 🗓 Дата и время
  - 📍 Локация
  - 🏢 Информация о компании
  - 👗 Дресс-код

Бот запрашивает данные у бекенда через HTTP-запросы.

---

## 📦 Стек технологий

- **Python 3.10**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL 13**
- **Docker / Docker Compose**
- **NGINX**
- **python-telegram-bot 20+**
- **aiohttp**

---

## ⚙️ Особенности проекта

- Простая авторизация через `Bot-Token`.
- Обработка ошибок при сетевых сбоях.
- Отправка информации через inline-кнопки Telegram.
- Контейнеризация всех сервисов.
- Возможность масштабирования.

---

## 🧑‍💻 Автор

**Vladas Kuodis**
