from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserRegister, UserLogin, TokenResponse
from app.crud import create_user, find_user_by_email
from app.auth import get_password_hash, verify_password, create_access_token
from app.utils import get_current_user, require_role
from datetime import datetime

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def recruiter_register(payload: UserRegister):
    existing = await find_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "role": "recruiter",
        "hashed_password": get_password_hash(payload.password),
        "profile": {},
        "created_at": datetime.utcnow()
    }
    uid = await create_user(user_doc)
    token = create_access_token({"sub": uid, "role": "recruiter"})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def recruiter_login(payload: UserLogin):
    user = await find_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a recruiter")
    uid = str(user["_id"])
    token = create_access_token({"sub": uid, "role": "recruiter"})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/dashboard")
async def recruiter_dashboard(current_user=Depends(require_role("recruiter"))):
    return {"recruiter_id": str(current_user["_id"])}
