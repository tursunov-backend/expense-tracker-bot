from tinydb import TinyDB

db = TinyDB("db.json", indent=4)


def add_user(user_data: dict):
    db.insert(user_data)
