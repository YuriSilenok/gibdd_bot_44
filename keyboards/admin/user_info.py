"""Модуль клавиатур для информации о пользователе"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import User, UserRole
from filters.chief import IsChief


def get_user_info_kb(user: User, current_user: User) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру управления ролями пользователя"""
    buttons = []
    current_is_chief = UserRole.select().where(
        (UserRole.user == current_user)
        & (UserRole.role == IsChief.role)
    ).exists()

    for user_role in user.user_roles:
        if (current_is_chief and user_role.role.name in ["Администратор",
                                                         "Инспектор"]) or \
           (not current_is_chief and user_role.role.name == "Инспектор"):
            buttons.append([
                InlineKeyboardButton(
                    text=f"Удалить {user_role.role.name.lower()}",
                    callback_data=f"delete_role_{user_role.role.id}_{user.id}",
                )
            ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
