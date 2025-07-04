import flet as ft

def DashboardPage(page: ft.Page):
    return ft.View(
        "/dashboard",
        controls=[
            ft.Text("✅ Welcome to the Dashboard!", size=24),
            ft.ElevatedButton("Logout", on_click=lambda e: page.go("/"))
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
