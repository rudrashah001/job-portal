# app/utils.py
from fastapi import Depends, HTTPException, status
from app.auth import require_token
from app.crud import find_user_by_id
from typing import Optional


async def get_current_user(token_payload: dict = Depends(require_token)):
    """
    token_payload expected to have {'sub': user_id, 'role': role, ...}
    """
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = await find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # normalize id to string
    user["id"] = str(user["_id"])
    user.pop("_id", None)
    return user


def require_role(role: str):
    async def inner(current_user=Depends(get_current_user)):
        if current_user.get("role") != role and current_user.get("role") != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return inner
