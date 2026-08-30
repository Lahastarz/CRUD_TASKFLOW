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

def get_user_id_from_token(token: str, expected_type: TokenType) -> str | None:
    try:
        payload = decode_token(token, expected_type)
        return payload["sub"]
    except jwt.PyJWTError:
        return None

