"""Выдача клавиатуры пользователям"""

from aiogram.types import ReplyKeyboardMarkup
from database.models import Role, User, UserRole
from .admin.admin import get_keyboard_by_user as keyboard_admin
from .inspector import get_keyboard_by_user as keyboard_inspector


def get_kb_by_user(user: User) -> ReplyKeyboardMarkup:
    """Выдача клавиатуры по ролям"""

    keyboard = []

    user_role_admin = UserRole.get_or_none(
        (UserRole.user == user) & (UserRole.role == Role.get(name="Администратор"))
    )

    if user_role_admin:
        keyboard += keyboard_admin(user)

    user_role_inspector = UserRole.get_or_none(
        (UserRole.user == user) & (UserRole.role == Role.get(name="Инспектор"))
    )

    if user_role_inspector:
        keyboard += keyboard_inspector(user)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
