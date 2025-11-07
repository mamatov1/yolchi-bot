from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def account_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🚀 Raketa — 4900 UZS", callback_data="tariff_rocket"),
        InlineKeyboardButton("⚡️ Chaqmoq — 21900 UZS", callback_data="tariff_lightning"),
        InlineKeyboardButton("☄️ Kometa — 39900 UZS", callback_data="tariff_comet"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")
    )
    return keyboard
