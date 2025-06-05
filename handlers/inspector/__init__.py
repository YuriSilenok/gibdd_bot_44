"""подключение роутеров"""

from aiogram import Dispatcher
from .start_patrol import router as start_patrol_router
from .end_patrol import router as end_patrol_router
from .show_patrol import router as show_inspector_router


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_router(show_inspector_router)
    dp.include_router(start_patrol_router)
    dp.include_router(end_patrol_router)
