import pytest

from aiogram.types import Update, Message, User, Chat
from asgiref.sync import sync_to_async, async_to_sync
from django.utils import timezone

from telegrambot.handlers.profile import router as profile_router
from users.model_files.profile import TelegramProfile
from .factory import ProfileFactory
from users.tests.factory import UserFactory


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_profile(dp, bot, fake_profile_sender):
    """
    Tests /profile — generates binding code + shows user info.
    """
    dp.include_router(profile_router)
    user = await sync_to_async(UserFactory)(email="tester115@test.com")
    profile = await sync_to_async(ProfileFactory)(user=user, chat_id="757")

    update = Update(
        update_id=22,
        message=Message(
            message_id=202,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(
                id=profile.chat_id,
                is_bot=False,
                first_name="Tester"
            ),
            text="/profile",
        )
    )

    await dp.feed_update(bot, update)

    fake_profile_sender.send.assert_awaited_once()
    text = fake_profile_sender.send.await_args.args[1]

    assert "telegram" in text.lower()
    assert "tester115@test.com" in text

    update = Update(
        update_id=33,
        message=Message(
            message_id=303,
            date=timezone.now(),
            chat=Chat(id=999, type="private"),
            from_user=User(
                id=999,
                is_bot=False,
                first_name="Tester"
            ),
            text="/profile",
        )
    )

    await dp.feed_update(bot, update)

    assert fake_profile_sender.send.await_count == 2
    text = fake_profile_sender.send.await_args.args[1]

    assert "Ваш Telegram не привязан" in text
