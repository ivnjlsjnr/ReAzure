import flet as ft
from pages.login.login import LoginPage
from pages.users.dashboard import DashboardPage
from pages.admin.adminPanel import AdminDashboard
from pages.login.registration import RegistrationPage
from pages.users.analytics import MoodAnalyticsPage

def main(page: ft.Page):
    page.title = "ReAzure"
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 700

    # Store logged-in user ID here as a page attribute
    page.user_id = None

    def route_change(route):
        print(f"[Router] Navigating to: {page.route}")
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginPage(page, on_login_success=on_login_success))

        elif page.route == "/dashboard":
            if page.user_id is None:
                page.go("/")
                return
            page.views.append(DashboardPage(page, user_id=page.user_id))

        elif page.route == "/admin":
            page.views.append(AdminDashboard(page))

        elif page.route == "/register":
            page.views.append(RegistrationPage(page))

        elif page.route == "/analytics":
            if page.user_id is None:
                page.go("/")
                return
            page.views.append(MoodAnalyticsPage(page, user_id=page.user_id))

        else:
            page.views.append(
                ft.View(
                    "/404",
                    controls=[
                        ft.Text("❌ 404 - Page Not Found", size=24),
                        ft.ElevatedButton("🔙 Go back to Login", on_click=lambda e: page.go("/"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        page.update()

    def on_login_success(user_id):
        print(f"User logged in with ID: {user_id}")
        page.user_id = user_id
        page.go("/dashboard")

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
