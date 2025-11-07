from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.profile_menu import profile_menu_keyboard
from keyboards.main_menu import main_menu_keyboard
from database.db import get_user, update_diamonds

# FSM holatlari
class ProfileStates(StatesGroup):
    name = State()
    surname = State()
    gender = State()
    phone = State()
    birthday = State()
    location = State()
    bio = State()

# Profilni ko‘rsatish
async def show_profile(message: types.Message):
    user = get_user(message.from_user.id)
    text = (
        f"👤 Profil ma’lumotlari:\n"
        f"Ism: {user['first_name']}\n"
        f"Familiya: {user['last_name']}\n"
        f"Jins: {user.get('gender', '—')}\n"
        f"Telefon: {user.get('phone', '—')}\n"
        f"Tug‘ilgan sana: {user.get('birthday', '—')}\n"
        f"Joylashuv: {user.get('location', '—')}\n"
        f"Bio: {user.get('bio', '—')}\n"
        f"Olmoslar: {user.get('diamonds', 0)} 💎"
    )
    await message.answer(text, reply_markup=profile_menu_keyboard())

# Profilni tahrirlash start
async def edit_profile_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ismingizni kiriting:")
    await ProfileStates.name.set()
    await call.answer()

# FSM: Ism
async def profile_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await ProfileStates.next()

# FSM: Familiya
async def profile_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Jinsingizni kiriting (Erkak / Ayol):")
    await ProfileStates.next()

# FSM: Gender
async def profile_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await ProfileStates.next()

# FSM: Phone
async def profile_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Tug‘ilgan sanangizni kiriting (YYYY-MM-DD):")
    await ProfileStates.next()

# FSM: Birthday
async def profile_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer("Joylashuvingizni kiriting:")
    await ProfileStates.next()

# FSM: Location
async def profile_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Bio yozing:")
    await ProfileStates.next()

# FSM: Bio
async def profile_bio(message: types.Message, state: FSMContext):
    await state.update_data(bio=message.text)
    data = await state.get_data()
    # DB ga saqlash
    user = get_user(message.from_user.id)
    conn = __import__("sqlite3").connect("database/yolchi.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users SET first_name=?, last_name=?, gender=?, phone=?, birthday=?, location=?, bio=?
        WHERE telegram_id=?
        """,
        (
            data['name'],
            data['surname'],
            data['gender'],
            data['phone'],
            data['birthday'],
            data['location'],
            data['bio'],
            message.from_user.id
        )
    )
    conn.commit()
    conn.close()
    await message.answer("✅ Profil yangilandi!", reply_markup=profile_menu_keyboard())
    await state.finish()

# Handlerlarni ro‘yxatdan o‘tkazish
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_profile, lambda message: message.text in ["👤 Profil", "profile"], state="*")
    dp.register_callback_query_handler(edit_profile_start, lambda c: c.data == "edit_profile", state="*")
    dp.register_message_handler(profile_name, state=ProfileStates.name)
    dp.register_message_handler(profile_surname, state=ProfileStates.surname)
    dp.register_message_handler(profile_gender, state=ProfileStates.gender)
    dp.register_message_handler(profile_phone, state=ProfileStates.phone)
    dp.register_message_handler(profile_birthday, state=ProfileStates.birthday)
    dp.register_message_handler(profile_location, state=ProfileStates.location)
    dp.register_message_handler(profile_bio, state=ProfileStates.bio)
