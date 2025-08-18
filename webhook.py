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
# webhook.py
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.dispatcher import setup_dispatcher
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")

# Inicializar Flask
app = Flask(__name__)

# Crear aplicación de telegram
application = ApplicationBuilder().token(TOKEN).build()

# Configurar dispatcher y comandos desde tu módulo
setup_dispatcher(application)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recibir actualizaciones de Telegram y procesarlas"""
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot en línea ✅", 200

if __name__ == "__main__":
    # Solo para pruebas locales con polling
    print("🤖 Iniciando bot en modo polling...")
    application.run_polling()

