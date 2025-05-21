"""Клавиатуры для Администратора"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


ADMIN_KEYBOARD = [
    [
        KeyboardButton(text="Добавить инспектора"),
        KeyboardButton(text="Показать инспекторов"),
    ],
    [
        KeyboardButton(text="Добавить администратора"),
        KeyboardButton(text="Показать администраторов"),
    ],
]

KB = ReplyKeyboardMarkup(
    keyboard=ADMIN_KEYBOARD,
    resize_keyboard=True,
)
