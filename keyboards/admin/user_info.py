"""Клавиатура управления ролями пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Role


def get_user_info_kb(user, roles: set):
    """Генерирует клавиатуру для управления ролями"""
    buttons = []

    all_roles = {r.name: r.id for r in Role.select()}

    for role_name in roles:
        if role_name in all_roles:
            buttons.append(InlineKeyboardButton(
                text=f"Удалить {role_name.lower()}",
                callback_data=f"delete_role_{all_roles[role_name]}_{user.id}"
            ))

    buttons.append(InlineKeyboardButton(
        text="Назад к списку",
        callback_data="back_to_users_list"
    ))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
