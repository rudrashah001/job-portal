# app/routes/students.py
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends, Form
from app.schemas import UserRegister, UserLogin, TokenResponse, UserOut, StudentProfile
from app.crud import create_user, find_user_by_email, find_user_by_id, init_text_index
from app.auth import get_password_hash, verify_password, create_access_token
from app.utils import get_current_user
from datetime import datetime
import os

router = APIRouter()

# initialize indexes when router is loaded (non-blocking)
# call crud.init_text_index() on startup in production; simplified here
@router.on_event("startup")
async def _startup():
    try:
        await init_text_index()
    except Exception:
        # index creation is optional here
        pass


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegister):
    existing = await find_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "role": "student",
        "hashed_password": get_password_hash(payload.password),
        "profile": {},
        "created_at": datetime.utcnow()
    }
    uid = await create_user(user_doc)
    token = create_access_token({"sub": uid, "role": "student"})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    user = await find_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    uid = str(user["_id"])
    token = create_access_token({"sub": uid, "role": user.get("role", "student")})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)):
    # prepare response user object
    user = current_user.copy()
    user["id"] = str(user["_id"]) if "_id" in user else user.get("id")
    user.pop("_id", None)
    return user


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """
    Simple resume upload: saves to ./uploads/<user_id>_resume_<filename>
    In production, use S3 and store URL in user's profile.
    """
    user_id = str(current_user["_id"]) if "_id" in current_user else current_user.get("id")
    upload_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, f"{user_id}_resume_{file.filename}")
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    # update user's profile with resume URL (local path)
    await find_user_by_id(user_id)  # just ensure user exists
    # for simplicity, update mongo directly here
    from app.crud import users_col
    await users_col.update_one({"_id": current_user["_id"]}, {"$set": {"profile.resume_url": save_path}})
    return {"resume_url": save_path}
