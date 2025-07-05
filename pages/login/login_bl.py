# login_bl.py
from login_dataAccess import load_users

def validate_login(username: str, password: str, file_path: str = "user.txt") -> bool:
    users = load_users(file_path)
    return any(username.strip() == u and password.strip() == p for u, p in users)
