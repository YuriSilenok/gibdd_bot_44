"""Модуль для запуска"""

import os
import socket
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from handlers import add_routers

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")


async def main():
    """Запуск бота"""
    # Создаем сессию с таймаутами
    session = AiohttpSession(
        # Ключевые параметры для решения ServerDisconnectedError
        timeout=30.0,  # Общий таймаут на операцию (уменьшите если ошибки частые)
    )

    # Дополнительные настройки коннектора
    session._connector_init = {
        "family": socket.AF_INET,
        "limit": 100,
        "ttl_dns_cache": 300,
        # Добавляем keepalive для стабильности соединения
        "force_close": False,
        "enable_cleanup_closed": True,
    }

    # Создаем бота с настройками по умолчанию
    bot_settings = DefaultBotProperties(
        # Устанавливаем таймауты для запросов к Telegram API
        read_timeout=20.0,  # Таймаут чтения данных
        write_timeout=20.0,  # Таймаут отправки данных
        connect_timeout=10.0,  # Таймаут установки соединения
        pool_timeout=1.0,  # ВАЖНО: не ждать свободного соединения
    )

    bot = Bot(
        token=TOKEN,
        session=session,
        default=bot_settings,  # Передаем настройки
    )

    dp = Dispatcher()

    try:
        add_routers(dp)
        # Обертываем polling в цикл для автоматического перезапуска
        while True:
            try:
                print("Запуск polling...")
                await dp.start_polling(bot)
            except Exception as e:
                print(f"Ошибка polling: {e}. Перезапуск через 10 секунд...")
                await asyncio.sleep(10)
                continue
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
