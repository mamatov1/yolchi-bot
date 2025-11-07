from aiogram import types, Dispatcher
from keyboards.account_menu import account_menu_keyboard
from keyboards.main_menu import main_menu_keyboard
from database.db import get_user, update_diamonds

# Hisob raqamni ko‘rsatish
async def show_account(message: types.Message):
    user = get_user(message.from_user.id)
    text = (
        f"💎 Hisob raqam:\n"
        f"F.I.Sh: {user['first_name']} {user['last_name']}\n"
        f"Olmoslar: {user.get('diamonds', 0)}"
    )
    await message.answer(text, reply_markup=account_menu_keyboard())

# Tarif sotib olish (mock payment)
async def buy_tariff(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    diamonds = user.get('diamonds', 0)

    # Tariflar
    tariffs = {
        "tariff_rocket": {"name": "Raketa", "cost": 1},
        "tariff_lightning": {"name": "Chaqmoq", "cost": 5},
        "tariff_comet": {"name": "Kometa", "cost": 10}
    }

    selected = call.data
    tariff = tariffs.get(selected)

    if diamonds >= tariff["cost"]:
        # Olmoslarni yechish
        new_balance = diamonds - tariff["cost"]
        update_diamonds(call.from_user.id, new_balance)
        await call.message.answer(f"✅ {tariff['name']} tarifi sotib olindi!\nYangi balans: {new_balance} 💎", reply_markup=main_menu_keyboard())
    else:
        await call.message.answer("❌ Yetarli olmos yo‘q!", reply_markup=main_menu_keyboard())
    await call.answer()

# Bekor qilish
async def cancel_purchase(call: types.CallbackQuery):
    await call.message.answer("❌ To‘lov bekor qilindi.", reply_markup=main_menu_keyboard())
    await call.answer()

# Handlerlarni ro‘yxatdan o‘tkazish
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_account, lambda message: message.text in ["💎 Hisob raqam", "account"], state="*")
    dp.register_callback_query_handler(buy_tariff, lambda c: c.data in ["tariff_rocket", "tariff_lightning", "tariff_comet"], state="*")
    dp.register_callback_query_handler(cancel_purchase, lambda c: c.data == "cancel", state="*")
