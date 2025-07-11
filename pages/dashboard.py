import flet as ft

def DashboardPage(page: ft.Page):
    return ft.View(
        "/dashboard",
        controls=[
            ft.Column(
                controls=[
                    ft.Image(src="Assets/ReAzure.png", width=160, height=160),  # Bigger logo
                    ft.Text("Welcome to ReAzure", size=26, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Text("What would you like to do today?", size=18),

            ft.Column(
                controls=[
                    ft.ElevatedButton("Log My Mood", on_click=lambda e: page.go("/mood")),
                    ft.ElevatedButton("Write in Journal", on_click=lambda e: page.go("/journal")),
                    ft.ElevatedButton("View My Mood Trends", on_click=lambda e: page.go("/analytics")),
                    ft.ElevatedButton("Wellness Recommendations", on_click=lambda e: page.go("/recommendations")),
                    ft.ElevatedButton("Logout", on_click=lambda e: page.go("/")),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=30
    )
