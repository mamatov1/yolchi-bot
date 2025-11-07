from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📝 Tahrirlash", callback_data="edit_profile"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")
    )
    return keyboard
