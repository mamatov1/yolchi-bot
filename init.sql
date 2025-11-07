-- users jadvali
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
);

-- goals jadvali
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    purpose TEXT,
    friends TEXT,
    duration TEXT,
    category TEXT,
    channel_posted INTEGER DEFAULT 0,
    tariff TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(telegram_id)
);
