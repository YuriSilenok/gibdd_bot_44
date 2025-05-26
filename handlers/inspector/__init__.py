"""подключение роутеров"""

from aiogram import Dispatcher
from .user_ban import router as user_ban
from .start_end_patrol import router as start_end_patrol_router


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(user_ban, start_end_patrol_router)
