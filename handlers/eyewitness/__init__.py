"""Подключение роутеров"""

from aiogram import Dispatcher
from .send_message import router as send_message_router


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(
        send_message_router,
    )
