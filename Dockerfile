FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем необходимые директории
RUN mkdir -p files/uploads files/results files/telegram_uploads files/telegram_results

# Устанавливаем переменные окружения по умолчанию
ENV PORT=8000

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["python", "run_all.py"]

