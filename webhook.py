# webhook.py
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot.dispatcher import setup_dispatcher
from dotenv import load_dotenv

# =========================
# Cargar variables
# =========================
# Solo carga .env si existe (local). En producción las toma de os.environ
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env ni en variables de entorno")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
setup_dispatcher(dispatcher)

# =========================
# Flask App
# =========================
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def index():
    return "Bot en línea ✅", 200
