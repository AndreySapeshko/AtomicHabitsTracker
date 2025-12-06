# tests/telegram/test_callbacks.py
from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from aiogram.types import Update, CallbackQuery, User, Chat, Message
from asgiref.sync import sync_to_async
from django.utils import timezone
from aiogram import Dispatcher

from habit_instances.models import HabitInstanceStatus
from habit_instances.tests.factory import HabitInstanceFactory
from habits.tests.factory import HabitFactory
from telegrambot.handlers.callbacks import router as callback_router
from telegrambot.tests.factory import ProfileFactory
from users.tests.factory import UserFactory

dp = Dispatcher()
dp.include_router(callback_router)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_undo_callback_habit(bot, fake_callback_sender, monkeypatch):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)
    habit = await sync_to_async(HabitFactory)(user=user, action="test callback")
    inst = await sync_to_async(HabitInstanceFactory)(
        habit=habit,
        status=HabitInstanceStatus.COMPLETED,
        confirm_deadline=timezone.now() + timedelta(days=1)
    )

    monkeypatch.setattr(Message, "edit_text", AsyncMock())

    cb = CallbackQuery(
        id="aaa",
        from_user=User(id=user.id, is_bot=False, first_name="Tester"),
        chat_instance="ci",
        message=Message(
            message_id=1,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester"),
            text="test callback"
        ),
        data=f"undo:{inst.id}"
    )

    monkeypatch.setattr(CallbackQuery, "answer", AsyncMock())

    update = Update(update_id=66, callback_query=cb)

    await dp.feed_update(bot, update)

    # Проверяем, что текст сообщения обновился
    Message.edit_text.assert_awaited_once()
    text = Message.edit_text.await_args.args[0]
    assert "test callback" in text.lower()

    # Проверяем, что callback.answer() был вызван
    cb.answer.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_callbacks(bot, fake_callback_sender, monkeypatch):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)
    habit = await sync_to_async(HabitFactory)(user=user, action="test callback")
    inst = await sync_to_async(HabitInstanceFactory)(
        habit=habit,
        status=HabitInstanceStatus.SCHEDULED,
        fix_deadline=timezone.now() + timedelta(days=1)
    )

    monkeypatch.setattr(Message, "edit_text", AsyncMock())

    cb = CallbackQuery(
        id="bbb",
        from_user=User(id=profile.chat_id, is_bot=False, first_name="Tester"),
        chat_instance="ci",
        message=Message(
            message_id=2,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester"),
            text="test callback"
        ),
        data=f"done:{inst.id}"
    )

    monkeypatch.setattr(CallbackQuery, "answer", AsyncMock())

    update = Update(update_id=77, callback_query=cb)

    await dp.feed_update(bot, update)

    # Проверяем, что текст сообщения обновился
    Message.edit_text.assert_awaited_once()
    text = Message.edit_text.await_args.args[0]
    assert "test callback" in text.lower()

    # Проверяем, что callback.answer() был вызван
    cb.answer.assert_awaited_once()
