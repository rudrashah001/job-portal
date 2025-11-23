# app/routes/recruiters.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import UserRegister, UserLogin, TokenResponse, UserOut
from app.crud import create_user, find_user_by_email, find_user_by_id
from app.auth import get_password_hash, verify_password, create_access_token
from app.utils import get_current_user, require_role
from datetime import datetime

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegister):
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
async def login(payload: UserLogin):
    user = await find_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    uid = str(user["_id"])
    token = create_access_token({"sub": uid, "role": user.get("role", "recruiter")})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)):
    return current_user


# Example protected route for recruiters to view their posted jobs (requires role recruiter)
@router.get("/my-posts")
async def my_posts(current_user=Depends(require_role("recruiter"))):
    from app.crud import jobs_col
    posts = []
    cursor = jobs_col.find({"posted_by": str(current_user["_id"])})
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        posts.append(doc)
    return {"count": len(posts), "posts": posts}
