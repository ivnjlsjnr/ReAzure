#login_bl.py
import sqlite3

def check_admin_login(username: str, password: str) -> bool:
    try:
        with open("admin.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "," not in line:
                    continue
                u, p = line.split(",", 1)
                if username.strip() == u.strip() and password.strip() == p.strip():
                    return True
    except FileNotFoundError:
        print("[Admin Login] admin.txt not found.")
    except Exception as e:
        print(f"[Admin Login] Unexpected error: {e}")
    return False


def check_user_login(username: str, password: str) -> bool:
    """
    Check if the given credentials exist in the SQLite database users table.
    """
    try:
        conn = sqlite3.connect("reazure.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username.strip(), password.strip())
        )
        user = cursor.fetchone()
        return user is not None
    except sqlite3.OperationalError as oe:
        print(f"[User Login] Database operation error: {oe}")
    except Exception as e:
        print(f"[User Login] Unexpected error: {e}")
    finally:
        conn.close()
    return False


def validate_login(username: str, password: str) -> str | None:
    """
    Validates login credentials and returns 'admin', 'user', or None.
    """
    if check_admin_login(username, password):
        return "admin"
    elif check_user_login(username, password):
        return "user"
    else:
        return None
