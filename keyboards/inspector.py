"""Клавиатура Инспектора"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )

from database.models import User, Patrol


def get_keyboard_by_user(user: User):
    """Получение списка кнопок"""

    is_patrol = Patrol.get_or_none(
        (Patrol.inspector == user) &
        (Patrol.end.is_null())
    )
    return [
        [
            KeyboardButton(
                text="Закончить патрулирование" if is_patrol
                else "Начать патрулирование"
            )
        ]
    ]


def get_kb_by_user(user: User):
    """Получение клавиатуры патрулирования"""

    return ReplyKeyboardMarkup(
        keyboard=get_keyboard_by_user(user),
        resize_keyboard=True,
    )


def user_ban_cobfirm_and_cancel_kb(user_id: int):
    """Подтвердение блокирования пользователя"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=f"user_ban_confirm_{user_id}",
                ),
                InlineKeyboardButton(
                    text="Отменить", callback_data="user_ban_cancel"
                ),
            ]
        ]
    )


def user_ban_kb(user_id: int):
    """Блокирование пользователя"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Бан", callback_data=f"ban_{user_id}"
                ),
            ]
        ]
    )
