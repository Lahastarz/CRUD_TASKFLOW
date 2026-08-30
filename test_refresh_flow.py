import asyncio
from app.core.security import create_refresh_token, decode_token, TokenType
from app.cache.redis_client import is_refresh_token_valid, revoke_refresh_token

async def main():
    token = await create_refresh_token("user-42")
    print("Refresh token created:", token[:40], "...")

    payload = decode_token(token, expected_type=TokenType.REFRESH)
    jti = payload["jti"]
    print("Extracted jti:", jti)

    valid = await is_refresh_token_valid(jti)
    print("Is valid in Redis right after creation?", valid)

    await revoke_refresh_token(jti)
    valid_after_revoke = await is_refresh_token_valid(jti)
    print("Is valid after revoke?", valid_after_revoke)

asyncio.run(main())