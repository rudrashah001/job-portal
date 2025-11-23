# app/routes/jobs.py
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas import JobCreate, JobOut, ApplicationCreate
from app.crud import create_job, get_jobs, get_job_by_id, add_applicant, create_application, get_applications_for_job
from app.utils import get_current_user, require_role
from datetime import datetime

router = APIRouter()


@router.post("/post")
async def post_job(payload: JobCreate, current_user=Depends(require_role("recruiter"))):
    job_doc = payload.dict()
    job_doc["posted_by"] = str(current_user["_id"])
    job_doc["posted_at"] = datetime.utcnow()
    jid = await create_job(job_doc)
    return {"job_id": jid}


@router.get("/search")
async def search_jobs(q: str = Query(None, description="search query"), limit: int = 50):
    filter_q = {}
    if q:
        filter_q = {"$text": {"$search": q}}
    results = await get_jobs(filter_q, limit=limit)
    return {"count": len(results), "results": results}


@router.get("/{job_id}")
async def job_details(job_id: str):
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.post("/{job_id}/apply")
async def apply_job(job_id: str, current_user=Depends(get_current_user)):
    # student applying to job; current_user must be student (role check)
    if current_user.get("role") != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students may apply")
    # create application and add applicant to job
    app_doc = {
        "job_id": job_id,
        "student_id": str(current_user["_id"]),
        "resume_snapshot": current_user.get("profile", {}).get("resume_url"),
        "applied_at": datetime.utcnow(),
        "status": "applied"
    }
    aid = await create_application(app_doc)
    await add_applicant(job_id, str(current_user["_id"]))
    return {"application_id": aid}


@router.get("/{job_id}/applicants")
async def job_applicants(job_id: str, current_user=Depends(require_role("recruiter"))):
    # only the recruiter who posted the job or admin can view applicants
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    # allow only poster or admin
    poster_id = job.get("posted_by")
    user_id = str(current_user["_id"])
    if user_id != poster_id and current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to view applicants")
    apps = await get_applications_for_job(job_id)
    return {"count": len(apps), "applications": apps}
