import asyncio
from app.db.session import AsyncSessionLocal
from app.auth.service import login_user, logout_user
from app.cache.redis_client import is_refresh_token_valid
from app.core.security import decode_token, TokenType
from app.tasks import models as tasks_models  # noqa: F401

async def main():
    async with AsyncSessionLocal() as db:
        tokens = await login_user(db, "arnab@example.com", "MyDog123!")

    refresh_token = tokens["refresh_token"]
    payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
    jti = payload["jti"]

    print("Is valid right after login?", await is_refresh_token_valid(jti))

    await logout_user(refresh_token)

    print("Is valid after logout?", await is_refresh_token_valid(jti))

asyncio.run(main())