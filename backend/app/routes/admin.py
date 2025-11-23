# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import require_role
from app.crud import users_col, jobs_col
from datetime import datetime

router = APIRouter()


@router.get("/stats")
async def stats(current_user=Depends(require_role("admin"))):
    users_count = await users_col.count_documents({})
    jobs_count = await jobs_col.count_documents({})
    return {"users": users_count, "jobs": jobs_count}


@router.get("/users")
async def list_users(current_user=Depends(require_role("admin"))):
    cursor = users_col.find({})
    out = []
    async for u in cursor:
        u["id"] = str(u["_id"])
        u.pop("_id", None)
        out.append(u)
    return {"count": len(out), "users": out}


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, current_user=Depends(require_role("admin"))):
    res = await jobs_col.delete_one({"_id": job_id})
    # note: job_id must be ObjectId; in production convert and validate
    return {"deleted": True}
