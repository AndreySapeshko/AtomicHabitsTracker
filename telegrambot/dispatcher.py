from aiogram import Dispatcher

from telegrambot.handlers.callbacks import router as callback_router

from .handlers.basic import router as basic_router

dp = Dispatcher()
dp.include_router(basic_router)
dp.include_router(callback_router)
