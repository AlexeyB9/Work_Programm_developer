# Инструкция по развертыванию на сервере

## Подготовка проекта

1. Убедитесь, что все зависимости установлены:
```bash
pip install -r requirements.txt
```

2. Проверьте наличие файла шаблона:
- `files/Шаблон.docx` должен существовать

3. Настройте переменные окружения:
- Используйте файл `config/env.example` как пример
- На сервере настройте переменные окружения через панель управления хостинга

## Варианты развертывания

### 1. Railway (Рекомендуется - бесплатный тариф)

**Преимущества:**
- Бесплатный тариф с 500 часами в месяц
- Автоматическое развертывание из GitHub
- Простое управление переменными окружения
- Поддержка Python и веб-приложений

**Инструкция:**

1. Зарегистрируйтесь на [Railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Создайте новый проект из репозитория
4. Настройте переменные окружения:
   - `PPLX_API_KEY` - ваш ключ Perplexity API
   - `TELEGRAM_BOT_TOKEN` - токен Telegram бота (если используется)
5. Railway автоматически определит Python проект
6. Добавьте команду запуска в настройках:
   ```
   python run_all.py
   ```
7. Railway автоматически назначит публичный URL

**Важно для Railway:**
- Создайте файл `Procfile`:
  ```
  web: python run_all.py
  ```
- Или используйте `railway.json`:
  ```json
  {
    "build": {
      "builder": "NIXPACKS"
    },
    "deploy": {
      "startCommand": "python run_all.py",
      "restartPolicyType": "ON_FAILURE",
      "restartPolicyMaxRetries": 10
    }
  }
  ```

### 2. Render.com (Бесплатный тариф)

**Преимущества:**
- Бесплатный тариф для веб-сервисов
- Автоматическое развертывание
- Простая настройка

**Инструкция:**

1. Зарегистрируйтесь на [Render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите GitHub репозиторий
4. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run_all.py`
   - **Environment:** Python 3
5. Добавьте переменные окружения:
   - `PPLX_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
6. Deploy!

**Ограничения бесплатного тарифа:**
- Сервис "засыпает" после 15 минут неактивности
- Первый запрос после простоя может быть медленным

### 3. PythonAnywhere (Бесплатный тариф)

**Преимущества:**
- Бесплатный тариф для Python приложений
- Простое управление через веб-интерфейс

**Инструкция:**

1. Зарегистрируйтесь на [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Загрузите проект через Files или Git
3. Создайте веб-приложение:
   - Выберите "Manual configuration"
   - Выберите Python версию
4. Настройте WSGI файл:
   ```python
   import sys
   path = '/home/yourusername/Work_Programm_developer'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from api import app
   application = app
   ```
5. Настройте переменные окружения в консоли:
   ```bash
   export PPLX_API_KEY="your_key"
   export TELEGRAM_BOT_TOKEN="your_token"
   ```
6. Запустите Telegram бота через задачу (Tasks):
   ```bash
   cd /home/yourusername/Work_Programm_developer
   python tgbot/bot.py
   ```

### 4. Heroku (Ограниченный бесплатный тариф)

**Примечание:** Heroku убрал бесплатный тариф, но можно использовать для тестирования.

**Инструкция:**

1. Установите Heroku CLI
2. Создайте `Procfile`:
   ```
   web: python run_all.py
   ```
3. Создайте `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Развертывание:
   ```bash
   heroku create your-app-name
   heroku config:set PPLX_API_KEY=your_key
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   git push heroku main
   ```

### 5. VPS (Vultr, DigitalOcean, AWS Free Tier)

**Для VPS серверов:**

1. Подключитесь к серверу по SSH
2. Установите Python и зависимости:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
3. Клонируйте репозиторий:
   ```bash
   git clone your-repo-url
   cd Work_Programm_developer
   ```
4. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Настройте переменные окружения:
   ```bash
   export PPLX_API_KEY="your_key"
   export TELEGRAM_BOT_TOKEN="your_token"
   ```
6. Используйте systemd для автозапуска (создайте `/etc/systemd/system/guap.service`):
   ```ini
   [Unit]
   Description=ГУАП веб-сервер и Telegram бот
   After=network.target

   [Service]
   Type=simple
   User=your_user
   WorkingDirectory=/path/to/Work_Programm_developer
   Environment="PPLX_API_KEY=your_key"
   Environment="TELEGRAM_BOT_TOKEN=your_token"
   ExecStart=/path/to/venv/bin/python run_all.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
7. Запустите сервис:
   ```bash
   sudo systemctl enable guap
   sudo systemctl start guap
   ```
8. Настройте Nginx как reverse proxy (опционально):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Рекомендации по бесплатным хостингам

### Для продакшена:
1. **Railway** - лучший вариант, простой и надежный
2. **Render** - хорошая альтернатива, но может "засыпать"

### Для разработки/тестирования:
1. **PythonAnywhere** - удобно для экспериментов
2. **VPS с бесплатным тарифом** (AWS Free Tier, Oracle Cloud)

### Важные замечания:

1. **Telegram бот:** Для работы бота нужен постоянный доступ к интернету. Railway и Render подходят лучше всего.

2. **Файловое хранилище:** 
   - На бесплатных хостингах файлы могут удаляться при перезапуске
   - Рассмотрите использование облачного хранилища (S3, Cloudinary) для файлов

3. **База данных:** 
   - Для истории чатов можно использовать SQLite (включено)
   - Для продакшена рассмотрите PostgreSQL

4. **Безопасность:**
   - Никогда не коммитьте `.env` файл
   - Используйте переменные окружения на сервере
   - Ограничьте доступ к API ключам

## Проверка работоспособности

После развертывания проверьте:

1. Веб-интерфейс доступен по URL
2. Можно загрузить файл и получить результат
3. Telegram бот отвечает на команды
4. Логи не содержат критических ошибок

## Мониторинг

Рекомендуется настроить:
- Логирование ошибок
- Мониторинг использования API (Perplexity имеет лимиты)
- Алерты при падении сервиса

