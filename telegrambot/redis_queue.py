import json
import logging

import redis
from django.conf import settings

logger = logging.getLogger("telegrambot")


def get_redis():
    if not getattr(settings, "USE_REDIS", True):
        logger.info("⚠️ Redis is disabled — redis_listener will not start")
        return
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )


def push_command(data: dict):
    """
    Celery → Redis
    """
    r = get_redis()
    r.lpush("telegram:out", json.dumps(data))
