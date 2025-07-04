import flet as ft

def LoginPage(page: ft.Page):
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    def login(e):
        try:
            print("Login button pressed")  # Debug
            with open("user.txt", "r") as f:
                users = [line.strip().split(",") for line in f if "," in line]
            print("Loaded users:", users)  # Debug
            uname = username.value.strip()
            pword = password.value.strip()
            if any(uname == u.strip() and pword == p.strip() for u, p in users):
                print("Login successful")  # Debug
                page.go("/dashboard")
            else:
                print("Invalid login")  # Debug
                page.snack_bar = ft.SnackBar(ft.Text("Invalid login 😓"))
                page.snack_bar.open = True
                page.update()
        except Exception as ex:
            print("Error:", ex)  # Debug
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
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
