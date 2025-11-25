from fastapi import Depends, HTTPException, status
from app.auth import require_token, decode_token


async def get_current_user(token: str = Depends(require_token)) -> dict:
    """Get the current authenticated user from token."""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No user_id in token")
    return {"_id": user_id, "role": payload.get("role", "user")}


def require_role(required_role: str):
    """Dependency to require a specific role."""
    async def role_checker(current_user=Depends(get_current_user)):
        user_role = current_user.get("role", "user")
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires '{required_role}' role"
            )
        return current_user
    return role_checker
