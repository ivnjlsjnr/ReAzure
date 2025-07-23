from models.user_model import User

def handle_register(username: str, password: str, confirm_password: str, email: str = None) -> tuple[bool, str]:
    if not username or not password or not confirm_password:
        return False, "Please fill in all required fields."

    if password != confirm_password:
        return False, "Passwords do not match."

    user = User(username, password, email)
    return user.register()

def handle_login(username: str, password: str) -> tuple[bool, int | None, str]:
    user = User(username, password)
    success, message = user.login()

    if success:
        user_id = user.get_user_id()
        if user_id:
            return True, user_id, "Login successful!"
        return False, None, "User ID not found."
    return False, None, message
