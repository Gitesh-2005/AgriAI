from app.core.config import settings
import redis.asyncio as redis

redis_client = redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True
)
