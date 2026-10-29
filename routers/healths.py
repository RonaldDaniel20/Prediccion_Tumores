from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health check"]
)

@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "API is healthy"
    }