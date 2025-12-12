import json
import logging

import redis
from celery import shared_task
from django.conf import settings

from .redis_queue import push_command

logger = logging.getLogger("celery")

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)


@shared_task
def send_telegram_message(chat_id: int, text: str, keyboard_dict=None):
    """
    Celery → Redis → Aiogram
    """
    push_command(
        {
            "cmd": "send_message",
            "chat_id": chat_id,
            "text": text,
            "keyboard": keyboard_dict,
        }
    )


@shared_task
def process_update_task(update_dict):
    r.lpush("telegram:in", json.dumps(update_dict))
