# keyboards/tariffs.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tariffs = [
    "🚀 Raketa — 4900 UZS • +1 olmos",
    "⚡️ Chaqmoq — 21900 UZS • +5 olmos",
    "☄️ Kometa — 39900 UZS • +10 olmos"
]

buttons = [KeyboardButton(t) for t in tariffs]
buttons.append(KeyboardButton("❌ Bekor qilish"))

tariffs_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
tariffs_keyboard.add(*buttons)
