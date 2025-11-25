import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional, Dict

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["AuthDB"]

users_col = db["users"]
jobs_col = db["jobs"]
applications_col = db["applications"]


def _id_to_str(doc: dict) -> dict:
    """Convert _id to id string."""
    if not doc:
        return doc
    doc["id"] = str(doc["_id"])
    return doc


async def create_user(doc: Dict) -> str:
    res = await users_col.insert_one(doc)
    return str(res.inserted_id)


async def find_user_by_email(email: str) -> Optional[dict]:
    return await users_col.find_one({"email": email})


async def find_user_by_id(uid: str) -> Optional[dict]:
    try:
        return await users_col.find_one({"_id": ObjectId(uid)})
    except:
        return None


async def create_job(doc: Dict) -> str:
    doc["applicants"] = doc.get("applicants", [])
    res = await jobs_col.insert_one(doc)
    return str(res.inserted_id)


async def get_jobs(filter: dict = None, limit: int = 100) -> List[dict]:
    try:
        query_filter = filter or {}
        cursor = jobs_col.find(query_filter).limit(limit)
        results = []
        async for doc in cursor:
            results.append(_id_to_str(doc))
        return results
    except Exception as e:
        print(f"Error in get_jobs: {e}")
        raise


async def get_job_by_id(jid: str) -> Optional[dict]:
    try:
        doc = await jobs_col.find_one({"_id": ObjectId(jid)})
        return _id_to_str(doc) if doc else None
    except:
        return None


async def add_applicant(job_id: str, student_id: str) -> bool:
    try:
        res = await jobs_col.update_one(
            {"_id": ObjectId(job_id)},
            {"$addToSet": {"applicants": student_id}}
        )
        return res.modified_count > 0
    except:
        return False


async def create_application(doc: dict) -> str:
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
    try:
        await jobs_col.create_index([("title", "text"), ("description", "text")])
    except:
        pass

