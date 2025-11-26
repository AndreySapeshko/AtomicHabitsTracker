from aiogram import Dispatcher

from telegrambot.handlers.basic import router as basic_router
from telegrambot.handlers.callbacks import router as callback_router

dp = Dispatcher()
dp.include_router(basic_router)
dp.include_router(callback_router)
