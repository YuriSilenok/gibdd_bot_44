"""Модуль для запуска"""

import os
import socket
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import add_routers

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")


async def main():
    """Запуск бота"""
    # Создаем сессию
    session = AiohttpSession()

    # Устанавливаем параметры коннектора через _connector_init
    # Это атрибут, который будет использоваться при создании коннектора
    session._connector_init = {
        "family": socket.AF_INET,
        "limit": 100,
        "ttl_dns_cache": 300,
    }

    bot = Bot(
        token=TOKEN,
        session=session,
    )

    dp = Dispatcher()
    try:
        add_routers(dp)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
