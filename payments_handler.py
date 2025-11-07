# handlers/payments_handler.py
from aiogram import types, Dispatcher
from database.db import get_connection

# Mock payment system: olmoslarni cheklash va kanalga post qilish
async def process_payment(user_id: int, tariff_olmos: int, goal_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Foydalanuvchi olmosini tekshirish
    cursor.execute("SELECT diamonds FROM users WHERE telegram_id=?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "Foydalanuvchi topilmadi"

    if user['diamonds'] < tariff_olmos:
        conn.close()
        return False, "❌ Yetarli olmos yo‘q"

    # Olmoslarni yechib olish
    new_diamonds = user['diamonds'] - tariff_olmos
    cursor.execute("UPDATE users SET diamonds=? WHERE telegram_id=?", (new_diamonds, user_id))

    # Maqsadni kanalga post qilinishini belgilash
    cursor.execute("UPDATE goals SET channel_posted=1 WHERE id=?", (goal_id,))

    conn.commit()
    conn.close()
    return True, f"✅ To‘lov muvaffaqiyatli amalga oshirildi. Olmoslar: {tariff_olmos}"
