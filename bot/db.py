from tinydb import TinyDB, Query

db = TinyDB("db.json", indent=4)

users_table = db.table("users")
categories_table = db.table("categories")
expenses_table = db.table("expenses")

User = Query()
Category = Query()


def add_user(user_data: dict):
    users_table.insert(user_data)


def is_user_registered(telegram_id: int):
    return users_table.contains(User.telegram_id == telegram_id)


def seed_categories():
    default_categories = [
        "Oziq-ovqat",
        "Transport",
        "Kommunal",
        "Ko‘ngilochar",
        "Sog‘liq",
    ]

    for name in default_categories:
        if not categories_table.contains(Category.name == name):
            categories_table.insert({"name": name})


def get_categories_from_db():
    return categories_table.all()


def get_category_by_name(name: str):
    name = name.strip()
    return categories_table.get(Category.name == name)


def add_expense_to_db(user_id, title, amount, category_id):
    expenses_table.insert(
        {
            "user_id": user_id,
            "title": title,
            "amount": amount,
            "category_id": category_id,
        }
    )
