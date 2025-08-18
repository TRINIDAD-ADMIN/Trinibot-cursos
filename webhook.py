from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import asyncio

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")

# Crear la app del bot sin Updater
bot_instance = Bot(TOKEN)
app_bot = Application(bot=bot_instance)

# Handler de ejemplo
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Bot en línea ✅")

# Agregar handler
app_bot.add_handler(CommandHandler("start", start))

# Crear app Flask
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recibir actualizaciones de Telegram y procesarlas"""
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app_bot.bot)
    asyncio.run(app_bot.process_update(update))
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot en línea ✅", 200
