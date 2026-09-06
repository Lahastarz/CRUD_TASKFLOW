from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.auth.schemas import RegisterRequest, TokenResponse
from app.auth import service

router = APIRouter(prefix="/auth", tags=["auth"])
