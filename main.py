"""Модуль для запуска"""

import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import add_routers

PROXY_HOST = '195.158.194.61'
PROXY_PORT = 8000
PROXY_LOGIN = 'gzwnxz'
PROXY_PASSWORD = 'eYE93q'

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
proxy_url = f'socks5://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
session = AiohttpSession(proxy=proxy_url)
BOT = Bot(token=TOKEN, session=session)
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
