import flet as ft
from datetime import datetime, timedelta
from controllers.dashboard_controller import (
    fetch_quote_by_mood,
    fetch_recommendations,
    get_recent_rating_feedback
)
from models.dashboard_model import (
    get_username,
    get_saved_moods,
    save_journal_entry,
    delete_mood_entry
)

def DashboardPage(page: ft.Page, user_id: int):
    username = get_username(user_id)
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    selected_emoji = {"file": "", "label": ""}
    chosen_date = ft.Text("")
    journal_input = ft.TextField(label="Describe your day", multiline=True, min_lines=3, width=300)
    result_view = ft.Text("")
    mood_cards_column = ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER)

    quote_text = ft.Text("Choose your mood to get inspired...", italic=True, color=ft.Colors.BLUE_400, size=14)
    quote_keyword_label = ft.Text("", size=12, italic=True, color=ft.Colors.BLUE_100)
    gemini_text = ft.Text("", size=13, color=ft.Colors.BLUE_800, italic=True)
    more_btn = ft.TextButton("More", visible=False)
    azure_rating = ft.Text(size=15, weight="bold", color=ft.Colors.BLUE_800)
    azure_feedback = ft.Text(size=12, italic=True, color=ft.Colors.BLUE_500)

    recommendation_column = ft.Column(spacing=5)

    def update_quote(mood_label=None):
        quote, source, keyword = fetch_quote_by_mood(mood_label)
        quote_text.value = quote
        quote_keyword_label.value = f"(source: {source}, keyword: {keyword})"

        rating, feedback = get_recent_rating_feedback(user_id)
        azure_rating.value = f"🔷 Azure Rating: {rating}"
        azure_feedback.value = feedback

        more_btn.visible = True
        page.update()

    def update_recommendations(mood_label):
        tips = fetch_recommendations(mood_label)
        recommendation_column.controls = [ft.Text("💡 Suggestions:", size=13, weight="bold", color=ft.Colors.BLUE_800)]
        recommendation_column.controls += [ft.Text(f"• {tip}", size=12) for tip in tips]
        page.update()

    def delete_mood(mood_id: int):
        delete_mood_entry(mood_id)
        page.snack_bar = ft.SnackBar(ft.Text("🗑 Mood entry deleted."))
        page.snack_bar.open = True
        load_mood_cards()
        page.update()

    def confirm_delete(mood_id: int):
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirm Delete"),
            content=ft.Text("Are you sure you want to delete this mood entry?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close_dialog()),
                ft.TextButton("Delete", on_click=lambda e: (delete_mood(mood_id), page.close_dialog()))
            ],
        )
        page.dialog = dialog
        page.open(dialog)

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
        previous_month = ""
        for mood_id, emoji, timestamp, content in get_saved_moods(user_id):
            emoji_file = emoji.lower() + ".png"
            try:
                parsed_date = datetime.strptime(timestamp, "%Y-%m-%d")
            except:
                parsed_date = datetime.strptime(timestamp, "%B %d, %Y")
            date_label = parsed_date.strftime("%b %d, %Y")
            current_month = parsed_date.strftime("%B %Y")

            if current_month != previous_month:
                mood_cards_column.controls.append(ft.Text(f"🗓 {current_month}", size=14, weight="bold", color=ft.Colors.BLUE_900))
                previous_month = current_month

            card = ft.CupertinoContextMenu(
                enable_haptic_feedback=True,
                content=ft.Image(src=f"Assets/{emoji_file}", width=48, height=48),
                actions=[
                    ft.CupertinoContextMenuAction(
                        text="View Journal",
                        trailing_icon=ft.Icons.BOOK,
                        on_click=lambda e, c=content, t=timestamp, emo=emoji: show_journal_entry(emo, c, t)
                    ),
                    ft.CupertinoContextMenuAction(
                        text="Delete Mood",
                        trailing_icon=ft.Icons.DELETE,
                        is_destructive_action=True,
                        on_click=lambda e, mid=mood_id: confirm_delete(mid)
                    )
                ]
            )

            mood_item = ft.Container(
                content=ft.Column([
                    card,
                    ft.Text(date_label, size=12, italic=True)
                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                col={"xs": 4, "sm": 3, "md": 2}
            )
            mood_cards_column.controls.append(mood_item)
        page.update()

    def open_date_picker():
        dp = ft.DatePicker(
            first_date=datetime(2025, 1, 1),
            last_date=datetime(2030, 12, 31),
            value=datetime.now(),
            on_change=handle_date_change
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
        )

        def save(e):
            entry_date = datetime.strptime(chosen_date.value, "%B %d, %Y").strftime("%Y-%m-%d")
            save_journal_entry(user_id, selected_emoji["label"], journal_input.value.strip(), entry_date)
            journal_input.value = ""
            chosen_date.value = ""
            result_view.value = f"{selected_emoji['label']} – Entry saved!"
            page.close(dlg)
            page.snack_bar = ft.SnackBar(ft.Text("✅ Entry saved"))
            page.snack_bar.open = True
            load_mood_cards()
            page.update()

        save_btn.on_click = save
        page.dialog = dlg
        page.open(dlg)

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
        update_quote(label)
        update_recommendations(label)
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

    more_btn.on_click = lambda e: update_quote(selected_emoji["label"])
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
                        more_btn,
                        azure_rating,
                        azure_feedback,
                        ft.Divider(),
                        ft.Text("🎯 Personalized Tips", size=15, weight="bold", color=ft.Colors.BLUE_900),
                        recommendation_column,
                        gemini_text
                    ], spacing=10),
                    padding=15,
                    border_radius=12,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    margin=ft.margin.only(left=20),
                    width=320
                )
            ])
        ],
        padding=20,
        scroll=ft.ScrollMode.AUTO
    )
