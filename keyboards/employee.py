"""Клавиатура для сотрудника"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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
                    text="Отменить", callback_data=f"user_ban_cancel_{user_id}"
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
