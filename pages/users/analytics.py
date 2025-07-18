import matplotlib
matplotlib.use("Agg")

import flet as ft
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import io
import base64


def get_mood_data(user_id: int):
    with sqlite3.connect("reazure.db") as conn:
        df = pd.read_sql_query("""
            SELECT emoji AS mood, COUNT(*) as count
            FROM moods
            WHERE user_id = ?
            GROUP BY mood
            ORDER BY count DESC
        """, conn, params=(user_id,))
    return df


def plot_mood_chart(df):
    fig, ax = plt.subplots()
    ax.bar(df["mood"], df["count"], color="skyblue")
    ax.set_title("Mood Frequency")
    ax.set_xlabel("Mood")
    ax.set_ylabel("Count")
    plt.xticks(rotation=30)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return encoded


def MoodAnalyticsPage(page: ft.Page, user_id: int):
    chart_column = ft.Column(spacing=20, alignment=ft.MainAxisAlignment.START)

    def load_chart():
        df = get_mood_data(user_id)
        chart_column.controls.clear()

        if df.empty:
            chart_column.controls.append(ft.Text("No mood data available."))
        else:
            img_data = plot_mood_chart(df)
            chart_column.controls.append(
                ft.Image(src_base64=img_data, width=350)
            )

        page.update()

    # Initial chart load
    load_chart()

    return ft.View(
        "/analytics",
        controls=[
            ft.AppBar(
                title=ft.Text("📊 Mood Analytics"),
                center_title=True,
                bgcolor=ft.Colors.BLUE_100,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        tooltip="Refresh Chart",
                        on_click=lambda _: load_chart()
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Back to Dashboard",
                        on_click=lambda _: page.go("/dashboard")
                    )
                ]
            ),
            ft.Column(
                [
                    ft.Text("Your Mood Frequency", size=20, weight=ft.FontWeight.BOLD),
                    chart_column
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START
            )
        ],
        padding=20,
        scroll=ft.ScrollMode.AUTO
    )
