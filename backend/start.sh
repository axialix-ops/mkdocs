#!/bin/bash

# Ожидаем, пока база данных будет готова
# (простая проверка, в реальном проекте можно использовать wait-for-it.sh)
echo "Ожидание запуска PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL запущен."

# Применяем миграции базы данных
echo "Применение миграций Alembic..."
alembic upgrade head

# Запускаем FastAPI приложение
echo "Запуск FastAPI приложения..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
