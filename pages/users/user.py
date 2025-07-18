# pages/users/user.py

import sqlite3
from datetime import datetime

class User:
    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email

    def register(self) -> tuple[bool, str]:
        try:
            conn = sqlite3.connect("reazure.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (self.username,))
            if cursor.fetchone():
                return False, "Username already exists."

            created_at = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
                (self.username, self.password, self.email, created_at)
            )
            conn.commit()
            return True, "Registration successful!"
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    def login(self) -> bool:
        try:
            conn = sqlite3.connect("reazure.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (self.username, self.password)
            )
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"[User Login] Error: {e}")
            return False
        finally:
            conn.close()

    def get_user_id(self) -> int | None:
        try:
            conn = sqlite3.connect("reazure.db")
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (self.username,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"[User ID Fetch] Error: {e}")
            return None
        finally:
            conn.close()
