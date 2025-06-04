"""подключение роутеров"""

from aiogram import Dispatcher
from .user import add_routers as add_routers_user
from .eyewitness import add_routers as add_routers_eyewitness
from .admin import add_routers as add_routers_admin
from .inspector import add_routers as add_routers_inspector
from .employee import add_routers as add_router_employee


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    add_routers_admin(dp)
    add_routers_inspector(dp)
    add_router_employee(dp)
    add_routers_eyewitness(dp)
    add_routers_user(dp)
