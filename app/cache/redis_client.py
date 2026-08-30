import redis.asyncio as redis
from app.core.config import settings
import asyncio
redis_client = redis.from_url(str(settings.REDIS_URL), decode_responses = True)

async def store_refresh_token(jti: str, user_id:str)-> None:
    key = f"refresh:{jti}"
    ttl_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS*86400
    await redis_client.set(key, user_id, ex=ttl_seconds)

async def is_refresh_token_valid(jti:str) -> bool:
    key = f"refresh:{jti}"
    value = await redis_client.get(key)

    return bool(value)

async def revoke_refresh_token(jti:str) -> bool:
    key = f"refresh:{jti}"
    deleted_count = await redis_client.delete(key)
    # After deletion value will be empty hecne it will return empty
    return deleted_count>0


# testing phase
async def test_flow():
    test_jti = "test-jti-123"
    test_user_id = "user-42"

    await store_refresh_token(test_jti, test_user_id)
    print("After storing, is valid?", await is_refresh_token_valid(test_jti))

    revoked = await revoke_refresh_token(test_jti)
    print("Was Something revoked? ", revoked)

    print("After revoking, is valid?", await is_refresh_token_valid(test_jti))

if __name__ == "__main__":
    asyncio.run(test_flow())