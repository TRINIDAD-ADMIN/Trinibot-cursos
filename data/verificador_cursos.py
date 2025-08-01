import requests
from db.connection import get_connection
import os
from dotenv import load_dotenv
import telegram

load_dotenv()

# Configuración token y chat id para notificaciones Telegram (ajusta a tu caso)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # Debes agregarlo a tu .env

def enviar_notificacion_telegram(mensaje):
    if not TELEGRAM_TOKEN or not ADMIN_CHAT_ID:
        print("⚠️ Falta configuración de Telegram para notificaciones.")
        return
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje, parse_mode='HTML')
    except Exception as e:
        print(f"❌ Error enviando notificación Telegram: {e}")

def verificar_y_eliminar_cursos_caducados():
    conn = get_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, titulo, url FROM recursos WHERE disponible = 1")
    cursos = cursor.fetchall()

    eliminados = 0

    for curso in cursos:
        url = curso["url"]
        id_curso = curso["id"]
        titulo = curso["titulo"]

        try:
            # Hacer un HEAD para solo verificar status sin bajar contenido completo
            response = requests.head(url, timeout=10)
            if response.status_code != 200:
                print(f"🚫 Curso '{titulo}' no disponible (HTTP {response.status_code}). Eliminando...")
                cursor.execute("DELETE FROM recursos WHERE id = %s", (id_curso,))
                eliminados += 1
            else:
                print(f"✅ Curso '{titulo}' disponible.")
        except requests.RequestException as e:
            print(f"⚠️ Error verificando curso '{titulo}': {e}. Eliminando por seguridad...")
            cursor.execute("DELETE FROM recursos WHERE id = %s", (id_curso,))
            eliminados += 1

    conn.commit()
    cursor.close()
    conn.close()

    mensaje = f"🗑️ Proceso de limpieza finalizado: {eliminados} cursos caducados eliminados."
    print(mensaje)
    enviar_notificacion_telegram(mensaje)


if __name__ == "__main__":
    verificar_y_eliminar_cursos_caducados()
