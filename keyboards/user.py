"""Клавиатуры для очевидцев"""

from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_location_request_kb():
    """Клавиатура с кнопкой запроса геолокации"""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отправить геолокацию",
        callback_data="request_location"
    )
    return builder.as_markup()
