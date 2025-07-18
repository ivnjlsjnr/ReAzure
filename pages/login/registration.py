# registration.py

import flet as ft
from pages.users.user import User

def RegistrationPage(page: ft.Page):
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True)
    email = ft.TextField(label="Email (optional)")

    def handle_register(e):
        uname = username.value.strip()
        pword = password.value.strip()
        cpword = confirm_password.value.strip()
        user_email = email.value.strip()

        if not uname or not pword or not cpword:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill in all required fields."))
            page.snack_bar.open = True
            page.update()
            return

        if pword != cpword:
            page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match."))
            page.snack_bar.open = True
            page.update()
            return

        new_user = User(uname, pword, user_email)
        success, message = new_user.register()
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

        if success:
            page.go("/")  # Back to login

    return ft.View(
        "/register",
        controls=[
            ft.Image(src="Assets/ReAzure.png", width=120, height=120),
            ft.Text("Create an Account", size=24, weight="bold"),
            username,
            password,
            confirm_password,
            email,
            ft.ElevatedButton("Register", on_click=handle_register),
            ft.TextButton("Back to Login", on_click=lambda e: page.go("/"))
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
