"""Выдача клавиатуры пользователям"""

from aiogram.types import ReplyKeyboardMarkup
from filters.admin import IsAdmin
from filters.inspector import IsInspector
from database.models import User, UserRole
from .admin.admin import get_keyboard_by_user as keyboard_admin
from .inspector import get_keyboard_by_user as keyboard_inspector


def get_kb_by_user(user: User) -> ReplyKeyboardMarkup:
    """Выдача клавиатуры по ролям"""

    keyboard = []

    user_role_admin = UserRole.get_or_none(
        (UserRole.user == user) & (UserRole.role == IsAdmin.role)
    )

    if user_role_admin:
        keyboard += keyboard_admin(user)

    user_role_inspector = UserRole.get_or_none(
        (UserRole.user == user) & (UserRole.role == IsInspector.role)
    )

    if user_role_inspector:
        keyboard += keyboard_inspector(user)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
