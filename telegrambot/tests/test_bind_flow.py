from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.types import Update, Message, User, Chat
from asgiref.sync import sync_to_async
from django.utils import timezone

from telegrambot.handlers.bind import router as bind_router
from aiogram import Dispatcher

from telegrambot.tests.factory import ProfileFactory
from users.tests.factory import UserFactory

dp = Dispatcher()
dp.include_router(bind_router)

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_bind_flow(bot, monkeypatch):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)

    fake_response = SimpleNamespace(status_code=200)
    monkeypatch.setattr(
        "telegrambot.handlers.bind.requests.post",  # путь к МЕСТУ, где ты делаешь requests.post
        lambda *a, **k: fake_response,
    )

    answer_mock = AsyncMock()
    monkeypatch.setattr(Message, "answer", answer_mock)

    update = Update(
        update_id=77,
        message=Message(
            message_id=1,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester", username="Tester"),
            text="bind758"
        ),
    )

    await dp.feed_update(bot, update)

    # 5) Проверяем, что answer вызывался
    assert answer_mock.await_count >= 1
    # Берём последний вызов
    call = answer_mock.await_args
    text = call.args[0]

    assert "успешно" in text.lower()


@pytest.mark.asyncio
async def test_bind_cmd(bot, fake_bind_sender, user, monkeypatch):

    update = Update(
        update_id=88,
        message=Message(
            message_id=808,
            date=timezone.now(),
            chat=Chat(id=800, type="private"),
            from_user=User(
                id=800,
                is_bot=False,
                first_name="Tester"
            ),
            text="/bind",
        )
    )

    await dp.feed_update(bot, update)

    fake_bind_sender.send.assert_awaited_once()
    args, kwargs = fake_bind_sender.send.await_args
    assert "Привязка Telegram" in args[1]


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_unbind_handler(bot, monkeypatch):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)

    answer_mock = AsyncMock()
    monkeypatch.setattr(Message, "answer", answer_mock)

    update = Update(
        update_id=99,
        message=Message(
            message_id=9,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester", username="Tester"),
            text="/unbind"
        ),
    )

    await dp.feed_update(bot, update)

    assert answer_mock.await_count >= 1
    call = answer_mock.await_args
    text = call.args[0]

    assert "Telegram был успешно отвязан" in text
