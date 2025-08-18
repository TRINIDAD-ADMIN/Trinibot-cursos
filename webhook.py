from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import asyncio
import traceback

# ============================
# Cargar variables de entorno
# ============================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")

# ============================
# Crear bot y Application
# ============================
bot_instance = Bot(TOKEN)
app_bot = Application(bot=bot_instance)

# ============================
# Definir handlers
# ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Hola! Bot en línea ✅")

# Agrega aquí más handlers si los tienes, ejemplo:
# async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Comandos disponibles: /start, /help")

# ============================
# Registrar handlers
# ============================
app_bot.add_handler(CommandHandler("start", start))
# app_bot.add_handler(CommandHandler("help", help))  # Si tienes más

# ============================
# Crear app Flask
# ============================
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recibir updates de Telegram y procesarlos"""
    json_data = request.get_json(force=True)
    print("Update recibido:", json_data)  # Para debug en logs

    try:
        update = Update.de_json(json_data, app_bot.bot)
        # Procesar update asincrónicamente en WSGI
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(app_bot.process_update(update))
    except Exception as e:
        print("❌ Error procesando update:", e)
        traceback.print_exc()
    finally:
        return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot en línea ✅", 200
