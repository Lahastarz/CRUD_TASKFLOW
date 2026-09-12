import redis.asyncio as redis
from app.core.config import settings
import asyncio
from app.core.logging import logger
redis_client = redis.from_url(str(settings.REDIS_URL), decode_responses = True)

async def store_refresh_token(jti: str, user_id:str)-> None:
    key = f"refresh:{jti}"
    ttl_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS*86400
    await redis_client.set(key, user_id, ex=ttl_seconds)

async def is_refresh_token_valid(jti:str) -> bool:
    key = f"refresh:{jti}"
    value = await redis_client.get(key)

    return bool(value)

async def revoke_refresh_token(jti:str, user_id:str, reason:str) -> bool:
    key = f"refresh:{jti}"
    deleted_count = await redis_client.delete(key)
    # After deletion value will be empty hecne it will return empty

    logger.info(
        "refresh_token_revoked",
        user_id=user_id,
        jti = jti,
        reason=reason
    )
    return deleted_count>0