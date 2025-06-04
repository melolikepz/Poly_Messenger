import sqlite3
from sqlite3 import Error


def create_connection():
    """Create a database connection"""
    conn = None
    try:
        conn = sqlite3.connect('mydata.db')
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn


def init_db():
    """Initialize database tables"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users (id),
                    FOREIGN KEY (receiver_id) REFERENCES users (id)
                )
            ''')

            conn.commit()
            print("Tables created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            conn.close()


def add_user(username, password, phone=None):
    """Add new user to database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, phone) VALUES (?, ?, ?)",
                (username, password, phone)
            )
            conn.commit()
            print("User added successfully")
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False
        finally:
            conn.close()
    return False


def check_user(username, password):
    """Check if user exists and credentials are correct"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            return user is not None
        except Error as e:
            print(f"The error '{e}' occurred")
            return False
        finally:
            conn.close()
    return False


def get_user_by_username(username):
    """Get user by username"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            return cursor.fetchone()
        except Error as e:
            print(f"The error '{e}' occurred")
            return None
        finally:
            conn.close()
    return None


# Initialize database when this module is imported
init_db()