import flet as ft

def LoginPage(page: ft.Page):
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    def login(e):
        if username.value == "admin" and password.value == "1234":
            page.go("/dashboard")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid login 😓"))
            page.snack_bar.open = True
            page.update()

    return ft.View(
        "/",
        controls=[
            ft.Text("🔐 Log into ReAzure", size=24, weight="bold"),
            username,
            password,
            ft.ElevatedButton("Login", on_click=login)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
