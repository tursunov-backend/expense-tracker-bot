from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)

from .config import settings
from .config.constants import RegisterationStates
from .handlers import (
    commands,
    messages,
)


def main() -> None:
    updater = Updater(settings.BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler("start", commands.start_command))

    # Conversation Handlers
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text("Ro'yxatdan o'tish"), messages.ask_name)
            ],
            states={
                RegisterationStates.SET_NAME: [
                    MessageHandler(Filters.text, messages.set_name)
                ],
                RegisterationStates.SET_PHONE: [
                    MessageHandler(Filters.contact, messages.set_phone)
                ],
                RegisterationStates.SET_LOCATION: [
                    MessageHandler(Filters.location, messages.set_location)
                ],
                RegisterationStates.CONFIRM: [
                    MessageHandler(Filters.text("Tasdiqlash"), messages.register),
                    MessageHandler(Filters.text("Qayta Boshlash"), messages.ask_name),
                ],
            },
            fallbacks=[CommandHandler("cancel", commands.start_command)],
        )
    )

    updater.start_polling()
    updater.idle()
