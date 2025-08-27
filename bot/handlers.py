from telegram import Update
from telegram.ext import CallbackContext
from db.models import obtener_categorias, obtener_recursos_por_categoria
from bot.buttons import generar_botones_categorias
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.models import obtener_recursos_por_tipo
from bot.buttons import generar_botones_categorias

def mostrar_menu_principal(update: Update, context: CallbackContext):
    """Función para mostrar el menú principal con los 3 botones"""
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        query = update.callback_query
    else:
        chat_id = update.effective_chat.id
        query = None

    # ✅ Los tres botones principales
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Categorías de Cursos", callback_data="mostrar_categorias")],
        [InlineKeyboardButton("👤 Acerca del desarrollador", url="https://trinibot.trinovadevps.com/web/acerca.php")],
        [InlineKeyboardButton("⚙️ Panel web", url="https://trinibot.trinovadevps.com/web/home.php")],
    ])

    mensaje = (
        "👋 <b>Bienvenido/a al Bot de Cursos Gratuitos</b> 🎓\n\n"
        "🔍 Aquí encontrarás <b>cursos 100% gratis</b> o con grandes <b>descuentos</b> de plataformas como Udemy, Coursera y más.\n\n"
        "🗂 Selecciona una opción para comenzar:"
    )

    if query:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=mensaje,
            reply_markup=teclado,
            parse_mode='HTML'
        )
        query.answer()
    else:
        context.bot.send_message(chat_id=chat_id, text=mensaje, reply_markup=teclado, parse_mode='HTML')

def start(update: Update, context: CallbackContext):
    """Comando /start - ahora muestra el menú principal"""
    mostrar_menu_principal(update, context)

def mostrar_categorias(update: Update, context: CallbackContext):
    """Muestra las categorías de cursos"""
    query = update.callback_query
    chat_id = query.message.chat_id

    categorias = obtener_categorias()
    if not categorias:
        context.bot.send_message(chat_id, "⚠️ No hay categorías disponibles por ahora.")
        query.answer()
        return

    # ✅ Botones extra (en la parte superior)
    botones_extra = [
        [InlineKeyboardButton("🎁 Gratis", callback_data="filtro_gratis"),
         InlineKeyboardButton("💸 Descuento", callback_data="filtro_descuento")],
        [InlineKeyboardButton("🌐 Visitar Web", url="https://trinibot.trinovadevps.com/web/home.php")],
    ]

    # ✅ Obtenemos los botones de categorías (como lista interna)
    teclado_categorias = generar_botones_categorias(categorias).inline_keyboard

    # ✅ Botón para volver al menú principal
    boton_volver = [[InlineKeyboardButton("🔙 Volver al menú principal", callback_data="menu_principal")]]

    # ✅ Concatenamos las listas internas correctamente
    teclado = InlineKeyboardMarkup(botones_extra + teclado_categorias + boton_volver)

    mensaje = (
        "📚 <b>Categorías de Cursos Disponibles</b> 🎓\n\n"
        "🔍 Selecciona una categoría o aplica un filtro para ver los cursos:"
    )

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text=mensaje,
        reply_markup=teclado,
        parse_mode='HTML'
    )
    query.answer()

def categoria_seleccionada(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    categoria_id = int(query.data.split('_')[1])

    recursos = obtener_recursos_por_categoria(categoria_id)

    if not recursos:
        context.bot.send_message(chat_id, "⚠️ No hay cursos disponibles para esta categoría por ahora.")
        query.answer()
        return

    # Verificar si hay muchos cursos para implementar paginación
    CURSOS_POR_PAGINA = 10
    total_cursos = len(recursos)
    
    if total_cursos > CURSOS_POR_PAGINA:
        # Si hay más de 10 cursos, mostrar solo los primeros 10 y redirigir al panel web
        recursos = recursos[:CURSOS_POR_PAGINA]
        mensaje = f"<b>📚 Primeros {CURSOS_POR_PAGINA} cursos de {total_cursos} disponibles:</b>\n\n"
        
        for r in recursos:
            descripcion = (r['descripcion'][:100] + "...") if r['descripcion'] and len(r['descripcion']) > 100 else (r['descripcion'] if r['descripcion'] else "Sin descripción")
            fecha = r['fecha_publicacion'].strftime("%d-%m-%Y")
            mensaje += f"🎓 <b>{r['titulo']}</b>\n📝 {descripcion}\n🔗 <a href='{r['url']}'>Ver curso</a>\n📅 Publicado: {fecha}\n\n"
        
        mensaje += f"<i>💡 Hay {total_cursos - CURSOS_POR_PAGINA} cursos más disponibles en el panel web.</i>"
        
        # Teclado con énfasis en ver todos los cursos en el panel web
        teclado_volver = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Ver TODOS los cursos en el Panel Web", url="https://trinibot.trinovadevps.com/web/home.php")],
            [InlineKeyboardButton("🔙 Volver al menú principal", callback_data="menu_principal")]
        ])
    else:
        # Si hay 10 cursos o menos, mostrar todos normalmente
        mensaje = "<b>📚 Cursos disponibles:</b>\n\n"
        
        for r in recursos:
            descripcion = (r['descripcion'][:100] + "...") if r['descripcion'] and len(r['descripcion']) > 100 else (r['descripcion'] if r['descripcion'] else "Sin descripción")
            fecha = r['fecha_publicacion'].strftime("%d-%m-%Y")
            mensaje += f"🎓 <b>{r['titulo']}</b>\n📝 {descripcion}\n🔗 <a href='{r['url']}'>Ver curso</a>\n📅 Publicado: {fecha}\n\n"
        
        # Teclado normal
        teclado_volver = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Ver más en el Panel Web", url="https://trinibot.trinovadevps.com/web/home.php")],
            [InlineKeyboardButton("🔙 Volver al menú principal", callback_data="menu_principal")]
        ])

    context.bot.send_message(chat_id, text=mensaje, parse_mode='HTML', disable_web_page_preview=True, reply_markup=teclado_volver)
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
        descripcion = (r['descripcion'][:100] + "...") if r['descripcion'] and len(r['descripcion']) > 100 else (r['descripcion'] if r['descripcion'] else "Sin descripción")
        fecha = r['fecha_publicacion'].strftime("%d-%m-%Y")
        mensaje += f"🎓 <b>{r['titulo']}</b>\n📝 {descripcion}\n🔗 <a href='{r['url']}'>Ver curso</a>\n📅 Publicado: {fecha}\n\n"

    # ✅ Botón para volver al menú principal al final
    teclado_volver = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Volver al menú principal", callback_data="menu_principal")]
    ])

    context.bot.send_message(chat_id, text=mensaje, parse_mode='HTML', disable_web_page_preview=True, reply_markup=teclado_volver)
    query.answer()