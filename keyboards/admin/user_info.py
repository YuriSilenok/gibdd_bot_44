"""Клавиатура управления ролями пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_user_info_kb(user, list_type: str):
    """Генерация кнопок в зависимости от типа списка"""
    buttons = []

    if list_type == "admin":
        buttons.append(InlineKeyboardButton(
            text="Удалить роль администратора",
            callback_data=f"admin_role_action_{user.id}"
        ))
    else:
        buttons.append(InlineKeyboardButton(
            text="Удалить роль инспектора",
            callback_data=f"inspector_role_action_{user.id}"
        ))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
