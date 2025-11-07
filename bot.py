import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, CHANNEL_ID, ADMIN_ID

# Handlers import
from handlers import start_handler, goals_handler, profile_handler, account_handler, recommendations_handler, about_handler, payments_handler

# Logger sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Handlerlarni ro‘yxatdan o‘tkazish
start_handler.register_handlers(dp)
goals_handler.register_handlers(dp)
profile_handler.register_handlers(dp)
account_handler.register_handlers(dp)
recommendations_handler.register_handlers(dp)
about_handler.register_handlers(dp)
payments_handler.register_handlers(dp)

# /start komandasi
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user = start_handler.add_user_if_not_exists(message.from_user)
    # Kanalga obuna tekshirish
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if member.status in ["left", "kicked"]:
            await message.answer(
                "Iltimos, kanalga obuna bo‘ling:",
                reply_markup=start_handler.subscription_keyboard()
            )
        else:
            await start_handler.show_main_menu(message)
    except Exception:
        await message.answer(
            "Iltimos, kanalga obuna bo‘ling:",
            reply_markup=start_handler.subscription_keyboard()
        )

# Kanal obunani tekshirish tugmasi
@dp.callback_query_handler(lambda c: c.data == "check_subscription")
async def check_subscription(call: types.CallbackQuery):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, call.from_user.id)
        if member.status in ["left", "kicked"]:
            await call.message.answer("❌ Siz hali kanalga obuna bo‘lmadingiz.")
        else:
            await call.message.answer("✅ Obuna tasdiqlandi!")
            await start_handler.show_main_menu(call.message)
    except Exception:
        await call.message.answer("❌ Xatolik yuz berdi. Qayta urinib ko‘ring.")
    await call.answer()

# Fallback: boshqa xabarlar
@dp.message_handler()
async def fallback(message: types.Message):
    await message.answer("❌ Iltimos, menyudan birini tanlang.")

# Botni ishga tushurish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
