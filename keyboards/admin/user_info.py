"""Клавиатура управления ролями пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_user_info_kb(user):
    """Генерирует клавиатуру с кнопками удаления ролей"""
    buttons = []
    for user_role in user.user_roles:
        buttons.append([
            InlineKeyboardButton(
                text=f"Удалить роль {user_role.role.name}",
                callback_data=f"delete_role_{user_role.role.id}_{user.id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
