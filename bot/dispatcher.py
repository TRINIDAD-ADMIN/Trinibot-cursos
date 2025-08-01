from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.handlers import start, categoria_seleccionada, filtro_cursos

def setup_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(categoria_seleccionada, pattern=r"^cat_\d+$"))
    dispatcher.add_handler(CallbackQueryHandler(filtro_cursos, pattern=r"^filtro_"))
