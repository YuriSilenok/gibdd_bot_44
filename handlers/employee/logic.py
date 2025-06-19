"""Функции относящиеся к сотрудникам"""

from datetime import datetime, timedelta
from database.models import User, UserRole


def is_employee(user: User) -> bool:
    """Проверка является ли пользователь сотрудником"""
    return UserRole.get_or_none(user=user) is not None


def ban_user(user_banned: User) -> None:
    """Бана пользователя"""

    days: int = 30 if user_banned.ban_count > 0 else 1

    user_banned.ban_until = datetime.now() + timedelta(days=days)
    user_banned.ban_count += 1
    user_banned.is_ban = True
    user_banned.save()
