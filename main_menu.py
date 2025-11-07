from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🎯 Maqsadlarim", callback_data="goals"),
        InlineKeyboardButton("👤 Profil", callback_data="profile"),
        InlineKeyboardButton("💡 Tavsiyalar", callback_data="recommendations"),
        InlineKeyboardButton("💎 Hisob raqam", callback_data="account"),
        InlineKeyboardButton("ℹ️ Biz haqimizda", callback_data="about")
    )
    return keyboard
