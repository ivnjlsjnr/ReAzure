import flet as ft
from login_bl import validate_login  # ✅ Import the business logic

def LoginPage(page: ft.Page):
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    def login(e):
        uname = username.value.strip()
        pword = password.value.strip()
        
        if validate_login(uname, pword):  # ✅ Use logic layer
            print("Login successful")
            page.go("/dashboard")
        else:
            print("Invalid login")
            page.snack_bar = ft.SnackBar(ft.Text("Invalid login 😓"))
            page.snack_bar.open = True
            page.update()

    return ft.View(
        "/",
        controls=[
            ft.Image(src="Assets/ReAzure.png", width=120, height=120),  
            ft.Text("🔐 Log into ReAzure", size=24, weight="bold"),
            username,
            password,
            ft.ElevatedButton("Login", on_click=login)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
