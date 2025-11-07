from aiogram import types, Dispatcher
from keyboards.main_menu import main_menu_keyboard
from database.db import get_paid_goals

# Tavsiyalar bo‘limi
async def show_recommendations(message: types.Message):
    goals = get_paid_goals()
    if not goals:
        await message.answer("💡 Hozircha tavsiya qilinadigan maqsadlar mavjud emas.", reply_markup=main_menu_keyboard())
        return

    text = "💡 Tavsiyalar:\n\n"
    for goal in goals:
        text += (
            f"Muallif: {goal['author']}\n"
            f"Kategoriya: {goal['category']}\n"
            f"Maqsaddoshlar soni: {goal['friends_count']}\n"
            f"-------------------------\n"
        )
    await message.answer(text, reply_markup=main_menu_keyboard())

# Handlerlarni ro‘yxatdan o‘tkazish
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_recommendations, lambda message: message.text in ["💡 Tavsiyalar", "recommendations"], state="*")
