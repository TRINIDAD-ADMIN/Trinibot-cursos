# webhook.py
"""
import os
import sys
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
import logging
from threading import Thread

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar tu setup de handlers
try:
    from bot.handlers import start, categoria_seleccionada, filtro_cursos
    from telegram.ext import CommandHandler, CallbackQueryHandler
    
    def setup_handlers(dispatcher):
        # Configurar tus handlers reales
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CallbackQueryHandler(categoria_seleccionada, pattern=r"^cat_\d+$"))
        dispatcher.add_handler(CallbackQueryHandler(filtro_cursos, pattern=r"^filtro_"))
        logger.info("✅ Handlers configurados correctamente")
        
except ImportError as e:
    logger.warning(f"⚠️ Error importando handlers: {e}")
    def setup_handlers(dispatcher):
        from telegram.ext import CommandHandler
        def start(update, context):
            update.message.reply_text('¡Bot funcionando en Render! 🌟')
        def help_command(update, context):
            update.message.reply_text('Bot desplegado exitosamente en Render.com')
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))

from dotenv import load_dotenv

# Configurar logging para Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# =========================
# Cargar variables de entorno
# =========================
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN no encontrado")
    raise ValueError("TELEGRAM_BOT_TOKEN requerido")

logger.info(f"🤖 Bot token configurado: {TOKEN[:10]}...")

# Crear bot y dispatcher
try:
    bot = Bot(TOKEN)
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    setup_handlers(dispatcher)
    logger.info("✅ Bot y dispatcher configurados correctamente")
except Exception as e:
    logger.error(f"❌ Error configurando bot: {e}")
    raise

# =========================
# Flask App
# =========================
app = Flask(__name__)

def process_update_background(update):
    """Procesa el update en segundo plano para evitar timeouts"""
    try:
        if update.effective_message:
            logger.info(f"📨 Procesando mensaje: '{update.effective_message.text[:50]}...' de usuario {update.effective_user.id}")
        elif update.callback_query:
            logger.info(f"🔘 Procesando callback: '{update.callback_query.data}' de usuario {update.effective_user.id}")
        
        dispatcher.process_update(update)
        logger.info("✅ Update procesado exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error procesando update: {e}", exc_info=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        
        if json_data is None:
            logger.warning("❌ No se recibió JSON data")
            return "No JSON data", 400
            
        update = Update.de_json(json_data, bot)
        if update is None:
            logger.warning("❌ Update inválido recibido")
            return "Invalid update", 400
        
        # Procesar en hilo separado para responder rápido a Telegram
        thread = Thread(target=process_update_background, args=(update,))
        thread.daemon = True
        thread.start()
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Error crítico en webhook: {e}", exc_info=True)
        return "Internal Error", 500

@app.route("/")
def index():
    return "🤖 TriniBot Cursos Online - Powered by Render.com 🌟", 200

@app.route("/health")
def health():
    try:
        bot_info = bot.get_me()
        return {
            "status": "healthy", 
            "bot_username": bot_info.username,
            "bot_id": bot_info.id,
            "service": "trinibot-cursos",
            "platform": "Render.com",
            "python_version": sys.version
        }, 200
    except Exception as e:
        logger.error(f"❌ Health check falló: {e}")
        return {"status": "unhealthy", "error": str(e)}, 500

@app.route("/status")
def status():
    return {
        "service": "TriniBot Cursos",
        "version": "2.0",
        "platform": "Render.com",
        "status": "running"
    }, 200

# Endpoint para despertar el servicio (Render lo duerme después de 15 min)
@app.route("/wake")
def wake():
    logger.info("🔔 Servicio despertado")
    return "Service awake", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🚀 Iniciando TriniBot en puerto {port}")
    logger.info(f"🌍 Plataforma: Render.com")
    app.run(host="0.0.0.0", port=port, debug=False)"""
    import os
import sys
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher
import logging
from threading import Thread
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# =========================
# Configuración de logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# =========================
# Handler START con menú inicial
# =========================
def start(update, context):
    """Mensaje de bienvenida con menú principal"""
    keyboard = [
        [InlineKeyboardButton("📚 Categorías de Cursos", callback_data="cat_menu")],
        [InlineKeyboardButton("👤 Acerca del desarrollador", url="https://trinibot.trinovadevps.com/web/acerca.php")],
        [InlineKeyboardButton("⚙️ Panel web", url="https://trinibot.trinovadevps.com/web/home.php")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "👋 ¡Bienvenido a *TriniBot Cursos*! 🚀\n\n"
        "Explora cursos gratuitos online y administra tus recursos de aprendizaje.\n\n"
        "Selecciona una opción del menú:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# =========================
# Importar setup de handlers
# =========================
try:
    from bot.handlers import categoria_seleccionada, filtro_cursos
    from telegram.ext import CommandHandler, CallbackQueryHandler
    
    def setup_handlers(dispatcher):
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CallbackQueryHandler(categoria_seleccionada, pattern=r"^cat_"))
        dispatcher.add_handler(CallbackQueryHandler(filtro_cursos, pattern=r"^filtro_"))
        logger.info("✅ Handlers configurados correctamente")
        
except ImportError as e:
    logger.warning(f"⚠️ Error importando handlers: {e}")
    def setup_handlers(dispatcher):
        from telegram.ext import CommandHandler
        def start_fallback(update, context):
            update.message.reply_text('¡Bot funcionando en Render! 🌟')
        def help_command(update, context):
            update.message.reply_text('Bot desplegado exitosamente en Render.com')
        dispatcher.add_handler(CommandHandler("start", start_fallback))
        dispatcher.add_handler(CommandHandler("help", help_command))

# =========================
# Cargar variables de entorno
# =========================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN no encontrado")
    raise ValueError("TELEGRAM_BOT_TOKEN requerido")

logger.info(f"🤖 Bot token configurado: {TOKEN[:10]}...")

# Crear bot y dispatcher
try:
    bot = Bot(TOKEN)
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    setup_handlers(dispatcher)
    logger.info("✅ Bot y dispatcher configurados correctamente")
except Exception as e:
    logger.error(f"❌ Error configurando bot: {e}")
    raise

# =========================
# Flask App
# =========================
app = Flask(__name__)

def process_update_background(update):
    """Procesa el update en segundo plano para evitar timeouts"""
    try:
        if update.effective_message:
            logger.info(f"📨 Procesando mensaje: '{update.effective_message.text[:50]}...' de usuario {update.effective_user.id}")
        elif update.callback_query:
            logger.info(f"🔘 Procesando callback: '{update.callback_query.data}' de usuario {update.effective_user.id}")
        
        dispatcher.process_update(update)
        logger.info("✅ Update procesado exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error procesando update: {e}", exc_info=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        
        if json_data is None:
            logger.warning("❌ No se recibió JSON data")
            return "No JSON data", 400
            
        update = Update.de_json(json_data, bot)
        if update is None:
            logger.warning("❌ Update inválido recibido")
            return "Invalid update", 400
        
        # Procesar en hilo separado para responder rápido a Telegram
        thread = Thread(target=process_update_background, args=(update,))
        thread.daemon = True
        thread.start()
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Error crítico en webhook: {e}", exc_info=True)
        return "Internal Error", 500

@app.route("/")
def index():
    return "🤖 TriniBot Cursos Online - Powered by Render.com 🌟", 200

@app.route("/health")
def health():
    try:
        bot_info = bot.get_me()
        return {
            "status": "healthy", 
            "bot_username": bot_info.username,
            "bot_id": bot_info.id,
            "service": "trinibot-cursos",
            "platform": "Render.com",
            "python_version": sys.version
        }, 200
    except Exception as e:
        logger.error(f"❌ Health check falló: {e}")
        return {"status": "unhealthy", "error": str(e)}, 500

@app.route("/status")
def status():
    return {
        "service": "TriniBot Cursos",
        "version": "2.0",
        "platform": "Render.com",
        "status": "running"
    }, 200

# Endpoint para despertar el servicio (Render lo duerme después de 15 min)
@app.route("/wake")
def wake():
    logger.info("🔔 Servicio despertado")
    return "Service awake", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🚀 Iniciando TriniBot en puerto {port}")
    logger.info(f"🌍 Plataforma: Render.com")
    app.run(host="0.0.0.0", port=port, debug=False)
