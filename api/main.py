from fastapi import FastAPI
from api.routes import users, moods, analytics

app = FastAPI(title="ReAzure API")

# Route registration
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(moods.router, prefix="/moods", tags=["Moods"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {
        "message": "Welcome to ReAzure API.",
        "docs": "Visit http://127.0.0.1:8000/docs for Swagger UI.",
        "redoc": "Visit http://127.0.0.1:8000/redoc for ReDoc UI."
    }
