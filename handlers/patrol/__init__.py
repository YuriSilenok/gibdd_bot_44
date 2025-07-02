"""подключение роутеров"""

from aiogram import Dispatcher
from . import end, start


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(start.router, end.router)
