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
    # Создаем сессию с таймаутами
    session = AiohttpSession(
        timeout=30.0,  # Общий таймаут
    )
    
    # Настройки коннектора
    session._connector_init = {
        "family": socket.AF_INET,
        "limit": 100,
        "ttl_dns_cache": 300,
        "force_close": False,
        "enable_cleanup_closed": True,
    }

    # Создаем бота с настройками таймаутов
    bot = Bot(
        token=TOKEN,
        session=session,
        # Таймауты передаются напрямую в Bot
        read_timeout=20.0,    # Таймаут чтения данных
        write_timeout=20.0,   # Таймаут отправки данных
        connect_timeout=10.0, # Таймаут установки соединения
        pool_timeout=1.0,     # ВАЖНО: не ждать свободного соединения
    )

    dp = Dispatcher()
    
    try:
        add_routers(dp)
        # Обертываем polling в цикл для автоматического перезапуска
        while True:
            try:
                print("Запуск polling...")
                await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
            except Exception as e:
                print(f"Ошибка polling: {e}. Перезапуск через 10 секунд...")
                await asyncio.sleep(10)
                continue
    except KeyboardInterrupt:
        print("Бот остановлен")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())