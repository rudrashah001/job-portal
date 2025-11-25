from fastapi import APIRouter, HTTPException, status, Depends, Form
from app.schemas import UserRegister, UserLogin, TokenResponse, UserOut, StudentProfile
from app.crud import create_user, find_user_by_email, find_user_by_id, init_text_index
from app.auth import get_password_hash, verify_password, create_access_token
from app.utils import get_current_user
from datetime import datetime

router = APIRouter()


@router.on_event("startup")
async def _startup():
    try:
        await init_text_index()
    except Exception:
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
    user = await find_user_by_id(current_user["_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user["id"] = str(user["_id"])
    return user


@router.put("/profile")
async def update_profile(profile: StudentProfile, current_user=Depends(get_current_user)):
    return {"status": "updated"}
