from datetime import timedelta

import pytest
from aiogram.types import Chat, Message, Update, User
from asgiref.sync import sync_to_async
from django.utils import timezone

from habit_instances.tests.factory import HabitInstanceFactory
from habits.tests.factory import HabitFactory
from telegrambot.handlers.today import router as today_router
from telegrambot.tests.factory import ProfileFactory
from users.tests.factory import UserFactory


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_today(dp, bot, fake_today_sender):
    dp.include_router(today_router)
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)
    habit = await sync_to_async(HabitFactory)(user=user)
    await sync_to_async(HabitInstanceFactory.create_batch)(2, habit=habit, scheduled_datetime=timezone.now())
    await sync_to_async(HabitInstanceFactory)(habit=habit, scheduled_datetime=timezone.now() + timedelta(days=2))

    update = Update(
        update_id=44,
        message=Message(
            message_id=404,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester"),
            text="/today",
        ),
    )

    await dp.feed_update(bot, update)

    fake_today_sender.send.assert_awaited()
    text = fake_today_sender.send.await_args.args[1]

    assert text.count(habit.action) == 2
