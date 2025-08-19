import os
import logging
from flask import Flask, request
import pymysql
import requests
from dotenv import load_dotenv

# ==============================
# 🔹 Configuración inicial
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Token con fallback
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    "8355145266:AAG5GxCK6fcfL7wXXmr4wCOh-HWcHzrfZII"  # fallback
)
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "6824583616")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "u749682169_trinibot")
DB_PASS = os.getenv("DB_PASS", "Qd0g&KM=")
DB_NAME = os.getenv("DB_NAME", "u749682169_trinbot_cursos")

# ==============================
# 🔹 Logging
# ==============================
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "webhook.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ==============================
# 🔹 Flask app
# ==============================
app = Flask(__name__)

def db_connection():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        logging.error(f"❌ Error DB: {e}")
        return None

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"❌ Error enviando mensaje: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(force=True, silent=True)
    logging.info(f"📩 Update recibido: {update}")

    if not update:
        return "no update", 400

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.lower() == "/start":
            send_message(chat_id, "🚀 Hola, tu bot está funcionando en PythonAnywhere 🎉")
        else:
            send_message(chat_id, f"📨 Recibí tu mensaje: {text}")

    return "ok", 200

# ==============================
# 🔹 Punto de entrada
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
