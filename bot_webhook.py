import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ Переменная TELEGRAM_TOKEN не найдена!")

# Flask-приложение
flask_app = Flask(__name__)
bot = Bot(token=TOKEN)

# Создаём Telegram-приложение
application = ApplicationBuilder().token(TOKEN).build()

# Обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает через Webhook и готов к работе!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Я получил твоё сообщение!")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook маршрут
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)

        # Запускаем event loop для обработки обновления
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_and_process(update))

        return "ok"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "error", 500

# Объединяем инициализацию и обработку
async def initialize_and_process(update):
    await application.initialize()
    await application.process_update(update)

# Запуск Flask-сервера
if __name__ == "__main__":
    print("🚀 Webhook бот запущен (Flask + Telegram)")
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

