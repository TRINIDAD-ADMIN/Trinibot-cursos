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

def verificar_url(url, titulo, timeout=20):
    """Verifica si una URL está disponible - más conservador"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.head(url, timeout=timeout, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            return True, f"✅ '{titulo}' OK"
        else:
            return False, f"❌ '{titulo}' HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, f"⏱️ '{titulo}' timeout"
    except Exception as e:
        return False, f"❌ '{titulo}' error: {str(e)[:30]}..."

def procesar_lote_cursos(cursos_batch, cursor, conn):
    """Procesa un lote de cursos y retorna estadísticas"""
    eliminados_lote = 0
    urls_no_disponibles = []
    
    # Primero verificar todas las URLs (sin tocar BD)
    for curso in cursos_batch:
        url = curso["url"]
        titulo = curso["titulo"][:40] + "..." if len(curso["titulo"]) > 40 else curso["titulo"]
        
        disponible, mensaje = verificar_url(url, titulo)
        print(mensaje)
        
        if not disponible:
            urls_no_disponibles.append(curso["id"])
        
        # Pausa breve entre verificaciones
        time.sleep(0.5)
    
    # Ahora eliminar en una sola operación si hay cursos a eliminar
    if urls_no_disponibles:
        try:
            # Crear placeholders para la consulta IN
            placeholders = ','.join(['%s'] * len(urls_no_disponibles))
            query = f"DELETE FROM recursos WHERE id IN ({placeholders})"
            
            cursor.execute(query, urls_no_disponibles)
            eliminados_lote = cursor.rowcount
            conn.commit()
            
            print(f"🗑️ Eliminados {eliminados_lote} cursos del lote")
            
        except Exception as e:
            print(f"❌ Error eliminando lote: {e}")
            conn.rollback()
    
    return eliminados_lote, len(cursos_batch)

def verificar_y_eliminar_cursos_caducados():
    # Usar una sola conexión durante todo el proceso
    conn = get_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return

    cursor = None
    try:
        # Configurar conexión para optimizar para muchas operaciones
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Limitar a máximo 50 cursos por ejecución para evitar timeout de Hostinger
        limite_cursos = 50
        print(f"📊 Obteniendo máximo {limite_cursos} cursos para verificar...")
        cursor.execute("SELECT id, titulo, url FROM recursos WHERE disponible = 1 ORDER BY RAND() LIMIT %s", (limite_cursos,))
        cursos = cursor.fetchall()
        
        if not cursos:
            print("ℹ️ No hay cursos para verificar.")
            return

        total_cursos = len(cursos)
        print(f"🔍 Total de cursos a verificar: {total_cursos}")
        
        # Configurar para procesar en lotes más pequeños
        batch_size = 5  # Lotes muy pequeños para hosting compartido
        total_eliminados = 0
        total_verificados = 0
        
        # Procesar en lotes
        for i in range(0, total_cursos, batch_size):
            lote_num = (i // batch_size) + 1
            total_lotes = ((total_cursos - 1) // batch_size) + 1
            
            batch = cursos[i:i + batch_size]
            print(f"\n📦 Procesando lote {lote_num}/{total_lotes} ({len(batch)} cursos)")
            
            # Verificar si la conexión sigue activa
            try:
                cursor.execute("SELECT 1")
            except:
                print("🔄 Conexión perdida, intentando reconectar...")
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                    
                # Intentar reconectar
                conn = get_connection()
                if not conn:
                    print("❌ No se pudo reconectar. Terminando proceso.")
                    break
                cursor = conn.cursor(dictionary=True, buffered=True)
            
            # Procesar el lote
            eliminados_lote, verificados_lote = procesar_lote_cursos(batch, cursor, conn)
            
            total_eliminados += eliminados_lote
            total_verificados += verificados_lote
            
            print(f"✅ Lote {lote_num} completado. Eliminados: {eliminados_lote}")
            
            # Pausa más larga entre lotes para no saturar Hostinger
            if lote_num < total_lotes:
                print("⏸️ Pausa entre lotes...")
                time.sleep(3)
        
        # Mensaje final
        mensaje_final = f"🎯 Verificación completada:\n" \
                       f"📊 Cursos verificados: {total_verificados}\n" \
                       f"🗑️ Cursos eliminados: {total_eliminados}\n" \
                       f"✅ Cursos activos: {total_verificados - total_eliminados}"
        
        print(f"\n{mensaje_final}")
        enviar_notificacion_telegram(mensaje_final)
        
    except Exception as e:
        error_msg = f"❌ Error durante verificación: {str(e)[:200]}..."
        print(error_msg)
        enviar_notificacion_telegram(error_msg)
        
    finally:
        # Cerrar conexiones de forma segura
        try:
            if cursor:
                cursor.close()
        except:
            pass
        try:
            if conn and conn.is_connected():
                conn.close()
        except:
            pass
        print("🔚 Conexiones cerradas")

if __name__ == "__main__":
    verificar_y_eliminar_cursos_caducados()