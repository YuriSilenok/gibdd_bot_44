"""Логика при взаимодействии над сотрудником"""

from database.models import User, UserRole


def is_employee(user: User) -> bool:
    """Проверка является ли пользователь сотрудником"""
    return UserRole.get_or_none(user=user) is not None
