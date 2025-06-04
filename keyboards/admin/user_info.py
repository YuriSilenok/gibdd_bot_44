"""Клавиатура управления ролями пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import UserRole, Role, User


def get_user_info_kb(user:  User) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с кнопками удаления ролей"""
    buttons = []
    inspector_role = Role.get_or_none(name="Инспектор")
    admin_role = Role.get_or_none(name="Администратор")

    if inspector_role and UserRole.get_or_none(user=user, role=inspector_role):
        buttons.append([
            InlineKeyboardButton(
                text="Удалить роль инспектора",
                callback_data=f"delete_role_{inspector_role.id}_{user.id}"
            )
        ])

    if admin_role and UserRole.get_or_none(user=user, role=admin_role):
        buttons.append([
            InlineKeyboardButton(
                text="Удалить роль администратора",
                callback_data=f"delete_role_{admin_role.id}_{user.id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
