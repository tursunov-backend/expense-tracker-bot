from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)

from .config import settings
from .handlers import messages, commands
from .db import seed_categories


def main():
    seed_categories()

    updater = Updater(settings.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", commands.start_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, messages.menu_router)],
        states={
            messages.SET_NAME: [MessageHandler(Filters.text, messages.set_name)],
            messages.SET_PHONE: [MessageHandler(Filters.contact, messages.set_phone)],
            messages.SET_LOCATION: [
                MessageHandler(Filters.location, messages.set_location)
            ],
            messages.SET_CATEGORY: [
                MessageHandler(Filters.text, messages.set_category)
            ],
            messages.SET_AMOUNT: [MessageHandler(Filters.text, messages.set_amount)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
