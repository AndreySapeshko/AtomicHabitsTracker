import logging

import requests
from aiogram import F, Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.conf import settings

from telegrambot.services.sender import sender
from users.model_files.profile import TelegramProfile

logger = logging.getLogger("telegrambot")

router = Router()

WEB_URL = settings.WEB_APP_URL


@router.message(F.text.startswith("bind"))
async def bind_code_handler(message: types.Message):
    logger.info("Start bind_code_handler")
    code = message.text.strip()

    if len(code) < 3:
        await message.answer("Введите корректный код привязки.")
        return

    chat_id = message.chat.id
    username = message.from_user.username
    logger.info(f"Start bind_code_handler with: code: {code}, chat_id: {chat_id}, username: {username}")
    # отправляем на Django
    payload = {
        "code": code,
        "chat_id": str(chat_id),
        "username": username,
    }

    try:
        r = requests.post(settings.TELEGRAM_BIND_URL, json=payload, timeout=5)
        logger.info(f"Асинхронно получен status: {r.status_code}")
    except Exception as e:
        await message.answer(f"Сервер недоступен. {e}")
        return

    if r.status_code == 200:
        await message.answer("🎉 Telegram успешно привязан!\nТеперь вы будете получать напоминания.")
    else:
        await message.answer("❌ Неверный код. Проверьте и попробуйте снова.")


@router.message(Command("bind"))
async def bind_cmd(msg: types.Message):
    text = (
        "🔗 <b>Привязка Telegram</b>\n\n"
        f"1. Откройте веб-приложение {WEB_URL}\n"
        "2. Войдите в свой профиль\n"
        "3. Нажмите «Привязать Telegram»\n"
        "4. Отправьте сюда полученный код\n\n"
        "Я автоматически подтвержу связь 😉"
    )
    await sender.send(msg.chat.id, text)


@router.message(Command("unbind"))
async def unbind_handler(message: types.Message):
    chat_id = message.chat.id

    # Проверяем, привязан ли пользователь
    try:
        profile = await sync_to_async(lambda: TelegramProfile.objects.get(chat_id=chat_id, is_active=True))()
    except TelegramProfile.DoesNotExist:
        await message.answer("❗ Telegram не привязан.")
        return

    # Отвязываем
    def deactivate():
        profile.is_active = False
        profile.chat_id = None
        profile.binding_code = None
        profile.save()

    await sync_to_async(deactivate)()

    await message.answer(
        "🔓 Telegram был успешно отвязан от вашего аккаунта.\n" "Чтобы привязать снова — используйте /bind."
    )
