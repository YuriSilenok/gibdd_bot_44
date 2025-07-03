"""подключение роутеров"""

from aiogram import Dispatcher
from .patrol import add_routers as add_routers_patrol
from .role import add_routers as add_routers_role
from . import (
    ban,
    notify,
    send_message,
    show_employees,
    start,
    user_info,
    other,
)


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    add_routers_role(dp)
    add_routers_patrol(dp)
    dp.include_routers(
        ban.router,
        notify.router,
        show_employees.router,
        user_info.router,
        start.router,
        send_message.router,
        other.router,
    )
