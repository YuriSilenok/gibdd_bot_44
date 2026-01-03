"""Модуль для запуска"""

import os
import socket
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import add_routers

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")


async def main():
    """Запуск бота"""
    # Способ 1: Используйте connector_kwargs (должен работать в 3.13.1)
    session = AiohttpSession(connector_kwargs={"family": socket.AF_INET})

    bot = Bot(token=TOKEN, session=session)

    dp = Dispatcher()
    try:
        add_routers(dp)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
