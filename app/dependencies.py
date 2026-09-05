from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_user_id_from_token, TokenType
from app.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    user_id = get_user_id_from_token(token, TokenType.ACCESS)
    if(user_id is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could Not Validate the Credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
    user = await db.get(User, user_id)
    if(user is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    return user