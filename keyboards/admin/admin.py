"""Клавиатуры для Администратора"""

from typing import List
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from database.models import User, Admin, Role, UserRole, Patrol
from filters.inspector import IsInspector


ADMIN_KEYBOARD: List[List[KeyboardButton]] = [
    [
        KeyboardButton(text="Добавить инспектора"),
        KeyboardButton(text="Показать инспекторов"),
    ],
    [
        KeyboardButton(text="Добавить администратора"),
        KeyboardButton(text="Показать администраторов"),
    ],
]


def get_keyboard_by_user(user: User) -> List[List[KeyboardButton]]:
    """Кнопки для клавиатуры администратора"""

    admin: Admin = Admin.get_or_none(user=user)
    return ADMIN_KEYBOARD + [
        [
            (
                KeyboardButton(text="Не получать сообщения очевидцев")
                if admin and admin.is_notify
                else KeyboardButton(text="Получать сообщения очевидцев")
            )
        ]
    ]


def get_kb_by_user(user: User) -> ReplyKeyboardMarkup:
    """Клавиатура администратора"""

    return ReplyKeyboardMarkup(
        keyboard=get_keyboard_by_user(user=user),
        resize_keyboard=True,
    )


def get_kb_by_show_employees(
    role: Role, page: int, limit: int = 10
) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру пользователей"""

    inspector_in_patrol = set()
    if IsInspector.role == role:
        inspector_in_patrol = {
            p.inspector.id
            for p in Patrol.select().where(Patrol.end.is_null()).execute()
        }

    inline_keyboard: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=" ".join(
                    [
                        "🚨" if ur.user.id in inspector_in_patrol else "",
                        f"@{ur.user.username}" if ur.user.username else "",
                        f"{ur.user.full_name}",
                    ]
                ),
                callback_data=f"user_info_{ur.user.id}",
            )
        ]
        for ur in UserRole.select()
        .where(UserRole.role == role)
        .offset((page - 1) * limit)
        .limit(limit)
    ]
    last_row = []
    if page > 1:
        last_row.append(
            InlineKeyboardButton(
                text="Назад",
                callback_data=f"users_page_{role}_{page-1}",
            )
        )

    last_row.append(
        InlineKeyboardButton(
            text=f"Страница: {page}",
            callback_data="alert",
        )
    )

    if len(inline_keyboard) == limit:
        last_row.append(
            InlineKeyboardButton(
                text="Вперед",
                callback_data=f"users_page_{role}_{page+1}",
            )
        )

    if last_row:
        inline_keyboard.append(last_row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
