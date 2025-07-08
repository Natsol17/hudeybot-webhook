import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Flask сервер
flask_app = Flask(__name__)

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает через Webhook и готов к работе!")

# Эхо-сообщение
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Я получил твоё сообщение!")

# Обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == "__main__":
    print("🚀 Бот запущен на Webhook (Flask + Telegram)")
    application.initialize()
    application.updater.start_polling()  # нужно для запуска очереди
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
