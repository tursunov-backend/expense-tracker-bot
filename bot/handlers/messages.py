from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from ..config.constants import RegisterationStates, ExpenseStates
from ..db import (
    add_user,
    get_categories_from_db,
    get_category_by_name,
    add_expense_to_db,
)


# ================= REGISTRATION =================

def ask_name(update: Update, context: CallbackContext):
    update.message.reply_text("Ismingizni yozing:")
    return RegisterationStates.SET_NAME


def set_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text

    update.message.reply_text(
        "Telefon raqamingizni yuboring:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Telefon raqam", request_contact=True)]],
            resize_keyboard=True,
        ),
    )
    return RegisterationStates.SET_PHONE


def set_phone(update: Update, context: CallbackContext):
    context.user_data["phone"] = update.message.contact.phone_number

    update.message.reply_text(
        "Lokatsiya yuboring:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Lokatsiya yuborish", request_location=True)]],
            resize_keyboard=True,
        ),
    )
    return RegisterationStates.SET_LOCATION


def set_location(update: Update, context: CallbackContext):
    context.user_data["location"] = {
        "lat": update.message.location.latitude,
        "lon": update.message.location.longitude,
    }

    update.message.reply_text(
        "Tasdiqlaysizmi?",
        reply_markup=ReplyKeyboardMarkup(
            [["Tasdiqlash"], ["Qayta boshlash"]],
            resize_keyboard=True,
        ),
    )
    return RegisterationStates.CONFIRM


def register(update: Update, context: CallbackContext):
    data = context.user_data
    data["telegram_id"] = update.message.from_user.id
    data["chat_id"] = update.message.chat.id

    add_user(data)

    update.message.reply_text(
        "Siz ro‘yxatdan o‘tdingiz ✅",
        reply_markup=ReplyKeyboardMarkup(
            [["Xarajat qoshish"]],
            resize_keyboard=True,
        ),
    )

    context.user_data.clear()
    return ConversationHandler.END


# ================= EXPENSE =================

def expense_start(update: Update, context: CallbackContext):
    print("EXPENSE START")  # tekshiruv uchun

    categories = get_categories_from_db()
    keyboard = [[KeyboardButton(cat["name"])] for cat in categories]

    update.message.reply_text(
        "Qaysi kategoriyaga qoshmoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

    return ExpenseStates.SET_CATEGORY


def set_expense_category(update: Update, context: CallbackContext):
    name = update.message.text.strip()
    category = get_category_by_name(name)

    if not category:
        update.message.reply_text("Noto‘g‘ri kategoriya, qayta tanlang")
        return ExpenseStates.SET_CATEGORY

    context.user_data["category_id"] = category.doc_id
    update.message.reply_text("Summani kiriting:")
    return ExpenseStates.SET_AMOUNT


def set_expense_amount(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if not text.isdigit():
        update.message.reply_text("Faqat raqam kiriting!")
        return ExpenseStates.SET_AMOUNT

    add_expense_to_db(
        user_id=update.message.from_user.id,
        title="Xarajat",
        amount=int(text),
        category_id=context.user_data["category_id"],
    )

    update.message.reply_text(
        "Xarajat muvaffaqiyatli qo‘shildi ✅",
        reply_markup=ReplyKeyboardMarkup(
            [["Xarajat qoshish"]],
            resize_keyboard=True,
        ),
    )

    context.user_data.clear()
    return ConversationHandler.END
