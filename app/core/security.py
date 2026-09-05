from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_hasher = PasswordHasher()

def hash_password(plain_password: str)->str:
    return _hasher.hash(plain_password)

def verify_password(hashed_password:str, plain_password:str)->bool:
    try:
        return _hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

from app.core.config import settings
from datetime import timedelta, datetime, UTC
from enum import Enum
import jwt
import uuid
from app.cache.redis_client import store_refresh_token
from app.cache.redis_client import is_refresh_token_valid, revoke_refresh_token
class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def _create_token(subject:str, expires_delta:timedelta, token_type: TokenType, jti: str | None = None)->str:
    now = datetime.now(UTC)
    payload = {
        "sub":subject,
        "iat": now, 
        "exp": now + expires_delta,
        "type": token_type.value,
    }
    if jti is not None:
        payload['jti'] = jti
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm = settings.JWT_ALGORITHM)

def create_access_token(user_id:str)->str:
    return _create_token(
        subject=user_id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type=TokenType.ACCESS,
    )

async def create_refresh_token(user_id: str)->str:
    jti = str(uuid.uuid4())
    token =  _create_token(
        subject=user_id,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type=TokenType.REFRESH,
        jti = jti
    )
    await store_refresh_token(jti, user_id)
    return token

def decode_token(token: str, expected_type: TokenType) -> dict:
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms = [settings.JWT_ALGORITHM]
    )
    if payload.get("type") != expected_type.value:
        raise jwt.InvalidTokenError(
            f"Expected a {expected_type.value} token, got {payload.get('type')}"
        )
    return payload

async def refresh_access_token(refresh_token:str)-> dict:
    payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
    jti = payload["jti"]
    is_valid = await is_refresh_token_valid(jti)
    if not is_valid:
        raise ValueError("Refresh Token has been Revoked or is now Invalid")
    
    # I will now issue brand new refresh, access token so that rotation can happen
    user_id = payload["sub"]
    await revoke_refresh_token(jti)

    new_access_token = create_access_token(user_id)
    new_refresh_token = await create_refresh_token(user_id)

    return {"access_token":new_access_token, "refresh_token":new_refresh_token}
    

def get_user_id_from_token(token: str, expected_type: TokenType) -> str | None:
    try:
        payload = decode_token(token, expected_type)
        return payload["sub"]
    except jwt.PyJWTError:
        return None

# async def _test():
#     token = await create_refresh_token("user-99")
#     result = await refresh_access_token(token)
#     print("Refresh succeeded, got:", result)

# async def _test_reuse_detection():
#     old_token = await create_refresh_token("user-77")

#     # First refresh -- should succeed, old token gets revoked, new one issued
#     result1 = await refresh_access_token(old_token)
#     print("First refresh (should succeed):", result1)

#     # Try reusing the SAME old token again -- should now fail
#     try:
#         result2 = await refresh_access_token(old_token)
#         print("BUG: second refresh should have failed but didn't:", result2)
#     except ValueError as e:
#         print("Correctly rejected reused token:", e)

# if __name__ == "__main__":
#     import asyncio
#     # asyncio.run(_test())
#     asyncio.run(_test_reuse_detection())