#!/bin/bash
# Скрипт для создания файла .env

echo "🔧 Создание файла .env..."

# Проверяем существует ли уже .env
if [ -f .env ]; then
    echo "⚠️  Файл .env уже существует!"
    read -p "Перезаписать? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Отменено."
        exit 0
    fi
fi

# Создаем файл .env
cat > .env << 'EOF'
# Perplexity API Key (обязательно)
PPLX_API_KEY=your_perplexity_api_key_here

# Telegram Bot Token (опционально)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Порт для веб-сервера (по умолчанию 8000)
PORT=8000
EOF

echo "✅ Файл .env создан!"
echo ""
echo "📝 Теперь отредактируйте файл .env и укажите ваши ключи:"
echo "   nano .env"
echo ""
echo "Или используйте:"
echo "   export PPLX_API_KEY=your_key"
echo "   export TELEGRAM_BOT_TOKEN=your_token"
echo "   и запустите без --env-file"

