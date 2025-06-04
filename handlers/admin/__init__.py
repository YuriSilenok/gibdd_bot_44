"""подключение роутеров"""

from aiogram import Dispatcher
from .add_role import router as add_role_router
from .show_employees import router as show_employees_router
from .notify import router as notify_router
from .user_info import router as user_info_router


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(
        add_role_router,
        show_employees_router,
        notify_router,
        user_info_router,
    )
