# tests/telegram/test_sender.py
import pytest
from unittest.mock import AsyncMock
from telegrambot.services.sender import TelegramSender


@pytest.mark.asyncio
async def test_sender_send_message():
    bot = AsyncMock()
    bot.send_message = AsyncMock()

    sender = TelegramSender(bot=bot)

    await sender.send(chat_id=111, text="Hello!")

    bot.send_message.assert_awaited_once()
