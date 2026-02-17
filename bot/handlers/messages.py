from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from ..config.constants import RegisterationStates
from ..db import add_user


def ask_name(update: Update, context: CallbackContext):
    update.message.reply_text("Ismingizni yozing...")

    return RegisterationStates.SET_NAME


def set_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text

    update.message.reply_text(
        "Telefon raqamingizni yuboring...",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("Telefon Raqam", request_contact=True)]]
        ),
    )

    # update.message.delete()

    return RegisterationStates.SET_PHONE


def set_phone(update: Update, context: CallbackContext):
    context.user_data["phone"] = update.message.contact.phone_number

    update.message.reply_text(
        "Lokatsiya yuboring...",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("Lokatsiya Yuborish", request_location=True)]]
        ),
    )

    return RegisterationStates.SET_LOCATION


def set_location(update: Update, context: CallbackContext):
    context.user_data["location"] = {
        "longitude": update.message.location.longitude,
        "latitude": update.message.location.latitude,
    }
    user_data = context.user_data

    user_info = f"ismingiz: {user_data['name']}\nphone: {user_data['phone']}"
    update.message.reply_text(
        user_info,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton("Tasdiqlash"),
                    KeyboardButton("Qayta Boshlash"),
                ]
            ]
        ),
    )

    return RegisterationStates.CONFIRM


def register(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data["telegram_id"] = update.message.from_user.id
    user_data["chat_id"] = update.message.chat.id

    add_user(user_data)

    update.message.reply_text("Siz muvaffaqiyatli royxatdan otdingiz.")

    return ConversationHandler.END
