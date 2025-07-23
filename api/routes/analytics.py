from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_analytics():
    return {"analytics": "📊 Analytics endpoint working!"}
