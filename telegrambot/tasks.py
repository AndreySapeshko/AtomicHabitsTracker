from celery import shared_task


@shared_task
def send_telegram_message(chat_id: int, text: str, reply_markup=None):
    import asyncio

    from telegrambot.bot import bot

    async def _send():
        await bot.send_message(chat_id, text, reply_markup=reply_markup)

    asyncio.run(_send())
