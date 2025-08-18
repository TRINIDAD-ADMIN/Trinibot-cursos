from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder
from bot.dispatcher import setup_dispatcher
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")

# Crear aplicación del bot (v20)
app_bot = ApplicationBuilder().token(TOKEN).build()

# Configurar handlers del bot
setup_dispatcher(app_bot)  # Ajusta tu función setup_dispatcher para usar app_bot

# Crear la app Flask
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recibir actualizaciones de Telegram y procesarlas"""
    update = Update.de_json(request.get_json(force=True), app_bot.bot)
    app_bot.update_queue.put(update)
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "Bot en línea ✅", 200
