import flet as ft

def DashboardPage(page: ft.Page):
    def logout(e):  
        page.go("/")

    return ft.View(
        "/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text(" ReAzure Dashboard"),
                actions=[
                    ft.IconButton(icon=ft.icons.LOGOUT, tooltip="Logout", on_click=logout)
                ],
                bgcolor=ft.colors.BLUE_200
            ),
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                ft.Column([
                                    ft.Text(" Users", size=18, weight="bold"),
                                    ft.Text("1245", size=32, weight="w900")
                                ]),
                                padding=20,
                                bgcolor=ft.colors.BLUE_100,
                                border_radius=10,
                                expand=True,
                            ),
                            ft.Container(
                                ft.Column([
                                    ft.Text("🟢 Active Sessions", size=18, weight="bold"),
                                    ft.Text("87", size=32, weight="w900")
                                ]),
                                padding=20,
                                bgcolor=ft.colors.GREEN_100,
                                border_radius=10,
                                expand=True,
                            ),
                        ],
                        spacing=20
                    ),
                    ft.Container(height=20),
                    ft.Text("📈 System Overview", size=20, weight="bold"),
                    ft.Container(
                        ft.Text("Placeholder for charts, graphs, or logs..."),
                        height=200,
                        bgcolor=ft.colors.GREY_200,
                        border_radius=10,
                        padding=20
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=20,
                padding=20
            )
        ]
    )
