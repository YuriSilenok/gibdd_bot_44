import asyncio
import functools
from aiogram.exceptions import TelegramNetworkError

def telegram_network_error(func):
    """Декоратор для сбоев сети интернет"""

    @functools.wraps(func)
    async def wrapper(*args, **qwargs):
        for delay in range(1, 10):
            try:
                return await func(*args, **qwargs)
            except TelegramNetworkError as ex:
                print(str(ex))
                await asyncio.sleep(delay=delay)

    return wrapper