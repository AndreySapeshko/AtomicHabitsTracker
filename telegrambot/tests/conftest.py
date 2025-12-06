# tests/telegram/conftest.py
import pytest
from unittest.mock import AsyncMock
from aiogram import Dispatcher
from aiogram import Bot

from users.tests.factory import UserFactory
from habits.tests.factory import HabitFactory
from habit_instances.tests.factory import HabitInstanceFactory


@pytest.fixture
def bot():
    """Mocked Telegram Bot (Aiogram 3.x)."""
    mock = AsyncMock(spec=Bot)
    mock.id = 777000
    mock.send_message = AsyncMock()
    mock.send_photo = AsyncMock()
    return mock


@pytest.fixture
def dp():
    """Dispatcher used in every Telegram test."""
    return Dispatcher()


@pytest.fixture
def fake_sender(monkeypatch):
    """
    Substitute your DI Sender, which is used in handlers.
    """
    fake = AsyncMock()
    fake.send_message = AsyncMock()
    fake.send_photo = AsyncMock()

    # monkeypatch your import path (adjust to your project layout)
    monkeypatch.setattr(f"telegrambot.handlers.basic.sender", fake)

    return fake


@pytest.fixture
def fake_bind_sender(monkeypatch):
    """
    Substitute your DI Sender, which is used in handlers.
    """
    fake = AsyncMock()
    fake.send_message = AsyncMock()
    fake.send_photo = AsyncMock()

    # monkeypatch your import path (adjust to your project layout)
    monkeypatch.setattr(f"telegrambot.handlers.bind.sender", fake)

    return fake


@pytest.fixture
def fake_profile_sender(monkeypatch):
    """
    Substitute your DI Sender, which is used in handlers.
    """
    fake = AsyncMock()
    fake.send_message = AsyncMock()
    fake.send_photo = AsyncMock()

    # monkeypatch your import path (adjust to your project layout)
    monkeypatch.setattr(f"telegrambot.handlers.profile.sender", fake)

    return fake


@pytest.fixture
def fake_habits_sender(monkeypatch):
    """
    Substitute your DI Sender, which is used in handlers.
    """
    fake = AsyncMock()
    fake.send_message = AsyncMock()
    fake.send_photo = AsyncMock()

    # monkeypatch your import path (adjust to your project layout)
    monkeypatch.setattr(f"telegrambot.handlers.habits.sender", fake)

    return fake


@pytest.fixture
def fake_today_sender(monkeypatch):
    """
    Substitute your DI Sender, which is used in handlers.
    """
    fake = AsyncMock()
    fake.send_message = AsyncMock()
    fake.send_photo = AsyncMock()

    # monkeypatch your import path (adjust to your project layout)
    monkeypatch.setattr(f"telegrambot.handlers.today.sender", fake)

    return fake


@pytest.fixture
def fake_callback_sender(monkeypatch):
    """
    Substitute your DI Sender, which is used in handlers.
    """
    fake = AsyncMock()
    fake.send_message = AsyncMock()
    fake.send_photo = AsyncMock()

    # monkeypatch your import path (adjust to your project layout)
    monkeypatch.setattr(f"telegrambot.services.sender.sender", fake)

    return fake


@pytest.fixture
def fake_api(monkeypatch):
    """
    Fake backend API used by Telegram bot.
    """
    api = AsyncMock()

    monkeypatch.setattr("telegrambot.", api)
    return api


@pytest.fixture
def fake_redis(monkeypatch):
    """
    Fake Redis storage for cross-communication Django ↔ Telegram.
    """
    storage = {}

    class FakeRedis:
        async def get(self, key):
            return storage.get(key)

        async def set(self, key, value):
            storage[key] = value

        async def delete(self, key):
            storage.pop(key, None)

    monkeypatch.setattr("telegrambot.redis_queue.get_redis", FakeRedis())
    return storage


@pytest.fixture
def user(db):
    return UserFactory()
