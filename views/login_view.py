import flet as ft
from controllers.auth_controller import handle_login

def LoginPage(page: ft.Page, on_login_success):
    page.theme_mode = ft.ThemeMode.LIGHT

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    def login(e):
        success, user_id, message = handle_login(username.value.strip(), password.value.strip())
        if success:
            on_login_success(user_id)
        else:
            page.snack_bar = ft.SnackBar(ft.Text(message))
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
