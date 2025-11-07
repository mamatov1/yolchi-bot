from aiogram import types, Dispatcher
from keyboards.main_menu import main_menu_keyboard

async def start_menu(message: types.Message):
    """
    Asosiy menyu xabari
    """
    user_name = message.from_user.first_name
    text = f"Salom, {user_name}! 👋\nAsosiy menyudan foydalanishingiz mumkin:"
    await message.answer(text, reply_markup=main_menu_keyboard())

def register_handlers(dp: Dispatcher):
    """
    Handlerlarni ro‘yxatdan o‘tkazadi
    """
    # /start allaqachon bot.py da yozilgan
    # Agar callback orqali main menu chaqirilsa
    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def show_main_menu(call: types.CallbackQuery):
        await start_menu(call.message)
