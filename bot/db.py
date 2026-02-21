from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB("db.json", indent=4)

users = db.table("users")
categories = db.table("categories")
expenses = db.table("expenses")

User = Query()
Category = Query()


def add_user(user_data: dict):
    if users.contains(User.telegram_id == user_data["telegram_id"]):
        return False
    users.insert(user_data)
    return True


def is_user_registered(telegram_id: int) -> bool:
    return users.contains(User.telegram_id == telegram_id)


def seed_categories():
    default = ["Oziq-ovqat", "Transport", "Kommunal", "Ko‘ngilochar", "Sog‘liq"]
    for name in default:
        if not categories.contains(Category.name == name):
            categories.insert({"name": name})


def get_categories():
    return categories.all()


def get_category_by_name(name: str):
    name = name.lower().strip()
    for c in categories.all():
        if c["name"].lower() == name:
            return c
    return None


def add_expense(user_id: int, amount: int, category_id: int):
    expenses.insert(
        {
            "user_id": user_id,
            "amount": amount,
            "category_id": category_id,
            "created_at": datetime.now().isoformat(),
        }
    )


def get_total_expense(user_id: int) -> int:
    return sum(e["amount"] for e in expenses.search(Query().user_id == user_id))


def get_expenses_by_category(user_id: int):
    result = {}
    for e in expenses.search(Query().user_id == user_id):
        cat = categories.get(doc_id=e["category_id"])
        name = cat["name"]
        result[name] = result.get(name, 0) + e["amount"]
    return result
