from telegram import Update
from telegram.ext import CallbackContext
from db.models import obtener_categorias, obtener_recursos_por_categoria
from bot.buttons import generar_botones_categorias
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.models import obtener_recursos_por_tipo
from bot.buttons import generar_botones_categorias

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    categorias = obtener_categorias()
    if not categorias:
        context.bot.send_message(chat_id, "⚠️ No hay categorías disponibles por ahora.")
        return

    # ✅ Botones extra (en la parte superior)
    botones_extra = [
        [InlineKeyboardButton("🎁 Gratis", callback_data="filtro_gratis"),
         InlineKeyboardButton("💸 Descuento", callback_data="filtro_descuento")],
        [InlineKeyboardButton("🌐 Visitar Web", url="https://tu-sitio.com")],
        [InlineKeyboardButton("👨‍💻 Desarrollador", url="https://t.me/tu_usuario_telegram")]
    ]

    # ✅ Obtenemos los botones de categorías (como lista interna)
    teclado_categorias = generar_botones_categorias(categorias).inline_keyboard

    # ✅ Concatenamos las listas internas correctamente
    teclado = InlineKeyboardMarkup(botones_extra + teclado_categorias)

    mensaje = (
        "👋 <b>Bienvenido/a al Bot de Cursos Gratuitos</b> 🎓\n\n"
        "🔍 Aquí encontrarás <b>cursos 100% gratis</b> o con grandes <b>descuentos</b> de plataformas como Udemy, Coursera y más.\n\n"
        "🗂 Selecciona una categoría o aplica un filtro para comenzar:"
    )

    context.bot.send_message(chat_id=chat_id, text=mensaje, reply_markup=teclado, parse_mode='HTML')

def categoria_seleccionada(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    categoria_id = int(query.data.split('_')[1])

    recursos = obtener_recursos_por_categoria(categoria_id)

    if not recursos:
        context.bot.send_message(chat_id, "⚠️ No hay cursos disponibles para esta categoría por ahora.")
        query.answer()
        return

    mensaje = "<b>Cursos disponibles:</b>\n\n"
    for r in recursos:
        descripcion = r['descripcion'] if r['descripcion'] else "Sin descripción"
        fecha = r['fecha_publicacion'].strftime("%d-%m-%Y")
        mensaje += f"🎓 <b>{r['titulo']}</b>\n📝 {descripcion}\n🔗 <a href='{r['url']}'>Ver curso</a>\n📅 Publicado: {fecha}\n\n"

    context.bot.send_message(chat_id, text=mensaje, parse_mode='HTML', disable_web_page_preview=True)
    query.answer()


def filtro_cursos(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    filtro = query.data

    if filtro == "filtro_gratis":
        recursos = obtener_recursos_por_tipo("gratis")
        titulo = "🎁 Cursos 100% Gratis"
    elif filtro == "filtro_descuento":
        recursos = obtener_recursos_por_tipo("descuento")
        titulo = "💸 Cursos con Descuento"
    else:
        query.answer()
        return

    if not recursos:
        context.bot.send_message(chat_id, f"⚠️ No hay cursos disponibles en {titulo}.")
        query.answer()
        return

    mensaje = f"<b>{titulo}</b>\n\n"
    for r in recursos:
        descripcion = r['descripcion'] if r['descripcion'] else "Sin descripción"
        fecha = r['fecha_publicacion'].strftime("%d-%m-%Y")
        mensaje += f"🎓 <b>{r['titulo']}</b>\n📝 {descripcion}\n🔗 <a href='{r['url']}'>Ver curso</a>\n📅 Publicado: {fecha}\n\n"

    context.bot.send_message(chat_id, text=mensaje, parse_mode='HTML', disable_web_page_preview=True)
    query.answer()
