import os
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

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Flask-приложение
flask_app = Flask(__name__)
bot = Bot(token=TOKEN)

application = ApplicationBuilder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает через Webhook и готов к работе!")

# echo
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Я получил твоё сообщение!")

# Добавляем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook маршрут
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    print("🚀 Бот запущен на Webhook (Flask + Telegram)")
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

