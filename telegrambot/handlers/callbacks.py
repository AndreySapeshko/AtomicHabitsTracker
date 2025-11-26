from aiogram import Router, types
from asgiref.sync import sync_to_async

from habit_instances.services import complete_instance, miss_instance

router = Router()


@router.callback_query()
async def callbacks(callback: types.CallbackQuery):
    data = callback.data.split(":")

    if len(data) != 2:
        return await callback.answer("Некорректная команда.")

    action, instance_id = data
    instance_id = int(instance_id)

    user_id = callback.from_user.id

    original_text = callback.message.text

    if action == "done":
        ok = await sync_to_async(complete_instance)(instance_id, user_id)
        if ok:
            new_text = original_text + "\n\nОтлично! Привычка отмечена как выполненная 👍"
            return await callback.message.edit_text(new_text, reply_markup=None)
        else:
            return await callback.answer("Нельзя выполнить эту привычку.", show_alert=True)

    elif action == "missed":
        ok = await sync_to_async(miss_instance)(instance_id, user_id)
        if ok:
            new_text = original_text + "\n\nЗаписал. Привычка пропущена ⛔"
            return await callback.message.edit_text(new_text, reply_markup=None)
        else:
            return await callback.answer("Нельзя изменить статус.", show_alert=True)
    return None
