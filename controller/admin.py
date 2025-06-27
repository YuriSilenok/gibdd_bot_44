"""Логика связанная с администратором"""

from typing import List
from database.models import Admin, Role, User, UserRole


def get_admins() -> List[User]:
    """Получить список администраторов"""

    return list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .where(UserRole.role == Role.get(name="Администратор"))
    )


def get_admins_for_notify() -> List[User]:
    """Получить администраторов, которых нужно уведомить"""

    return list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Admin, on=Admin.user == User.id)
        .where(
            (UserRole.role == Role.get(name="Администратор"))
            & (Admin.is_notify)
        )
    )
