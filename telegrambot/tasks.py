import asyncio
import logging

from aiogram import types
from celery import shared_task

from .bot import bot
from .dispatcher import dp
from .redis_queue import push_command

logger = logging.getLogger("celery")
logger_tg = logging.getLogger("telegrambot")


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
    logger_tg.info("Start process_update_task")
    update = types.Update.to_python(update_dict)
    asyncio.run(dp.feed_update(bot, update))
    logger_tg.info(f"🚀 запущен dp.feed_update with: {update}")
