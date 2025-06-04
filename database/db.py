import sqlite3


def init_db():
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()

    # ایجاد جدول کاربران
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

    # ایجاد جدول پیام‌ها
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        time TEXT
    )
    ''')

    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def check_user(username, password):
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None