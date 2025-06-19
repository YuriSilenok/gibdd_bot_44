"""Клавиатура Инспектора"""

from typing import List
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from database.models import User, Patrol


def get_keyboard_by_user(user: User) -> List[List[KeyboardButton]]:
    """Получение списка кнопок"""

    is_patrol: Patrol = Patrol.get_or_none(
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
            )
        ]
    ]


def get_kb_by_user(user: User) -> ReplyKeyboardMarkup:
    """Получение клавиатуры патрулирования"""

    return ReplyKeyboardMarkup(
        keyboard=get_keyboard_by_user(user=user),
        resize_keyboard=True,
    )
