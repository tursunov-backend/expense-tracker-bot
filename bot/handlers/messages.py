from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from ..db import (
    add_user,
    is_user_registered,
    get_categories,
    get_category_by_name,
    add_expense,
    get_total_expense,
    get_expenses_by_category,
)

SET_NAME, SET_PHONE, SET_LOCATION, SET_CATEGORY, SET_AMOUNT = range(5)


def main_menu(update: Update):
    update.message.reply_text(
        "Menyu 👇",
        reply_markup=ReplyKeyboardMarkup(
            [["Xarajat qoshish"], ["Xarajatlarim"]], resize_keyboard=True
        ),
    )


def menu_router(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Ro'yxatdan o'tish":
        update.message.reply_text("Ismingizni yozing:")
        return SET_NAME

    if text == "Xarajat qoshish":
        if not is_user_registered(update.message.from_user.id):
            update.message.reply_text("Avval ro'yxatdan o'ting ❗")
            return ConversationHandler.END

        keyboard = [[KeyboardButton(c["name"])] for c in get_categories()]
        update.message.reply_text(
            "Kategoriya tanlang:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        )
        return SET_CATEGORY

    if text == "Xarajatlarim":
        total = get_total_expense(update.message.from_user.id)
        data = get_expenses_by_category(update.message.from_user.id)

        msg = f"💰 Umumiy: {total:,} so'm\n\n"
        for k, v in data.items():
            msg += f"• {k}: {v:,} so'm\n"

        update.message.reply_text(msg)
        main_menu(update)
        return ConversationHandler.END

    return ConversationHandler.END


def set_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    update.message.reply_text(
        "Telefon raqam yuboring:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Telefon", request_contact=True)]], resize_keyboard=True
        ),
    )
    return SET_PHONE


def set_phone(update: Update, context: CallbackContext):
    context.user_data["phone"] = update.message.contact.phone_number
    update.message.reply_text(
        "Lokatsiya yuboring:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Lokatsiya", request_location=True)]], resize_keyboard=True
        ),
    )
    return SET_LOCATION


def set_location(update: Update, context: CallbackContext):
    context.user_data["location"] = {
        "lat": update.message.location.latitude,
        "lon": update.message.location.longitude,
    }

    data = context.user_data
    data["telegram_id"] = update.message.from_user.id
    data["chat_id"] = update.message.chat.id

    add_user(data)

    update.message.reply_text("Ro'yxatdan o'tdingiz ✅")

    context.user_data.clear()
    main_menu(update)
    return ConversationHandler.END


def set_category(update: Update, context: CallbackContext):
    cat = get_category_by_name(update.message.text)
    if not cat:
        return SET_CATEGORY

    context.user_data["category_id"] = cat.doc_id
    update.message.reply_text("Summani kiriting:")
    return SET_AMOUNT


def set_amount(update: Update, context: CallbackContext):
    if not update.message.text.isdigit():
        return SET_AMOUNT

    add_expense(
        update.message.from_user.id,
        int(update.message.text),
        context.user_data["category_id"],
    )
    update.message.reply_text("Xarajat qo'shildi ✅")
    context.user_data.clear()
    main_menu(update)
    return ConversationHandler.END
