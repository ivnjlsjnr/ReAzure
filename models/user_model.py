import requests

API_BASE_URL = "http://127.0.0.1:8000"

class User:
    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email

    def register(self) -> tuple[bool, str]:
        try:
            response = requests.post(f"{API_BASE_URL}/users/register", json={
                "username": self.username,
                "password": self.password,
                "email": self.email
            })
            if response.status_code == 200:
                return True, response.json().get("message", "Registration successful.")
            return False, response.json().get("detail", "Registration failed.")
        except Exception as e:
            return False, f"[Register Error] {e}"

    def login(self) -> tuple[bool, str]:
        try:
            response = requests.post(f"{API_BASE_URL}/users/login", json={
                "username": self.username,
                "password": self.password
            })
            if response.status_code == 200:
                return True, response.json().get("message", "Login successful.")
            return False, response.json().get("detail", "Login failed.")
        except Exception as e:
            return False, f"[Login Error] {e}"

    def get_user_id(self) -> int | None:
        try:
            response = requests.get(
                f"{API_BASE_URL}/users/get-id",
                params={"username": self.username}
            )
            if response.status_code == 200:
                return response.json().get("user_id")
            print(f"[User ID Fetch] Failed: {response.status_code} — {response.text}")
            return None
        except Exception as e:
            print(f"[User ID Fetch] Error: {e}")
            return None
