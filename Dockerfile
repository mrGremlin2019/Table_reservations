# Базовый образ
FROM python:3.10-slim

# Установка зависимостей для psycopg2 и alembic
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Даем права на выполнение скрипта
RUN chmod +x start.sh

# Команда запуска
CMD ["sh", "./start.sh"]


