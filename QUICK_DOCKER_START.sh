#!/bin/bash
# Быстрый скрипт запуска через Docker

echo "🐳 Запуск проекта ГУАП через Docker..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "Создайте файл .env с переменными:"
    echo "  PPLX_API_KEY=your_key"
    echo "  TELEGRAM_BOT_TOKEN=your_token"
    echo "  PORT=8000"
    exit 1
fi

# Проверка наличия Dockerfile
if [ ! -f Dockerfile ]; then
    if [ -f config/Dockerfile ]; then
        echo "📋 Копирую Dockerfile из config/..."
        cp config/Dockerfile Dockerfile
    else
        echo "❌ Dockerfile не найден!"
        exit 1
    fi
fi

# Проверка наличия docker-compose
if command -v docker-compose &> /dev/null; then
    echo "🚀 Запуск через docker-compose..."
    docker-compose up -d
    echo "✅ Контейнер запущен!"
    echo "📊 Логи: docker-compose logs -f"
    echo "🌐 Веб-интерфейс: http://localhost:8000"
else
    echo "🚀 Запуск через docker..."
    docker build -t guap-app .
    docker run -d \
      --name guap \
      --restart unless-stopped \
      -p 8000:8000 \
      --env-file .env \
      guap-app
    echo "✅ Контейнер запущен!"
    echo "📊 Логи: docker logs -f guap"
    echo "🌐 Веб-интерфейс: http://localhost:8000"
fi

