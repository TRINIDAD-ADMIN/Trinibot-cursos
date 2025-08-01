from telegram.ext import Updater
from dotenv import load_dotenv
import os
from bot.dispatcher import setup_dispatcher

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN no encontrado en .env")
        return

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    setup_dispatcher(dispatcher)

    print("🤖 Bot en ejecución... Ctrl+C para detener")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
