import logging

from aiogram import F, Router, types
from aiogram.types import InlineKeyboardButton
from asgiref.sync import sync_to_async

from habit_instances.models import HabitInstance
from habit_instances.services import complete_instance, miss_instance
from users.model_files.profile import TelegramProfile

logger = logging.getLogger("telegrambot")

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("undo:"))
async def undo_callback_handler(callback: types.CallbackQuery):
    logger.info("Start undo_callback_handler")
    instance_id = callback.data.split(":")[1]
    chat_id = callback.message.chat.id

    # --- 1. Проверяем привязку Telegram ---
    try:
        profile = await sync_to_async(
            lambda: TelegramProfile.objects.select_related("user").get(chat_id=chat_id, is_active=True)
        )()
    except TelegramProfile.DoesNotExist:
        logger.info("Telegram не привязан.")
        await callback.answer("Telegram не привязан.", show_alert=True)
        return

    # --- 2. Получаем инстанс ---
    try:
        instance = await sync_to_async(
            lambda: HabitInstance.objects.select_related("habit").get(id=instance_id, habit__user=profile.user)
        )()
    except HabitInstance.DoesNotExist:
        await callback.answer("Инстанс не найден.", show_alert=True)
        return

    # --- 3. Пытаемся отменить ---
    ok, msg = await sync_to_async(instance.undo_completion)()

    if not ok:
        await callback.answer(msg, show_alert=True)
        return

    # --- 4. Обновляем сообщение ---
    new_status = "⏳ Ожидает выполнения"
    text = (
        f"🔄 Статус изменён\n\n"
        f"Привычка: {instance.habit.action}\n"
        f"Время: {instance.scheduled_datetime.strftime('%H:%M')}\n"
        f"Статус: {new_status}"
    )

    # Возвращаем исходную пару кнопок: Выполнено / Не успел
    buttons = [
        [
            InlineKeyboardButton(text="✔️ Выполнено", callback_data=f"done:{instance.id}"),
            InlineKeyboardButton(text="❌ Не успел", callback_data=f"missed:{instance.id}"),
        ]
    ]

    await callback.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))
    logger.info("Отработал callback.message.edit_text")
    await callback.answer("Выполнение отменено.")


@router.callback_query(F.data.startswith(("done:", "missed:")))
async def callbacks(callback: types.CallbackQuery):
    logger.info("Start callback")
    data = callback.data.split(":")

    if len(data) != 2:
        return await callback.answer("Некорректная команда.")

    action, instance_id = data
    instance_id = int(instance_id)

    user_id = callback.from_user.id

    original_text = callback.message.text

    undo_button = InlineKeyboardButton(text="↩️ Отменить выполнение", callback_data=f"undo:{instance_id}")
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[undo_button]])

    if action == "done":
        ok = await sync_to_async(complete_instance)(instance_id, user_id)
        if ok:
            new_text = original_text + "\n\nОтлично! Привычка отмечена как выполненная 👍"
            await callback.message.edit_text(new_text, reply_markup=markup)
            return await callback.answer("Привычка выполнена.")
        else:
            return await callback.answer("Нельзя выполнить эту привычку.", show_alert=True)

    elif action == "missed":
        ok = await sync_to_async(miss_instance)(instance_id, user_id)
        if ok:
            new_text = original_text + "\n\nЗаписал. Привычка пропущена ⛔"
            await callback.message.edit_text(new_text, reply_markup=None)
            return await callback.answer("Привычка пропущена.")
        else:
            return await callback.answer("Нельзя изменить статус.", show_alert=True)
    return None
