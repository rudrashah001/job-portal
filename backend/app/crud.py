# app/crud.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional, Dict

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["jobportal"]

users_col = db["users"]
jobs_col = db["jobs"]
applications_col = db["applications"]


def _id_to_str(doc: dict) -> dict:
    """Convert _id to id string and remove _id for responses."""
    if not doc:
        return doc
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc


async def create_user(doc: Dict) -> str:
    res = await users_col.insert_one(doc)
    return str(res.inserted_id)


async def find_user_by_email(email: str) -> Optional[dict]:
    return await users_col.find_one({"email": email})


async def find_user_by_id(uid: str) -> Optional[dict]:
    return await users_col.find_one({"_id": ObjectId(uid)})


async def create_job(doc: Dict) -> str:
    doc["posted_at"] = doc.get("posted_at")
    doc["applicants"] = []
    res = await jobs_col.insert_one(doc)
    return str(res.inserted_id)


async def get_jobs(filter: dict = None, limit: int = 100) -> List[dict]:
    cursor = jobs_col.find(filter or {}).limit(limit)
    results = []
    async for doc in cursor:
        results.append(_id_to_str(doc))
    return results


async def get_job_by_id(jid: str) -> Optional[dict]:
    doc = await jobs_col.find_one({"_id": ObjectId(jid)})
    return _id_to_str(doc) if doc else None


async def add_applicant(job_id: str, student_id: str) -> bool:
    res = await jobs_col.update_one(
        {"_id": ObjectId(job_id)},
        {"$addToSet": {"applicants": student_id}}
    )
    return res.modified_count > 0


async def create_application(doc: dict) -> str:
    doc["applied_at"] = doc.get("applied_at")
    doc["status"] = doc.get("status", "applied")
    res = await applications_col.insert_one(doc)
    return str(res.inserted_id)


async def get_applications_for_job(job_id: str) -> List[dict]:
    cursor = applications_col.find({"job_id": job_id})
    results = []
    async for doc in cursor:
        results.append(_id_to_str(doc))
    return results


async def init_text_index():
    # create text index for job searching on title and description
    await jobs_col.create_index([("title", "text"), ("description", "text")])
