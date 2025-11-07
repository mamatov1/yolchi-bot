from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.goals_menu import goals_menu_keyboard, duration_keyboard, confirm_keyboard
from keyboards.categories import categories_keyboard
from keyboards.tariffs import tariffs_keyboard
from database import db
from utils.image_generator import generate_goal_image

# ==========================
# FSM Maqsad yaratish
# ==========================
class GoalFSM(StatesGroup):
    title = State()
    description = State()
    purpose = State()
    friends = State()
    duration = State()
    category = State()
    confirm_channel = State()
    tariff = State()

# ==========================
# Goals menu
# ==========================
async def goals_menu(message: types.Message):
    await message.answer("📌 Maqsadlar menyusi:", reply_markup=goals_menu_keyboard())

# ==========================
# Maqsad yaratish
# ==========================
async def create_goal_start(message: types.Message):
    await GoalFSM.title.set()
    await message.answer("✍️ Maqsad nomini kiriting:")

async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await GoalFSM.next()
    await message.answer("Maqsad tavsifini yozing:")

async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await GoalFSM.next()
    await message.answer("Siz nimaga erishmoqchisiz?")

async def process_purpose(message: types.Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await GoalFSM.next()
    await message.answer("Qanday maqsaddosh qidiryapsiz? 🤝")

async def process_friends(message: types.Message, state: FSMContext):
    await state.update_data(friends=message.text)
    await GoalFSM.next()
    await message.answer("Maqsad necha kun davom etadi?", reply_markup=duration_keyboard())

async def process_duration(callback: types.CallbackQuery, state: FSMContext):
    # Callback data raqam bo‘lishi kerak: 7,14,21,28
    if callback.data.isdigit():
        await state.update_data(duration=int(callback.data))
        await GoalFSM.next()
        await callback.message.answer("Maqsad kategoriyasini tanlang:", reply_markup=categories_keyboard())
        await callback.answer()

async def process_category(callback: types.CallbackQuery, state: FSMContext):
    # Callback data: cat_<category_name>
    category = callback.data.replace("cat_", "")
    await state.update_data(category=category)
    await GoalFSM.next()
    await callback.message.answer("Kanalga joylashilsinmi?", reply_markup=confirm_keyboard())
    await callback.answer()

async def process_confirm(callback: types.CallbackQuery, state: FSMContext):
    # yes / no
    await state.update_data(confirm_channel=callback.data)
    await GoalFSM.next()
    await callback.message.answer("Tarifni tanlang:", reply_markup=tariffs_keyboard())
    await callback.answer()

async def process_tariff(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff = callback.data  # raketa / chaqmoq / kometa
    await state.update_data(tariff=tariff)

    # Mock payment: diamonds kamaytirish
    user = db.get_user(callback.from_user.id)
    if not user:
        db.add_user(callback.from_user.id, callback.from_user.first_name)
        user = db.get_user(callback.from_user.id)

    tariff_diamonds = {"raketa":1,"chaqmoq":5,"kometa":10}.get(tariff, 1)

    if user["diamonds"] < tariff_diamonds:
        await callback.message.answer("❌ Sizda yetarli olmos yo‘q.")
        await state.finish()
        await callback.answer()
        return

    db.update_diamonds(callback.from_user.id, user["diamonds"] - tariff_diamonds)
    db.add_goal(
        telegram_id=callback.from_user.id,
        title=data["title"],
        desc=data["description"],
        purpose=data.get("purpose",""),
        friends=data.get("friends",""),
        duration=data.get("duration",7),
        category=data.get("category",""),
        confirm_channel=data.get("confirm_channel","no"),
        tariff=tariff,
        paid=1
    )

    # Kanalga post (agar user ruxsat bergan bo‘lsa)
    if data.get("confirm_channel") == "yes":
        img_path = generate_goal_image(data["title"], data["description"])
        try:
            channel_id = -1001234567890  # O‘zingizning kanal ID sini qo‘ying
            await callback.message.bot.send_photo(
                chat_id=channel_id,
                photo=open(img_path,"rb"),
                caption=f"📌 {data['title']}\n{data['description']}\nKategoriya: {data.get('category')}\nTarif: {tariff_diamonds} 💎"
            )
        except Exception as e:
            await callback.message.answer(f"Kanalga post berishda xatolik: {e}")

    await callback.message.answer("✅ Maqsad muvaffaqiyatli yaratildi!")
    await state.finish()
    await callback.answer()

# ==========================
# Register handlers
# ==========================
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(goals_menu, commands=["goals"])
    dp.register_message_handler(create_goal_start, lambda m: m.text=="Maqsad yaratish")
    dp.register_message_handler(process_title, state=GoalFSM.title)
    dp.register_message_handler(process_description, state=GoalFSM.description)
    dp.register_message_handler(process_purpose, state=GoalFSM.purpose)
    dp.register_message_handler(process_friends, state=GoalFSM.friends)

    dp.register_callback_query_handler(process_duration, lambda c: c.data.isdigit(), state=GoalFSM.duration)
    dp.register_callback_query_handler(process_category, lambda c: c.data.startswith("cat_"), state=GoalFSM.category)
    dp.register_callback_query_handler(process_confirm, lambda c: c.data in ["yes","no"], state=GoalFSM.confirm_channel)
    dp.register_callback_query_handler(process_tariff, lambda c: c.data in ["raketa","chaqmoq","kometa"], state=GoalFSM.tariff)
