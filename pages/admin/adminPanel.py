import flet as ft
from pages.admin.AdminDA import get_all_users
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import io
import base64


def get_user_mood_distribution(user_id):
    with sqlite3.connect("reazure.db") as conn:
        df = pd.read_sql_query("""
            SELECT emoji AS mood, COUNT(*) AS count
            FROM moods
            WHERE user_id = ?
            GROUP BY mood
        """, conn, params=(user_id,))
    return df


def generate_mood_pie_chart(df):
    fig, ax = plt.subplots()
    ax.pie(df["count"], labels=df["mood"], autopct='%1.1f%%', startangle=140)
    ax.axis("equal")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return encoded


def AdminDashboard(page: ft.Page):
    users_table = ft.Column(spacing=20)

    def format_datetime(created_at_str):
        try:
            if "." in created_at_str:
                created_at_str = created_at_str.split(".")[0]
            dt = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"[Time Format Error] {e}")
            return "N/A"

    def load_users():
        users_table.controls.clear()
        users = get_all_users()

        if users:
            for user in users:
                user_id, username, email, created_at = user
                formatted_dt = format_datetime(created_at) if created_at else "N/A"

                # User info
                user_info = ft.Text(
                    f"🆔 {user_id} | 👤 {username} | 📧 {email or 'N/A'} | 📅 {formatted_dt}",
                    size=16
                )

                df = get_user_mood_distribution(user_id)

                # Analytics section toggle
                chart_section = ft.Column(visible=False)

                def toggle_chart(e, section=chart_section, data=df):
                    if not data.empty and not section.controls:
                        chart_b64 = generate_mood_pie_chart(data)
                        section.controls.append(ft.Image(src_base64=chart_b64, width=250))
                    section.visible = not section.visible
                    page.update()

                toggle_button = ft.ElevatedButton(
                    "📈 View Mood Analytics",
                    on_click=lambda e, s=chart_section, d=df: toggle_chart(e, s, d)
                )

                users_table.controls.append(
                    ft.Container(
                        content=ft.Column([
                            user_info,
                            toggle_button,
                            chart_section,
                        ]),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=8
                    )
                )
        else:
            users_table.controls.append(ft.Text("No users found."))

        page.update()

    load_users()

    return ft.View(
        "/admin",
        controls=[
            ft.Image(src="Assets/ReAzure.png", width=140, height=140),
            ft.Text("👑 Admin Panel - ReAzure", size=28, weight="bold"),
            ft.Divider(),
            ft.ElevatedButton("🔄 Refresh User List", on_click=lambda e: load_users()),
            ft.Container(users_table, padding=20),
            ft.Divider(),
            ft.ElevatedButton("🚪 Logout", on_click=lambda e: page.go("/")),
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )
