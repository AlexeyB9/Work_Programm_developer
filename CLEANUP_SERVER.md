# 🧹 Очистка старых данных на сервере

## Полная очистка и перезапуск

### Шаг 1: Остановить и удалить все контейнеры

```bash
# Остановить все контейнеры проекта
docker-compose down

# Удалить контейнер guap если он существует
docker stop guap 2>/dev/null || true
docker rm guap 2>/dev/null || true

# Удалить все остановленные контейнеры
docker container prune -f
```

### Шаг 2: Удалить старые образы

```bash
# Удалить образ проекта
docker rmi work_programm_developer_app 2>/dev/null || true
docker rmi guap-app 2>/dev/null || true

# Удалить все неиспользуемые образы
docker image prune -a -f
```

### Шаг 3: Очистить volumes (опционально)

```bash
# Удалить неиспользуемые volumes
docker volume prune -f
```

### Шаг 4: Полная очистка (если ничего не помогает)

```bash
# ОСТОРОЖНО: Удалит ВСЕ остановленные контейнеры, образы, сети и volumes
docker system prune -a --volumes -f
```

### Шаг 5: Пересобрать и запустить

```bash
# Пересобрать образ без кэша
docker-compose build --no-cache

# Запустить
docker-compose up -d

# Проверить логи
docker-compose logs -f
```

## Быстрая команда (все в одной строке)

```bash
docker-compose down && docker stop guap 2>/dev/null; docker rm guap 2>/dev/null; docker rmi work_programm_developer_app guap-app 2>/dev/null; docker-compose build --no-cache && docker-compose up -d
```

## Скрипт автоматической очистки

Создайте файл `cleanup.sh`:

```bash
#!/bin/bash
echo "🧹 Очистка старых контейнеров и образов..."

docker-compose down
docker stop guap 2>/dev/null || true
docker rm guap 2>/dev/null || true
docker rmi work_programm_developer_app guap-app 2>/dev/null || true

echo "✅ Очистка завершена!"
echo "Теперь запустите: docker-compose build --no-cache && docker-compose up -d"
```

Использование:
```bash
chmod +x cleanup.sh
./cleanup.sh
```

