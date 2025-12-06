import datetime

import pytest

from aiogram.types import Update, Message, User, Chat
from django.utils import timezone

from telegrambot.handlers.basic import router as basic_router


@pytest.mark.asyncio
async def test_start(dp, bot, fake_sender, user, monkeypatch):
    dp.include_router(basic_router)

    update = Update(
        update_id=11,
        message=Message(
            message_id=101,
            date=timezone.now(),
            chat=Chat(id=500, type="private"),
            from_user=User(
                id=500,
                is_bot=False,
                first_name="Tester"
            ),
            text="/start",
        )
    )

    await dp.feed_update(bot, update)

    fake_sender.send.assert_awaited_once()
    args, kwargs = fake_sender.send.await_args
    assert "start" in args[1].lower() or "привет" in args[1].lower()
