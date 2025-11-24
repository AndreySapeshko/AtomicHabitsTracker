from aiogram import Router, types

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

    if action == "done":
        ok = complete_instance(instance_id, user_id)
        if ok:
            return await callback.message.edit_text("Отлично! Привычка отмечена как выполненная 👍")
        else:
            return await callback.answer("Нельзя выполнить эту привычку.", show_alert=True)

    elif action == "missed":
        ok = miss_instance(instance_id, user_id)
        if ok:
            return await callback.message.edit_text("Записал. Привычка пропущена ⛔")
        else:
            return await callback.answer("Нельзя изменить статус.", show_alert=True)
    return None
