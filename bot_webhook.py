@@ -2,50 +2,52 @@ import os
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

# Загрузка переменных
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ Переменная TELEGRAM_TOKEN не найдена!")

# Flask-приложение
flask_app = Flask(__name__)
bot = Bot(token=TOKEN)

# Telegram Application
application = ApplicationBuilder().token(TOKEN).build()
# Инициализируем приложение один раз при старте
asyncio.run(application.initialize())

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает через Webhook и готов к работе!")

# Обработчик текстов
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Я получил твоё сообщение!")

# Добавляем в Application
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook route
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.process_update(update))
        return "ok"
    except Exception as e:
        print("❌ Ошибка при обработке webhook:")
        import traceback
        traceback.print_exc()
        return "error", 500

