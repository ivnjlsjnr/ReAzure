from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import bcrypt

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str
    email: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: UserRegister):
    try:
        conn = sqlite3.connect("reazure.db")
        cursor = conn.cursor()

        # Check for existing username
        cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists.")

        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # Insert user
        cursor.execute(
            "INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
            (user.username, hashed_password.decode('utf-8'), user.email, datetime.now().isoformat())
        )
        conn.commit()
        return {"message": "Registration successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        conn.close()

@router.post("/login")
def login_user(credentials: UserLogin):
    try:
        conn = sqlite3.connect("reazure.db")
        cursor = conn.cursor()

        # Fetch user by username
        cursor.execute("SELECT password FROM users WHERE username = ?", (credentials.username,))
        row = cursor.fetchone()

        if row:
            stored_hash = row[0]

            if bcrypt.checkpw(credentials.password.encode('utf-8'), stored_hash.encode('utf-8')):
                return {"message": "Login successful!"}
            else:
                raise HTTPException(status_code=401, detail="Invalid password.")
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        conn.close()

@router.get("/get-id")
def get_user_id(username: str):
    try:
        conn = sqlite3.connect("reazure.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return {"user_id": row[0]}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
