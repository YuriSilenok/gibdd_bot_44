"""Клавиатура управления ролями пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import UserRole


def get_user_info_kb(user):
    """Генерация кнопок для каждой роли пользователя"""
    buttons = []
    user_roles = list(UserRole.select().where(UserRole.user == user))

    for user_role in user_roles:
        role_name = user_role.role.name.lower()
        buttons.append(InlineKeyboardButton(
            text=f"Удалить роль {role_name}",
            callback_data=f"remove_role_{user_role.role.id}_{user.id}"
        ))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
