"""
Telegram бот для обработки учебников через Perplexity API.
"""

import os
import sys
import uuid
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Добавляем родительскую директорию в путь для импорта init_core
sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from wpd.merge_with_docx import generate_docx_from_template

# Токен бота должен быть установлен через переменную окружения TELEGRAM_BOT_TOKEN
# Получите токен у @BotFather в Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    print("⚠️ TELEGRAM_BOT_TOKEN не установлен. Telegram бот не будет запущен.")
    print("   Установите переменную окружения: export TELEGRAM_BOT_TOKEN=your_token")
    print("   или настройте на сервере через панель управления хостинга.")

# Папки для временных файлов (относительно корня проекта)
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "files" / "telegram_uploads"
RESULT_DIR = BASE_DIR / "files" / "telegram_results"
TEMPLATE_PATH = BASE_DIR / "files" / "Шаблон.docx"

# Создаем папки если их нет
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_message = (
        "👋 Привет! Я бот для формирования учебной программы ГУАП.\n\n"
        "📚 Отправьте мне файл учебника в формате .docx, и я сгенерирую "
        "документ из шаблона (без автогенерации через ИИ).\n\n"
        "Используйте /help для получения справки."
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = (
        "📖 Справка по использованию бота:\n\n"
        "1️⃣ Отправьте файл учебника в формате .docx\n"
        "2️⃣ Дождитесь генерации документа (это займет несколько секунд)\n"
        "3️⃣ Получите готовый файл result.docx\n\n"
        "Команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n\n"
        "ℹ️ Бот работает в режиме генерации по шаблону (без автогенерации через ИИ)."
    )
    await update.message.reply_text(help_text)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик загруженных документов"""
    document = update.message.document

    # Проверяем, что это .docx файл
    if not document.file_name or not document.file_name.endswith('.docx'):
        await update.message.reply_text(
            "❌ Поддерживаются только файлы в формате .docx. "
            "Пожалуйста, отправьте файл с расширением .docx"
        )
        return

    # Отправляем сообщение о начале обработки
    processing_msg = await update.message.reply_text(
        "⏳ Файл получен. Начинаю обработку...\n"
        "Это может занять несколько минут, пожалуйста, подождите."
    )

    try:
        # Генерируем уникальный ID для сессии
        file_id = str(uuid.uuid4())

        # Скачиваем файл
        file = await context.bot.get_file(document.file_id)
        uploaded_file_path = UPLOAD_DIR / f"{file_id}_{document.file_name}"

        await file.download_to_drive(uploaded_file_path)

        # Проверяем наличие шаблона
        if not TEMPLATE_PATH.exists():
            await processing_msg.edit_text(
                f"❌ Ошибка: Шаблон не найден по пути {TEMPLATE_PATH}. "
                "Обратитесь к администратору."
            )
            return

        # Путь к результату
        result_path = RESULT_DIR / f"{file_id}_result.docx"

        # Обновляем сообщение о прогрессе
        await processing_msg.edit_text(
            "Генерация документа из шаблона...\n"
            "Это займет несколько секунд."
        )

        # Генерируем документ из шаблона без автогенерации через ИИ
        # Просто создаем документ с пустыми переменными
        generate_docx_from_template(
            data={},  # Пустой словарь - все переменные будут пустыми
            template_path=str(TEMPLATE_PATH),
            output_path=str(result_path),
            all_variables={}  # Пустой словарь для всех переменных
        )

        # Проверяем, что файл результата создан
        if not result_path.exists():
            await processing_msg.edit_text(
                "Ошибка: Файл результата не был создан. "
                "Попробуйте отправить файл еще раз."
            )
            return

        # Отправляем файл результата
        await processing_msg.edit_text("Обработка завершена! Отправляю файл...")

        with open(result_path, 'rb') as result_file:
            await update.message.reply_document(
                document=result_file,
                filename="result.docx",
                caption="Готовый файл result.docx"
            )

        await processing_msg.edit_text("Файл успешно обработан и отправлен!")

        # Удаляем временные файлы
        try:
            uploaded_file_path.unlink()
            result_path.unlink()
        except Exception:
            pass  # Игнорируем ошибки удаления

    except FileNotFoundError as e:
        await processing_msg.edit_text(
            f"Ошибка: Файл не найден - {str(e)}"
        )
    except ValueError as e:
        await processing_msg.edit_text(
            f"Ошибка: {str(e)}"
        )
    except Exception as e:
        error_msg = f"Произошла ошибка при обработке файла: {str(e)}"
        await processing_msg.edit_text(error_msg)
        # Логируем ошибку для отладки
        print(f"Ошибка в handle_document: {e}")
        import traceback
        traceback.print_exc()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    await update.message.reply_text(
        "Пожалуйста, отправьте файл учебника в формате .docx.\n\n"
        "Используйте /help для получения справки."
    )


def run_bot() -> None:
    """Запуск бота (для использования в отдельном потоке)"""
    if not BOT_TOKEN:
        print("⚠️ Telegram бот не запущен: не указан TELEGRAM_BOT_TOKEN")
        return
    
    token = BOT_TOKEN
    
    # Создаем приложение
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Запускаем бота
    try:
        print("🤖 Telegram бот запущен...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Игнорируем старые обновления при перезапуске
        )
    except Exception as e:
        error_msg = str(e)
        if "Conflict" in error_msg or "terminated by other getUpdates" in error_msg:
            print("⚠️ Telegram бот уже запущен в другом процессе.")
            print("   Остановите другие экземпляры бота или используйте только run_all.py")
        else:
            print(f"❌ Ошибка при запуске Telegram бота: {e}")
        import traceback
        traceback.print_exc()
        raise


def main() -> None:
    """Запуск бота (точка входа для отдельного запуска)"""
    if not BOT_TOKEN:
        print("❌ Ошибка: Не указан TELEGRAM_BOT_TOKEN!")
        print("Установите переменную окружения: export TELEGRAM_BOT_TOKEN=your_token")
        print("Получить токен можно у @BotFather в Telegram")
        return
    
    run_bot()


if __name__ == "__main__":
    main()
