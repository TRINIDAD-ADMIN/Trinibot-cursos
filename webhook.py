"""from telegram.ext import Updater
from dotenv import load_dotenv
import os
from bot.dispatcher import setup_dispatcher

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")
        return

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    setup_dispatcher(dispatcher)

    print("🤖 Bot en ejecución... Ctrl+C para detener")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
"""
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot.dispatcher import setup_dispatcher
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
setup_dispatcher(dispatcher)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return "Bot en línea ✅", 200



