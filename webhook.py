from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot.dispatcher import setup_dispatcher
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")

# Inicializar bot y dispatcher
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)  # workers=0 para hosting compartido
setup_dispatcher(dispatcher)

# Crear la app de Flask
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recibir actualizaciones de Telegram y procesarlas"""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "Bot en línea ✅", 200

# Nota: No se usa if __name__ == "__main__" en producción con Gunicorn
