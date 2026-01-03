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
    # Создаем aiohttp сессию с нужными параметрами
    aiohttp_session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(family=socket.AF_INET)
    )

    # Создаем сессию для aiogram
    session = AiohttpSession(
        session=aiohttp_session  # передаем созданную сессию
    )

    bot = Bot(token=TOKEN, session=session)

    dp = Dispatcher()
    try:
        add_routers(dp)
        await dp.start_polling(
            bot, skip_updates=True
        )  # исправлено: skip_updates вместо skip_updatet
    finally:
        await bot.session.close()
        await aiohttp_session.close()  # закрываем и aiohttp сессию


if __name__ == "__main__":
    asyncio.run(main())
