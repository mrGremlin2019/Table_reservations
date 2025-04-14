# 🪑 Restaurant Table Reservation API

REST API-сервис для бронирования столиков в ресторане. Позволяет управлять столиками, создавать и просматривать бронирования с учетом времени и доступности.

---

## 🚀 Функциональность

### 📌 Столики (`/tables`)
- `GET /tables/` — получить список всех столиков
- `POST /tables/` — создать новый столик
- `DELETE /tables/{id}` — удалить столик по ID

### 📌 Бронирования (`/reservations`)
- `GET /reservations/` — получить список всех броней
- `POST /reservations/` — создать новую бронь
- `DELETE /reservations/{id}` — удалить бронь по ID

> ❗ Проверка конфликта по времени: нельзя создать бронь на столик, если он уже занят в указанный промежуток времени.

---

## ⚙️ Технологии

- **FastAPI** — основной фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Docker + Docker Compose** — изоляция и удобный запуск
- **Pytest** — тестирование
- **.env/.test.env** — конфигурация окружения

---

## 📂 Структура проекта

```bash
     table_reservations/ 
         ├── src/ │ 
         ├── alembic/ # Миграции БД 
         │ ├── db/ # Подключение, модели, CRUD 
         │ ├── routers/ # Маршруты API 
         │ ├── schemas/ # Pydantic-схемы 
         │ ├── tests/ # Тесты 
         │ └── main.py # Точка входа 
         ├── docker-compose.yml 
         ├── Dockerfile 
         ├── .env # Настройки для dev 
         ├── .test.env # Настройки для тестов 
         └── requirements.txt
```

---

## 🐳 Запуск через Docker Compose
Создайте файл .env и .test.env (или используйте шаблоны, приведённые ниже)

```.env:```
```ini
    Копировать
    Редактировать
    MODE=dev
    POSTGRES_USER=user1
    POSTGRES_PASSWORD=qwerty
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=table_reservations
```

```.test.env:```
```ini
    MODE=TEST
    POSTGRES_USER=test_user1
    POSTGRES_PASSWORD=qwerty
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=test_table_reservations
```
> ❗ Перед первым запуском рекомендуется вручную создать обе базы данных (table_reservations и test_table_reservations) и соответствующих пользователей в локальном PostgreSQL.


Запустите проект:

```bash
    docker compose up --build
```

---

## 🧪 Тестирование

Для запуска тестов:

```bash
    docker compose exec web pytest tests/ -v
```

Тесты используют ```.test.env```, в котором указаны тестовая БД и пользователь. Конфигурация окружения автоматически подхватывается.

## 📎 Полезные команды
🔄 Применить миграции:

```bash
    docker compose exec web alembic upgrade head
```
📝 Создать новую миграцию:

```bash
`docker compose exec web alembic revision --autogenerate -m "your message"`
```
