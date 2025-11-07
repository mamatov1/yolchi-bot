import os

# =========================
# BOT TOKEN
# =========================
# Telegram Bot Token (BotFather orqali oling)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8578100062:AAEUdemzFCKeLan_la6QW58gGMFiWavS-bs")

# =========================
# Kanal ID
# =========================
# Masalan: -1001234567890
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002434635006"))

# =========================
# Admin ID
# =========================
# Sizning Telegram ID, botga admin funksiyalarini berish uchun
ADMIN_ID = int(os.getenv("ADMIN_ID", "7903688837"))

# =========================
# Tarifflar qiymati (olmoslar)
# =========================
TARIFFS = {
    "raketa": {"price": 4900, "diamonds": 1},
    "chaqmoq": {"price": 21900, "diamonds": 5},
    "kometa": {"price": 39900, "diamonds": 10}
}

# =========================
# Boshqa sozlamalar
# =========================
# Misol: default maqsad davomiyligi
DEFAULT_GOAL_DURATION = 7
