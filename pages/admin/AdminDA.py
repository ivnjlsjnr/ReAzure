import sqlite3

def get_all_users():
    conn = sqlite3.connect("reazure.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, email, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_mood_stats(user_id: int):
    conn = sqlite3.connect("reazure.db")
    cursor = conn.cursor()

    # Get total mood entries
    cursor.execute("SELECT COUNT(*) FROM moods WHERE user_id = ?", (user_id,))
    entry_count = cursor.fetchone()[0]

    # Get top mood
    cursor.execute("""
        SELECT emoji, COUNT(*) as count
        FROM moods
        WHERE user_id = ?
        GROUP BY emoji
        ORDER BY count DESC
        LIMIT 1
    """, (user_id,))
    top_mood_row = cursor.fetchone()
    top_mood = top_mood_row[0] if top_mood_row else None

    conn.close()
    return {"top_mood": top_mood, "entry_count": entry_count}
