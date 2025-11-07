import sqlite3
from pathlib import Path

# =========================
# DB Fayl manzili
# =========================
DB_PATH = Path(__file__).parent / "yolchi.db"

# =========================
# DB Ulash
# =========================
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# DB Init (jadval yaratish)
# =========================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Foydalanuvchilar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            phone TEXT,
            birthday TEXT,
            location TEXT,
            bio TEXT,
            diamonds INTEGER DEFAULT 0
        )
    """)

    # Maqsadlar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            title TEXT,
            description TEXT,
            purpose TEXT,
            friends TEXT,
            duration INTEGER,
            category TEXT,
            confirm_channel TEXT,
            tariff TEXT,
            paid INTEGER DEFAULT 0,
            start_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# =========================
# Foydalanuvchi qo‘shish / olish
# =========================
def add_user(telegram_id, first_name="", last_name="", diamonds=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id, first_name, last_name, diamonds) VALUES (?, ?, ?, ?)",
                   (telegram_id, first_name, last_name, diamonds))
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def update_diamonds(telegram_id, diamonds):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET diamonds = ? WHERE telegram_id = ?", (diamonds, telegram_id))
    conn.commit()
    conn.close()

# =========================
# Maqsad qo‘shish
# =========================
def add_goal(telegram_id, title, desc, purpose="", friends="", duration=7, category="", confirm_channel="no", tariff="raketa", paid=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (telegram_id, title, description, purpose, friends, duration, category, confirm_channel, tariff, paid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (telegram_id, title, desc, purpose, friends, duration, category, confirm_channel, tariff, paid))
    conn.commit()
    conn.close()
