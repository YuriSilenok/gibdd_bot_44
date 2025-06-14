"""Клавиатура для сотрудника"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from database.models import UserRole


def is_staff(user_id: int) -> bool:
    """Проверка является ли пользователь сотрудником"""
    return UserRole.select().where(UserRole.user == user_id).exists()


def user_ban_cobfirm_and_cancel_kb(user_id: int):
    """Подтверждение блокирования пользователя"""
    if is_staff(user_id):
        return InlineKeyboardMarkup(inline_keyboard=[])

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
    if is_staff(user_id):
        return InlineKeyboardMarkup(inline_keyboard=[])

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Бан", callback_data=f"ban_{user_id}"
                ),
            ]
        ]
    )
