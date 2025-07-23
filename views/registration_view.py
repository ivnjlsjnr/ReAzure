import flet as ft
from controllers.auth_controller import handle_register

def RegistrationPage(page: ft.Page):
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True)
    email = ft.TextField(label="Email (optional)")

    def register(e):
        success, message = handle_register(username.value.strip(), password.value.strip(), confirm_password.value.strip(), email.value.strip())
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()
        if success:
            page.go("/")

    return ft.View(
        "/register",
        controls=[
            ft.Image(src="Assets/ReAzure.png", width=120, height=120),
            ft.Text("Create an Account", size=24, weight="bold"),
            username,
            password,
            confirm_password,
            email,
            ft.ElevatedButton("Register", on_click=register),
            ft.TextButton("Back to Login", on_click=lambda e: page.go("/"))
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
