#!/bin/bash
# Скрипт очистки старых контейнеров и образов

echo "🧹 Очистка старых контейнеров и образов..."

# Остановить и удалить контейнеры
echo "1. Остановка контейнеров..."
docker-compose down 2>/dev/null || true
docker stop guap 2>/dev/null || true
docker rm guap 2>/dev/null || true

# Удалить образы
echo "2. Удаление образов..."
docker rmi work_programm_developer_app 2>/dev/null || true
docker rmi guap-app 2>/dev/null || true

# Очистить неиспользуемые ресурсы
echo "3. Очистка неиспользуемых ресурсов..."
docker container prune -f
docker image prune -f

echo ""
echo "✅ Очистка завершена!"
echo ""
echo "Теперь запустите:"
echo "  docker-compose build --no-cache"
echo "  docker-compose up -d"

