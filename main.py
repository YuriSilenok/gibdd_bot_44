"""Модуль для запуска"""

import os
import socket
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import add_routers

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")


async def main():
    """Запуск бота"""
    # Создаем aiohttp коннектор с AF_INET
    connector = aiohttp.TCPConnector(family=socket.AF_INET)

    # Создаем aiohttp ClientSession
    http_session = aiohttp.ClientSession(connector=connector)

    # Создаем сессию для aiogram, передавая созданную http сессию
    session = AiohttpSession(session=http_session)

    bot = Bot(token=TOKEN, session=session)

    dp = Dispatcher()
    try:
        add_routers(dp)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        # Важно закрыть обе сессии
        await session.close()
        await http_session.close()


if __name__ == "__main__":
    asyncio.run(main())
