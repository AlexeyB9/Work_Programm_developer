"""
Скрипт для запуска всех сервисов: веб-сервер и Telegram бот.
"""

import sys
import threading
import time
from pathlib import Path

# Флаг для отслеживания запуска бота
_bot_started = False

def start_telegram_bot():
    """Запуск Telegram бота в отдельном потоке"""
    global _bot_started
    if _bot_started:
        print("Telegram бот уже запущен, пропускаем...")
        return
    
    try:
        import os
        # Проверка токена перед запуском
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            print("⚠️  TELEGRAM_BOT_TOKEN не установлен. Telegram бот не будет запущен.")
            print("   Установите переменную окружения TELEGRAM_BOT_TOKEN в .env файле.")
            return
        
        sys.path.insert(0, str(Path(__file__).parent))
        from tgbot.bot import run_bot
        _bot_started = True
        print("🤖 Запуск Telegram бота...")
        run_bot()
    except Exception as e:
        _bot_started = False
        error_msg = str(e)
        if "Conflict" in error_msg or "terminated by other getUpdates" in error_msg:
            print("⚠️  Telegram бот уже запущен в другом процессе.")
            print("   Убедитесь, что не запущены другие экземпляры бота.")
            print("   Веб-сервер будет работать без бота.")
        elif "TELEGRAM_BOT_TOKEN" in error_msg or "токен" in error_msg.lower():
            print("⚠️  Ошибка конфигурации Telegram бота: токен не установлен или неверный.")
            print("   Установите TELEGRAM_BOT_TOKEN в .env файле.")
            print("   Веб-сервер будет работать без бота.")
        else:
            print(f"❌ Ошибка при запуске Telegram бота: {e}")
            import traceback
            traceback.print_exc()
            print("   Веб-сервер будет работать без бота.")

def start_web_server():
    """Запуск веб-сервера"""
    try:
        import uvicorn
        import os
        from api import app
        port = int(os.getenv("PORT", 8000))
        print(f"Запуск веб-сервера на http://0.0.0.0:{port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Ошибка при запуске веб-сервера: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Главная функция запуска всех сервисов"""
    print("=" * 60)
    print("🚀 Запуск всех сервисов ГУАП")
    print("=" * 60)
    print()
    
    # Запускаем Telegram бота в отдельном потоке
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    
    # Даем боту время на запуск
    time.sleep(2)
    
    # Запускаем веб-сервер (блокирующий вызов)
    try:
        start_web_server()
    except KeyboardInterrupt:
        print("\n\nОстановка всех сервисов...")
        print("До свидания!")
        sys.exit(0)

if __name__ == "__main__":
    main()

