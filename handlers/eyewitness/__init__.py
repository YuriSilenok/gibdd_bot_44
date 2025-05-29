"""Подключение роутеров"""

from aiogram import Dispatcher
from .send_message import router as send_message_router
from .send_photo import router as send_photo_router
from .send_location import router as send_location_router


def add_routers(dp: Dispatcher):
    """Подключение роутеров"""
    dp.include_routers(
        send_photo_router,
        send_message_router,
        send_location_router,
    )
