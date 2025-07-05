import flet as ft
from pages.login.login import LoginPage
from pages.dashboard import DashboardPage

def main(page: ft.Page):
    page.title = "ReAzure"
    page.theme_mode = "light"

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(LoginPage(page))
        elif page.route == "/dashboard":
            page.views.append(DashboardPage(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
