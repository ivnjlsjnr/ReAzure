import sqlite3
import requests
from datetime import datetime

def get_username(user_id: int) -> str:
    with sqlite3.connect("reazure.db") as conn:
        row = conn.execute("SELECT username FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return row[0] if row else "Guest"

def get_saved_moods(user_id: int):
    with sqlite3.connect("reazure.db") as conn:
        return conn.execute("""
            SELECT moods.mood_id, moods.emoji, moods.timestamp, journals.content
            FROM moods
            JOIN journals ON moods.mood_id = journals.mood_id
            WHERE moods.user_id = ?
            ORDER BY date(moods.timestamp) DESC
        """, (user_id,)).fetchall()

def save_journal_entry(user_id: int, emoji_label: str, content: str, entry_date: str):
    with sqlite3.connect("reazure.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO moods (user_id, emoji, intensity, timestamp) VALUES (?, ?, ?, ?)",
                  (user_id, emoji_label, None, entry_date))
        mood_id = c.lastrowid
        c.execute("INSERT INTO journals (user_id, mood_id, content, timestamp) VALUES (?, ?, ?, ?)",
                  (user_id, mood_id, content, entry_date))
        conn.commit()

def delete_mood_entry(mood_id: int):
    with sqlite3.connect("reazure.db") as conn:
        conn.execute("DELETE FROM journals WHERE mood_id = ?", (mood_id,))
        conn.execute("DELETE FROM moods WHERE mood_id = ?", (mood_id,))
        conn.commit()

def analyze_recent_moods(user_id: int) -> tuple[str, str]:
    with sqlite3.connect("reazure.db") as conn:
        moods = conn.execute("""
            SELECT emoji FROM moods
            WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT 5
        """, (user_id,)).fetchall()

    recent_moods = [m[0] for m in moods]
    if not recent_moods:
        return "No mood data yet", ""

    positive = {"Ecstatic", "Excited", "Happy", "Calm"}
    negative = {"Sad", "Stressed", "Worried", "Tired", "Bored"}

    pos_count = sum(1 for mood in recent_moods if mood in positive)
    neg_count = sum(1 for mood in recent_moods if mood in negative)
    total = len(recent_moods)

    if pos_count / total >= 0.8:
        return "🌤 High", "Keep it up! Your recent mood logs show strong positivity."
    elif neg_count / total >= 0.8:
        return "🌧 Low", "Try to take breaks or talk to someone — things seem a bit heavy lately."
    else:
        return "⛅ Balanced", "You're showing a healthy mix of moods. Keep observing your feelings regularly!"

def get_quote(keyword=None):
    try:
        response = requests.get("https://zenquotes.io/api/quotes", timeout=5)
        data = response.json()
        if isinstance(data, list) and data:
            if keyword:
                for quote in data:
                    if keyword.lower() in quote["q"].lower():
                        return f'"{quote["q"]}" — {quote["a"]}', "ZenQuotes"
                return f'"{data[0]["q"]}" — {data[0]["a"]}', "ZenQuotes"
            return f'"{data[0]["q"]}" — {data[0]["a"]}', "ZenQuotes"
    except Exception as e:
        print("[QUOTE ERROR]", e)
    return "✨ Couldn't fetch quote. Try again!", "none"

