import json
import logging

import redis
from django.conf import settings

logger = logging.getLogger("telegrambot")


def get_redis():
    return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


def push_command(data: dict):
    """
    Celery → Redis
    """
    r = get_redis()
    logger.info(f"🔥 push_command CALLED: {data}")
    r.lpush("telegram:out", json.dumps(data))
    logger.info("🔥 push_command DONE")
