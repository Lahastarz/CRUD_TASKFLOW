# Let's build auth/service.py — this is where register, login, refresh, and logout logic actually lives, using everything you've already built.

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token
from app.core.security import decode_token, TokenType
from app.cache.redis_client import revoke_refresh_token
import jwt

async def get_user_by_email(db: AsyncSession, email:str) -> User|None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# Now I will do the Register_user function
async def register_user(db: AsyncSession, email:str, password:str) -> User:
    existing_user = await get_user_by_email(db, email)
    if existing_user is not None:
        raise ValueError("A user with this E-Mail ID already exists")
    hashed = hash_password(password)
    new_user = User(email=email, hashed_password = hashed)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
async def login_user(db: AsyncSession, email:str, password:str)->dict:
    user = await get_user_by_email(db, email)
    if user is None:
        # Means that user does not exist
        raise ValueError("Invalid Email or password")
    
    if not verify_password(user.hashed_password, password):
        raise ValueError("Invalid Email or password")
    
    access_token = create_access_token(str(user.id))
    refresh_token = await create_refresh_token(str(user.id))

    return {"access_token": access_token, "refresh_token": refresh_token}

async def logout_user(refresh_token:str)-> None:
    try:
        payload = decode_token(refresh_token,expected_type=TokenType.REFRESH)
        jti = payload["jti"]
        await revoke_refresh_token(jti)
    except jwt.PyJWTError:
        pass