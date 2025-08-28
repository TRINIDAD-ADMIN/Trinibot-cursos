import requests
from db.connection import get_connection
import os
from dotenv import load_dotenv
import telegram
import time

load_dotenv()

# Configuración token y chat id para notificaciones Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def enviar_notificacion_telegram(mensaje):
    if not TELEGRAM_TOKEN or not ADMIN_CHAT_ID:
        print("⚠️ Falta configuración de Telegram para notificaciones.")
        return
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje, parse_mode='HTML')
    except Exception as e:
        print(f"❌ Error enviando notificación Telegram: {e}")

def verificar_url(url, titulo, timeout=30):
    """Verifica si una URL está disponible con reintentos"""
    max_intentos = 2
    
    for intento in range(max_intentos):
        try:
            # Usar timeout más largo y headers para parecer navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection': 'keep-alive'
            }
            
            response = requests.head(url, timeout=timeout, headers=headers, allow_redirects=True)
            
            if response.status_code == 200:
                return True, f"✅ Curso '{titulo}' disponible."
            elif response.status_code in [301, 302, 307, 308]:
                # Redirecciones - probar con GET
                response = requests.get(url, timeout=timeout, headers=headers, stream=True)
                return response.status_code == 200, f"🔄 Curso '{titulo}' redirigido (HTTP {response.status_code})."
            else:
                return False, f"🚫 Curso '{titulo}' no disponible (HTTP {response.status_code})."
                
        except requests.exceptions.Timeout:
            if intento < max_intentos - 1:
                print(f"⏱️ Timeout en intento {intento + 1} para '{titulo}', reintentando...")
                time.sleep(2)
                continue
            return False, f"⏱️ Curso '{titulo}' timeout después de {timeout}s."
        except requests.exceptions.RequestException as e:
            if intento < max_intentos - 1:
                print(f"⚠️ Error en intento {intento + 1} para '{titulo}': {e}, reintentando...")
                time.sleep(2)
                continue
            return False, f"❌ Error verificando curso '{titulo}': {str(e)[:100]}..."
    
    return False, f"❌ Curso '{titulo}' falló después de {max_intentos} intentos."

def verificar_y_eliminar_cursos_caducados():
    conn = get_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return

    try:
        # Configurar conexión para que no se cierre automáticamente
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Obtener cursos disponibles
        cursor.execute("SELECT id, titulo, url FROM recursos WHERE disponible = 1")
        cursos = cursor.fetchall()
        
        if not cursos:
            print("ℹ️ No hay cursos para verificar.")
            return

        print(f"🔍 Verificando {len(cursos)} cursos...")
        
        eliminados = 0
        verificados = 0
        batch_size = 10  # Procesar en lotes para evitar timeout de BD
        
        for i in range(0, len(cursos), batch_size):
            batch = cursos[i:i + batch_size]
            print(f"📦 Procesando lote {i//batch_size + 1}/{(len(cursos)-1)//batch_size + 1}")
            
            # Reconectar si es necesario
            if not conn.is_connected():
                print("🔄 Reconectando a la base de datos...")
                conn = get_connection()
                if not conn:
                    print("❌ Error de reconexión. Abortando...")
                    return
                cursor = conn.cursor(dictionary=True, buffered=True)
            
            for curso in batch:
                url = curso["url"]
                id_curso = curso["id"]
                titulo = curso["titulo"][:50] + "..." if len(curso["titulo"]) > 50 else curso["titulo"]
                
                # Verificar URL
                disponible, mensaje = verificar_url(url, titulo)
                print(mensaje)
                
                if not disponible:
                    try:
                        cursor.execute("DELETE FROM recursos WHERE id = %s", (id_curso,))
                        conn.commit()  # Commit inmediato para evitar pérdida
                        eliminados += 1
                        print(f"🗑️ Eliminado: {titulo}")
                    except Exception as e:
                        print(f"❌ Error eliminando curso ID {id_curso}: {e}")
                        # Reconectar si hay error de conexión
                        if "Lost connection" in str(e):
                            conn = get_connection()
                            cursor = conn.cursor(dictionary=True, buffered=True)
                
                verificados += 1
                
                # Pausa para no sobrecargar el servidor
                time.sleep(1)
            
            print(f"✅ Lote completado. Verificados: {verificados}/{len(cursos)}")
        
        mensaje_final = f"🗑️ Proceso de limpieza finalizado:\n" \
                       f"📊 Cursos verificados: {verificados}\n" \
                       f"🗑️ Cursos eliminados: {eliminados}\n" \
                       f"✅ Cursos activos: {verificados - eliminados}"
        
        print(mensaje_final)
        enviar_notificacion_telegram(mensaje_final)
        
    except Exception as e:
        error_msg = f"❌ Error durante verificación: {e}"
        print(error_msg)
        enviar_notificacion_telegram(error_msg)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    verificar_y_eliminar_cursos_caducados()