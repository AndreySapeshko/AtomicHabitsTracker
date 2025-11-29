from aiogram import Dispatcher

from telegrambot.handlers import get_handlers

dp = Dispatcher()


def setup_routers():
    for router in get_handlers():
        dp.include_router(router)
    return dp
