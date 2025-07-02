"""Клавиатура управления ролями пользователя"""

from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Role, User
from filters.permition import IsPermition


def get_user_info_kb(from_user: User, by_user: User) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с кнопками удаления ролей"""
    buttons: List = []
    for user_role in from_user.user_roles:
        role: Role = user_role.role
        if (
            role.name == "Администратор" 
            and not IsPermition("Удалить роль администратора").check(by_user)
        ):
            continue

        if role.name == "Начальник":
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"Удалить роль {role.name}",
                    callback_data=f"delete_role_{role.id}_{user_role.id}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
