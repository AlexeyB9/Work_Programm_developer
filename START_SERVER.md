# 🚀 Быстрый запуск на сервере через Docker

## Шаг 1: Подготовка

На сервере выполните:

```bash
# Перейдите в папку проекта
cd /path/to/Work_Programm_developer

# Создайте файл .env с вашими ключами
nano .env
```

В файле `.env` укажите:
```env
PPLX_API_KEY=ваш_ключ_perplexity
TELEGRAM_BOT_TOKEN=ваш_токен_бота
PORT=8000
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

## Шаг 2: Запуск (выберите один вариант)

### Вариант А: Через docker-compose (рекомендуется)

```bash
# Запуск
docker-compose up -d

# Проверка логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Вариант Б: Через docker напрямую

```bash
# Сборка образа
docker build -t guap-app .

# Запуск контейнера
docker run -d \
  --name guap \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  guap-app

# Проверка логов
docker logs -f guap
```

### Вариант В: Автоматический скрипт

```bash
chmod +x QUICK_DOCKER_START.sh
./QUICK_DOCKER_START.sh
```

## Шаг 3: Проверка

Откройте в браузере: `http://ваш_сервер:8000`

Или проверьте статус:
```bash
docker ps
curl http://localhost:8000
```

## Управление

```bash
# Остановить
docker stop guap
# или
docker-compose stop

# Запустить
docker start guap
# или
docker-compose start

# Перезапустить
docker restart guap
# или
docker-compose restart

# Удалить
docker stop guap && docker rm guap
# или
docker-compose down
```

## Проблемы?

Смотрите логи:
```bash
docker logs guap
# или
docker-compose logs -f
```

Подробная инструкция: [DOCKER_RUN.md](DOCKER_RUN.md)

