"""Подключение роутеров"""

from aiogram import Dispatcher
from .ban import router as user_ban_router


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(
        user_ban_router,
    )
