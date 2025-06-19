"""Клавиатура для сотрудника"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database.models import UserMessage


def user_ban_cobfirm_and_cancel_kb(
        user_message: UserMessage
) -> InlineKeyboardMarkup:
    """Подтвердение блокирования пользователя"""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=f"user_ban_confirm_{user_message.id}",
                ),
                InlineKeyboardButton(
                    text="Отменить",
                    callback_data=f"user_ban_cancel_{user_message.id}",
                ),
            ]
        ]
    )


def user_ban_kb(user_message: UserMessage) -> InlineKeyboardMarkup:
    """Блокирование пользователя"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Бан", callback_data=f"ban_{user_message.id}"
                ),
            ]
        ]
    )
