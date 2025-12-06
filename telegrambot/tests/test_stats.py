import pytest

from aiogram.types import Update, Message, User, Chat
from asgiref.sync import sync_to_async
from django.utils import timezone

from habits.tests.factory import HabitFactory
from telegrambot.handlers.habits import router as habits_router
from telegrambot.tests.factory import ProfileFactory
from users.tests.factory import UserFactory
from habit_instances.tests.factory import HabitInstanceFactory
from habit_instances.models import HabitInstanceStatus


# @pytest.mark.asyncio
# @pytest.mark.django_db
# async def test_stats(dp, bot, fake_habits_sender):
#     # dp.include_router(habits_router)
#     user = await sync_to_async(UserFactory)()
#     profile = await sync_to_async(ProfileFactory)(user=user)
#     habit = await sync_to_async(HabitFactory)(id=7, user=user)
#     await sync_to_async(HabitInstanceFactory.create_batch)(
#         3, habit=habit,
#         status=HabitInstanceStatus.COMPLETED
#     )
#     await sync_to_async(HabitInstanceFactory.create_batch)(
#         2, habit=habit,
#         status=HabitInstanceStatus.MISSED
#     )
#
#     update = Update(
#         update_id=44,
#         message=Message(
#             message_id=404,
#             date=timezone.now(),
#             chat=Chat(id=profile.chat_id, type="private"),
#             from_user=User(id=user.id, is_bot=False, first_name="Tester"),
#             text=f"/stats_{habit.id}",
#         ),
#     )
#     print(f"update.message.text: {update.message.text}")
#     await dp.feed_update(bot, update)
#
#     fake_habits_sender.send.assert_awaited_once()
#     fake_habits_sender.send.assert_awaited()
#     text = fake_habits_sender.send.await_args.args[1]
#
#     assert "Выполнено: 3" in text
#     assert "Пропущено: 2" in text
