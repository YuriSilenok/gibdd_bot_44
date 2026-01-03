"""Модуль для запуска"""

import os
import socket
import asyncio
from aiohttp import TCPConnector
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import add_routers

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")


async def main():
    """Запуск бота"""
    bot = Bot(
        token=TOKEN,
        session=AiohttpSession(connector=TCPConnector(family=socket.AF_INET)),
    )
    dp = Dispatcher()
    try:
        add_routers(dp)
        await dp.start_polling(bot, skip_updatet=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
