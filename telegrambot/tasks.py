import logging

from celery import shared_task

from .redis_queue import push_command

logger = logging.getLogger("celery")


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
