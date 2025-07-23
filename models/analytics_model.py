# models/analytics_model.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
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

def generate_mood_chart_base64(df: pd.DataFrame) -> str:
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
