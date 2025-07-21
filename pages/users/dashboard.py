import flet as ft
import sqlite3
import requests
from datetime import datetime, timedelta


def get_username(user_id: int) -> str:
    with sqlite3.connect("reazure.db") as conn:
        row = conn.execute("SELECT username FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return row[0] if row else "Guest"

def get_saved_moods(user_id: int):
    with sqlite3.connect("reazure.db") as conn:
        return conn.execute("""
            SELECT moods.emoji, moods.timestamp, journals.content
            FROM moods
            JOIN journals ON moods.mood_id = journals.mood_id
            WHERE moods.user_id = ?
            ORDER BY moods.timestamp DESC
        """, (user_id,)).fetchall()


# --- SMART ZEN QUOTE FETCHER ---
def get_quote(keyword=None):
    try:
        url = "https://zenquotes.io/api/quotes"
        response = requests.get(url, timeout=5)
        data = response.json()

        if isinstance(data, list) and data:
            if keyword:
                keyword_lower = keyword.lower()
                for quote in data:
                    if keyword_lower in quote["q"].lower():
                        return f'"{quote["q"]}" — {quote["a"]}', keyword
                return f'"{data[0]["q"]}" — {data[0]["a"]}', "random (fallback)"
            else:
                return f'"{data[0]["q"]}" — {data[0]["a"]}', "random"
    except Exception as e:
        print("[QUOTE ERROR]", e)
    return "✨ Couldn't fetch quote. Try again!", "none"


# --- MOOD TO KEYWORD MAPPING ---
MOOD_KEYWORDS = {
    "Sad": "Pain",
    "Ecstatic": "Happiness",
    "Excited": "Dreams",
    "Bored": "Time",
    "Tired": "Work",
    "Happy": "Happiness",
    "Calm": "Freedom",
    "Stressed": "Anxiety",
    "Worried": "Fear"
}


def DashboardPage(page: ft.Page, user_id: int):
    username = get_username(user_id)
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    selected_emoji = {"file": "", "label": ""}
    chosen_date = ft.Text("")
    journal_input = ft.TextField(label="Describe your day", multiline=True, min_lines=3, width=300)
    result_view = ft.Text("")

    now = datetime.now()
    first_day = now.replace(day=1)
    last_day = (now.replace(month=now.month % 12 + 1, day=1) - timedelta(days=1))
    mood_cards_column = ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER)

    quote_text = ft.Text("Choose your mood to get inspired...", italic=True, color=ft.Colors.BLUE_400, size=14)
    quote_keyword_label = ft.Text("", size=12, italic=True, color=ft.Colors.BLUE_100)
    more_btn = ft.TextButton("More", visible=False)

    def update_quote(keyword=None):
        quote, used_keyword = get_quote(keyword)
        quote_text.value = quote
        quote_keyword_label.value = f"(keyword: {used_keyword})"
        more_btn.visible = True
        page.update()

    def show_journal_entry(emoji, content, timestamp):
        dlg = ft.AlertDialog(
            title=ft.Text(f"📘 {emoji} — {timestamp}"),
            content=ft.Column([ft.Text(content, size=16)], spacing=10),
            actions=[ft.TextButton("Close", on_click=lambda e: page.close(dlg))],
        )
        page.dialog = dlg
        page.open(dlg)

    def load_mood_cards():
        mood_cards_column.controls.clear()
        for emoji, timestamp, content in get_saved_moods(user_id):
            emoji_file = emoji.lower() + ".png"
            card = ft.CupertinoContextMenu(
                enable_haptic_feedback=True,
                content=ft.Image(src=f"Assets/{emoji_file}", width=48, height=48),
                actions=[ft.CupertinoContextMenuAction(
                    text="View Journal",
                    trailing_icon=ft.Icons.BOOK,
                    on_click=lambda e, c=content, t=timestamp, emo=emoji: show_journal_entry(emo, c, t)
                )]
            )
            date_label = timestamp.split(",")[0] if isinstance(timestamp, str) else timestamp.strftime("%B %d")
            mood_item = ft.Container(
                content=ft.Column([card, ft.Text(date_label, size=12, italic=True)], spacing=4,
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                col={"xs": 4, "sm": 3, "md": 2}
            )
            mood_cards_column.controls.append(mood_item)
        page.update()

    def open_date_picker():
        dp = ft.DatePicker(
            first_date=first_day,
            last_date=last_day,
            value=now,
            on_change=handle_date_change,
            on_dismiss=lambda e: None,
        )
        page.overlay.append(dp)
        dp.open = True
        page.update()

    def handle_date_change(e: ft.ControlEvent):
        picked = e.control.value
        chosen_date.value = picked.strftime("%B %d, %Y")
        open_journal_prompt()

    def open_journal_prompt():
        save_btn = ft.TextButton("Save", disabled=True)

        def on_text_change(e):
            save_btn.disabled = not bool(journal_input.value.strip())
            page.update()

        journal_input.on_change = on_text_change
        dlg = ft.AlertDialog(
            title=ft.Text("Final Step!"),
            content=ft.Column([
                ft.Row([
                    ft.Image(src=f"Assets/{selected_emoji['file']}", width=40, height=40),
                    ft.Text(selected_emoji["label"], size=16),
                    ft.Text(chosen_date.value, size=14, italic=True),
                ], spacing=10),
                journal_input
            ]),
            actions=[save_btn],
            on_dismiss=lambda e: None
        )

        save_btn.on_click = lambda e: save_journal(dlg)
        page.dialog = dlg
        page.open(dlg)

    def save_journal(dialog):
        emoji_label = selected_emoji["label"]
        entry_date = chosen_date.value
        content = journal_input.value.strip()

        with sqlite3.connect("reazure.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO moods (user_id, emoji, intensity, timestamp) VALUES (?, ?, ?, ?)",
                      (user_id, emoji_label, None, entry_date))
            mood_id = c.lastrowid
            c.execute("INSERT INTO journals (user_id, mood_id, content, timestamp) VALUES (?, ?, ?, ?)",
                      (user_id, mood_id, content, entry_date))
            conn.commit()

        result_view.value = f"{emoji_label} – Entry saved!"
        journal_input.value = ""
        chosen_date.value = ""
        page.close(dialog)
        page.snack_bar = ft.SnackBar(ft.Text("✅ Entry saved"))
        page.snack_bar.open = True
        load_mood_cards()
        page.update()

    emoji_row = ft.Row(visible=False, spacing=15, alignment=ft.MainAxisAlignment.CENTER)
    emojis = [
        ("sad.png", "Sad"), ("ecstatic.png", "Ecstatic"), ("excited.png", "Excited"),
        ("bored.png", "Bored"), ("tired.png", "Tired"), ("happy.png", "Happy"),
        ("calm.png", "Calm"), ("stressed.png", "Stressed"), ("worried.png", "Worried")
    ]

    def on_emoji_click(e, file, label):
        selected_emoji["file"] = file
        selected_emoji["label"] = label
        emoji_row.visible = False
        keyword = MOOD_KEYWORDS.get(label)
        update_quote(keyword)
        page.update()
        open_date_picker()

    for file, label in emojis:
        emoji_row.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Image(src=f"Assets/{file}", width=48, height=48),
                    ft.Text(label, size=12, text_align=ft.TextAlign.CENTER),
                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=8,
                border_radius=8,
                bgcolor=ft.Colors.BLUE_50,
                on_click=lambda e, f=file, l=label: on_emoji_click(e, f, l)
            )
        )

    def toggle_emojis(e):
        emoji_row.visible = not emoji_row.visible
        page.update()

    logout_menu = ft.PopupMenuButton(
        items=[ft.PopupMenuItem(text="Logout", on_click=lambda e: page.go("/"))]
    )

    more_btn.on_click = lambda e: update_quote(MOOD_KEYWORDS.get(selected_emoji["label"], None))
    load_mood_cards()

    return ft.View(
        "/dashboard",
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[logout_menu]),
            ft.Row([
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src="Assets/ReAzure.png", width=200, height=200),
                        ft.Text(f"Welcome, {username}!", size=24, weight="bold"),
                        ft.Text(today_str, size=16, italic=True),
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.ADD, size=32),
                            on_click=toggle_emojis,
                            padding=10,
                            border_radius=ft.border_radius.all(12),
                            bgcolor=ft.Colors.BLUE_100,
                        ),
                        ft.Text("Add your Mood", size=14, italic=True),
                        emoji_row,
                        result_view,
                        ft.Divider(),

                        ft.Text("🕒 Mood History", size=18, weight="bold"),
                        mood_cards_column,

                        ft.Row([
                            ft.ElevatedButton("🔁 Refresh Mood History", on_click=lambda _: load_mood_cards()),
                            ft.ElevatedButton("📈 View My Mood Trends", on_click=lambda _: page.go("/analytics")),
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("☁ Azure Wall", size=16, weight="bold"),
                        quote_text,
                        quote_keyword_label,
                        more_btn
                    ], spacing=10),
                    padding=15,
                    border_radius=12,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    margin=ft.margin.only(left=20),
                    width=300
                )
            ])
        ],
        padding=20,
        scroll=ft.ScrollMode.AUTO
    )
