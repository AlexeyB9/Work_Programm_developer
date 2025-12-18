# 🚀 Быстрый запуск на сервере через Docker

## Шаг 1: Подготовка

На сервере выполните:

```bash
# Перейдите в папку проекта
cd /Work_Programm_developer

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

**Или используйте быструю команду:**
```bash
cat > .env << 'EOF'
PPLX_API_KEY=ваш_ключ_perplexity
TELEGRAM_BOT_TOKEN=ваш_токен_бота
PORT=8000
EOF
nano .env  # Отредактируйте и укажите реальные значения
```

**Если получили ошибку про .env файл:** См. [FIX_ENV_ERROR.md](FIX_ENV_ERROR.md)

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

## Шаг 3: Настройка файрвола

**ВАЖНО:** Откройте порт 8000 в файрволе:

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 8000/tcp
sudo ufw reload

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## Шаг 4: Проверка

```bash
# Проверка доступности
chmod +x check_access.sh
./check_access.sh

# Или вручную
docker ps
curl http://localhost:8000
```

Откройте в браузере: `http://IP_ВАШЕГО_СЕРВЕРА:8000`

**Если недоступно извне:** См. [FIREWALL_SETUP.md](FIREWALL_SETUP.md)

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

### Приложение недоступно извне:

1. **Проверьте файрвол:**
   ```bash
   sudo ufw allow 8000/tcp  # Ubuntu/Debian
   sudo firewall-cmd --permanent --add-port=8000/tcp && sudo firewall-cmd --reload  # CentOS/RHEL
   ```

2. **Проверьте доступность:**
   ```bash
   chmod +x check_access.sh
   ./check_access.sh
   ```

3. **Используйте правильный IP:**
   - Не `localhost` или `127.0.0.1`
   - Используйте внешний IP сервера: `http://IP_СЕРВЕРА:8000`

Смотрите логи:
```bash
docker logs guap
# или
docker-compose logs -f
```

Подробная инструкция: [DOCKER_RUN.md](DOCKER_RUN.md)  
Проверка доступа: [VERIFY_ACCESS.md](VERIFY_ACCESS.md)  
Настройка файрвола: [FIREWALL_SETUP.md](FIREWALL_SETUP.md)

