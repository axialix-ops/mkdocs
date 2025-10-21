# Указываем базовый образ Python
FROM python:3.9-slim

# Устанавливаем netcat для проверки доступности БД
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в рабочую директорию
COPY . .

# Делаем стартовый скрипт исполняемым
RUN chmod +x /app/start.sh

# Указываем команду для запуска приложения
ENTRYPOINT ["/app/start.sh"]
