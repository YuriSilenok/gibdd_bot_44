"""Управление ролями пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_user_info_kb(user_id: int, roles: set):
    """Генерирует клавиатуру на основе имеющихся ролей"""
    buttons = []

    role_actions = {
        "Инспектор": ("Удалить инспектора", "inspector"),
        "Администратор": ("Удалить администратора", "admin")
    }

    for role, (text, key) in role_actions.items():
        if role in roles:
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"remove_role_{user_id}_{key}"
                )
            )

    buttons.append(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_users_list"
        )
    )

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
