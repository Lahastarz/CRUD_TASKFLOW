from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.auth.schemas import RegisterRequest, TokenResponse
from app.auth import service

from app.auth.schemas import LoginRequest, RegisterRequest, RefreshRequest
import jwt
router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await service.register_user(db, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"id":str(user.id), "email":user.email}


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        tokens = await service.login_user(db, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    from app.core.security import refresh_access_token
    try:
        tokens = await refresh_access_token(body.refresh_token)
    except (ValueError, jwt.PyJWTError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    return tokens

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshRequest):
    await service.logout_user(body.refresh_token)