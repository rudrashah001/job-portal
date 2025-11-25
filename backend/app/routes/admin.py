from fastapi import APIRouter, Depends
from app.utils import require_role

router = APIRouter()


@router.get("/stats")
async def admin_stats(current_user=Depends(require_role("admin"))):
    return {"status": "admin access", "user_id": str(current_user["_id"])}


@router.get("/users")
async def list_users(current_user=Depends(require_role("admin"))):
    return {"count": 0, "users": []}

