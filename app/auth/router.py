from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.auth.schemas import RegisterRequest, TokenResponse
from app.auth import service

from app.auth.schemas import LoginRequest

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


