# login.py
import flet as ft
from .login_bl import validate_login
from pages.users.user import User

def LoginPage(page: ft.Page, on_login_success):
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    def login(e):
        uname = username.value.strip()
        pword = password.value.strip()

        role = validate_login(uname, pword)

        if role == "admin":
            print("Admin login ✅")
            page.go("/admin")
        elif role == "user":
            print("User login ✅")
            user = User(uname, pword)
            user_id = user.get_user_id()
            if user_id:
                on_login_success(user_id)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("User ID not found."))
                page.snack_bar.open = True
                page.update()
        else:
            print("Login failed ❌")
            page.snack_bar = ft.SnackBar(ft.Text("Invalid credentials."))
            page.snack_bar.open = True
            page.update()

    def go_register(e):
        page.go("/register")

    return ft.View(
        "/",
        controls=[
            ft.Image(src="Assets/ReAzure.png", width=300, height=300),
            ft.Text("Log into ReAzure", size=24, weight="bold"),
            username,
            password,
            ft.ElevatedButton("Login", on_click=login),
            ft.TextButton("Don't have an account? Register here", on_click=go_register)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
