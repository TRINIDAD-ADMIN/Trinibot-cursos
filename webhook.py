# webhook.py
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot.dispatcher import setup_dispatcher
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# =========================
# Cargar variables
# =========================
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no encontrado en .env ni en variables de entorno")

# Crear bot y dispatcher
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
setup_dispatcher(dispatcher)

# =========================
# Flask App
# =========================
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        print("=== WEBHOOK LLAMADO ===")
        json_data = request.get_json(force=True)
        print(f"Datos recibidos: {json_data}")
        
        if json_data is None:
            print("❌ No JSON data")
            return "No JSON data", 400
            
        update = Update.de_json(json_data, bot)
        if update is None:
            print("❌ Invalid update")
            return "Invalid update", 400
            
        print(f"✅ Update procesado: {update}")
        
        # Responder rápido a Telegram ANTES de procesar
        from threading import Thread
        
        def process_update_async():
            try:
                dispatcher.process_update(update)
                print("✅ Dispatcher procesado correctamente")
            except Exception as e:
                print(f"❌ Error en dispatcher: {e}")
                logging.error(f"Error en dispatcher: {e}")
        
        # Procesar en hilo separado para evitar timeout
        thread = Thread(target=process_update_async)
        thread.start()
        
        # Responder inmediatamente a Telegram
        return "OK", 200
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        logging.error(f"Error processing webhook: {e}")
        return "Error", 500

@app.route("/")
def index():
    return "Bot en línea ✅", 200

if __name__ == "__main__":
    app.run(debug=True)