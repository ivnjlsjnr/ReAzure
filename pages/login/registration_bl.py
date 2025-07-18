import sqlite3
from datetime import datetime

def register_user(username: str, password: str, email: str = None) -> tuple[bool, str]:
    try:
        conn = sqlite3.connect("reazure.db")
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False, "Username already taken."

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
            (username, password, email, datetime.now().isoformat())
        )
        conn.commit()
        return True, "Registration successful!"
    except Exception as e:
        print("[Register] Error:", e)
        return False, "Registration failed. Try again."
    finally:
        conn.close()
