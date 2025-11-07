from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def goals_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("➕ Maqsad yaratish", callback_data="create_goal"),
        InlineKeyboardButton("📋 Mening maqsadlarim", callback_data="my_goals"),
        InlineKeyboardButton("🤝 Men qo‘shilgan maqsadlar", callback_data="joined_goals"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")
    )
    return keyboard
