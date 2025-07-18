import sqlite3

def create_tables():
    conn = sqlite3.connect("reazure.db")
    cursor = conn.cursor()

    # Users table with email and created_at
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
    ''')

    # Moods table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            mood_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            emoji TEXT NOT NULL,
            intensity INTEGER,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # Journals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journals (
            journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood_id INTEGER,
            content TEXT NOT NULL,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (mood_id) REFERENCES moods(mood_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ SQLite database schema created!")

if __name__ == "__main__":
    create_tables()
