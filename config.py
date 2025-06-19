import os

APP_NAME = "Restaurant Management System"
DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PATHS = {
    "users": os.path.join(DATA_DIR, "users.txt"),
    "customers": os.path.join(DATA_DIR, "customers.txt"),
    "orders": os.path.join(DATA_DIR, "orders.txt"),
    "reviews": os.path.join(DATA_DIR, "reviews.txt"),
    "carts": os.path.join(DATA_DIR, "carts.txt"),
    "menu": os.path.join(DATA_DIR, "menu_items.txt"),
    "promo": os.path.join(DATA_DIR, "promo_codes.txt"),
    "finances": os.path.join(DATA_DIR, "finances.txt"),
    "inventory": os.path.join(DATA_DIR, "inventory.txt"),
    "feedback": os.path.join(DATA_DIR, "feedbacks.txt")
}

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"