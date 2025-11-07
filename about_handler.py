from aiogram import types, Dispatcher
from keyboards.main_menu import main_menu_keyboard

async def about_bot(message: types.Message):
    text = (
        "ℹ️ Yo‘lchi — insonning hayot yo‘lini ongli boshqarishga yordam beradigan "
        "shaxsiy rivojlanish botidir.\n\n"
        "Har bir foydalanuvchi o‘z hayotining muallifi bo‘lishi uchun yordam beradi."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(about_bot, lambda message: message.text in ["ℹ️ Biz haqimizda", "about"], state="*")
