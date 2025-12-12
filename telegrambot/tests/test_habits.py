import pytest
from aiogram import Dispatcher
from aiogram.types import Chat, Message, Update, User
from asgiref.sync import sync_to_async
from django.utils import timezone

from habit_instances.models import HabitInstanceStatus
from habit_instances.tests.factory import HabitInstanceFactory
from habits.tests.factory import HabitFactory
from telegrambot.handlers.habits import router as habits_router
from users.tests.factory import UserFactory

from .factory import ProfileFactory

dp = Dispatcher()
dp.include_router(habits_router)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_habits_list(bot, fake_habits_sender):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)
    await sync_to_async(HabitFactory.create_batch)(2, user=user, action="test action")
    await sync_to_async(HabitFactory.create_batch)(1, action="foreign")

    update = Update(
        update_id=33,
        message=Message(
            message_id=303,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester"),
            text="/habits",
        ),
    )

    await dp.feed_update(bot, update)

    fake_habits_sender.send.assert_awaited()
    sent = fake_habits_sender.send.await_args.args[1]

    assert "Ваши привычки" in sent
    assert "test action" in sent.lower()
    assert "foreign" not in sent


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_stats(bot, fake_habits_sender):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)
    habit = await sync_to_async(HabitFactory)(user=user)
    await sync_to_async(HabitInstanceFactory.create_batch)(3, habit=habit, status=HabitInstanceStatus.COMPLETED)
    await sync_to_async(HabitInstanceFactory.create_batch)(2, habit=habit, status=HabitInstanceStatus.MISSED)

    update = Update(
        update_id=44,
        message=Message(
            message_id=404,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester"),
            text=f"/stats_{habit.id}",
        ),
    )

    await dp.feed_update(bot, update)

    fake_habits_sender.send.assert_awaited_once()
    text = fake_habits_sender.send.await_args.args[1]

    assert "Выполнено: 3" in text
    assert "Пропущено: 2" in text


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_detail_habit(bot, fake_habits_sender):
    user = await sync_to_async(UserFactory)()
    profile = await sync_to_async(ProfileFactory)(user=user)
    habit = await sync_to_async(HabitFactory)(user=user, action="test_detail")

    update = Update(
        update_id=44,
        message=Message(
            message_id=404,
            date=timezone.now(),
            chat=Chat(id=profile.chat_id, type="private"),
            from_user=User(id=user.id, is_bot=False, first_name="Tester"),
            text=f"/habit_{habit.id}",
        ),
    )

    await dp.feed_update(bot, update)

    fake_habits_sender.send.assert_awaited_once()
    text = fake_habits_sender.send.await_args.args[1]

    assert "test_detail" in text

    @pytest.mark.asyncio
    @pytest.mark.django_db
    async def test_detail_non_existent_habit(bot, fake_habits_sender):
        user = await sync_to_async(UserFactory)()
        profile = await sync_to_async(ProfileFactory)(user=user)
        await sync_to_async(HabitFactory)(user=user, action="test_detail")

        update = Update(
            update_id=44,
            message=Message(
                message_id=404,
                date=timezone.now(),
                chat=Chat(id=profile.chat_id, type="private"),
                from_user=User(id=user.id, is_bot=False, first_name="Tester"),
                text=f"/habit_{999}",
            ),
        )

        await dp.feed_update(bot, update)

        fake_habits_sender.send.assert_awaited_once()
        text = fake_habits_sender.send.await_args.args[1]

        assert "Привычка не найдена" in text
