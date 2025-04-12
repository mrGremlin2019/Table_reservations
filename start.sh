#!/bin/bash

# Ожидание, пока Postgres не станет доступен
echo "⏳ Ожидание запуска PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "✅ PostgreSQL доступен!"

# Применение миграций Alembic
echo "📦 Применение миграций Alembic..."
alembic upgrade head

# Запуск uvicorn сервера
echo "🚀 Запуск FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
