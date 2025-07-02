"""подключение роутеров"""

from aiogram import Dispatcher
from . import add, delete


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(add.router, delete.router)
