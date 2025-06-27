"""Клавиатуры для Администратора"""

from typing import List
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from peewee import DoesNotExist
from database.models import User, Admin, Role, UserRole, Patrol
from filters.inspector import IsInspector
from handlers.inspector.logic import get_patrol


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

def get_inspectors() -> List[User]:
    """Получить инспекторов"""

    return (
        User.select(User)
        .join(UserRole, on=UserRole.user == User.id)
        .where(
            (UserRole.role == IsInspector.role)
        )
    )


def get_kb_by_show_employees(
    role: Role, page: int, limit: int = 10
) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру пользователей"""

    inspectors = get_inspectors()

    inline_keyboard: List[List[InlineKeyboardButton]] = []

    for inspector in inspectors:
        patrol = get_patrol(inspector=inspector)        
        inline_keyboard.append([
            InlineKeyboardButton(
                text=" ".join(
                    [
                        "🚨" if patrol else "",
                        f"@{inspector.username}" if inspector.username else "",
                        f"{inspector.full_name}",
                    ]
                ),
                callback_data=f"user_info_{inspector.id}",
            )
        ])

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
