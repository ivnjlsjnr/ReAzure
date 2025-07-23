# views/analytics_view.py

import flet as ft
from models.analytics_model import get_mood_data, generate_mood_chart_base64

def MoodAnalyticsPage(page: ft.Page, user_id: int):
    chart_column = ft.Column(spacing=20, alignment=ft.MainAxisAlignment.START)

    def load_chart():
        df = get_mood_data(user_id)
        chart_column.controls.clear()

        if df.empty:
            chart_column.controls.append(ft.Text("No mood data available."))
        else:
            base64_img = generate_mood_chart_base64(df)
            chart_column.controls.append(
                ft.Image(src_base64=base64_img, width=350)
            )

        page.update()

    load_chart()

    return ft.View(
        "/analytics",
        controls=[
            ft.AppBar(
                title=ft.Text("📊 Mood Analytics"),
                center_title=True,
                bgcolor=ft.Colors.BLUE_100,
                actions=[
                    ft.IconButton(icon=ft.Icons.REFRESH, tooltip="Refresh", on_click=lambda _: load_chart()),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Back", on_click=lambda _: page.go("/dashboard")),
                ]
            ),
            ft.Column([
                ft.Text("Your Mood Frequency", size=20, weight=ft.FontWeight.BOLD),
                chart_column
            ], spacing=20)
        ],
        padding=20,
        scroll=ft.ScrollMode.AUTO
    )
