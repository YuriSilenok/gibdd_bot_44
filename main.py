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

BOT = Bot(
    token=TOKEN,
    session=AiohttpSession(connector=TCPConnector(family=socket.AF_INET)),
)
DP = Dispatcher()


async def main():
    """Запуск бота"""

    try:
        add_routers(DP)
        await DP.start_polling(BOT, skip_updatet=True)
    finally:
        await BOT.session.close()


if __name__ == "__main__":
    asyncio.run(main())
