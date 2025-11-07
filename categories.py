# keyboards/categories.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 16 ta kategoriya misol
categories = [
    "Ta’lim", "Biznes", "Sayohat", "Zamonaviy kasblar",
    "Sog‘liq", "Sport", "San’at", "Texnologiya",
    "Moliyaviy", "Oila", "Madaniyat", "Ijtimoiy",
    "Motivatsiya", "Shaxsiy rivojlanish", "Hobby", "Boshqa"
]

# Tugmalar yaratish
buttons = [KeyboardButton(cat) for cat in categories]
buttons.append(KeyboardButton("⬅️ Orqaga"))

categories_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
categories_keyboard.add(*buttons)
