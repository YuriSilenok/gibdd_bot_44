"""Клавиатура Инспектора"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from database.models import User, Patrol


def get_keyboard_by_user(user: User):
    """Получение списка кнопок"""

    is_patrol = Patrol.get_or_none(
        (Patrol.inspector == user) & (Patrol.end.is_null())
    )
    return [
        [
            KeyboardButton(
                text=(
                    "Закончить патрулирование"
                    if is_patrol
                    else "Начать патрулирование"
                )
            ),
            KeyboardButton(
                text=("\U0001F6A8")
            )
        ]
    ]


def get_kb_by_user(user: User):
    """Получение клавиатуры патрулирования"""

    return ReplyKeyboardMarkup(
        keyboard=get_keyboard_by_user(user),
        resize_keyboard=True,
    )
