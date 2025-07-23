import flet as ft
from views.login_view import LoginPage
from views.registration_view import RegistrationPage
from views.dashboard_view import DashboardPage
from views.analytics_view import MoodAnalyticsPage

def main(page: ft.Page):
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginPage(page, on_login_success))
        elif page.route == "/register":
            page.views.append(RegistrationPage(page))
        elif page.route == "/dashboard":
            user_id = page.session.get("user_id")
            if user_id:
                page.views.append(DashboardPage(page, user_id))
            else:
                page.go("/")
        elif page.route == "/analytics":
            user_id = page.session.get("user_id")
            if user_id:
                page.views.append(MoodAnalyticsPage(page, user_id))
            else:
                page.go("/")
        else:
            page.views.append(
                ft.View(
                    "/404",
                    controls=[
                        ft.Text("❌ 404 - Page Not Found", size=24),
                        ft.ElevatedButton("🔙 Back to Login", on_click=lambda e: page.go("/"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        page.update()

    def on_login_success(user_id):
        print(f"User logged in with ID: {user_id}")
        page.session.set("user_id", user_id)
        page.go("/dashboard")

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
