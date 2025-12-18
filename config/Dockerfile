FROM python:3.11-slim

WORKDIR /app

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

# Команда запуска (run_all.py должен быть в корне проекта)
CMD ["python", "run_all.py"]

