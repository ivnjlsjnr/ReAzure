from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from api.database import get_db

router = APIRouter()

class MoodEntry(BaseModel):
    user_id: int
    emoji: str
    intensity: int | None = None
    content: str
    timestamp: str | None = None  # Optional

@router.post("/")
def save_mood(entry: MoodEntry):
    db = get_db()
    cursor = db.cursor()

    timestamp = entry.timestamp or datetime.now().strftime("%B %d, %Y, %H:%M:%S")

    try:
        # Insert into moods table
        cursor.execute("""
            INSERT INTO moods (user_id, emoji, intensity, timestamp)
            VALUES (?, ?, ?, ?)
        """, (entry.user_id, entry.emoji, entry.intensity, timestamp))
        mood_id = cursor.lastrowid

        # Insert into journals table
        cursor.execute("""
            INSERT INTO journals (user_id, mood_id, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (entry.user_id, mood_id, entry.content, timestamp))

        db.commit()
        return {"message": "Mood and journal entry saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save mood: {str(e)}")
@router.get("/{user_id}")
def get_user_moods(user_id: int):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT moods.emoji, journals.content, moods.timestamp
            FROM moods
            JOIN journals ON moods.mood_id = journals.mood_id
            WHERE moods.user_id = ?
            ORDER BY moods.timestamp DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        result = [
            {"emoji": row[0], "content": row[1], "timestamp": row[2]}
            for row in rows
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch moods: {str(e)}")
