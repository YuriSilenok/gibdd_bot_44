"""Бизнес-логика для алминистратора"""

from typing import Tuple, List
from aiogram.types.contact import Contact

from database.models import Admin, Role, User, UserRole
from filters.admin import IsAdmin


def add_role(contact: Contact, role: Role) -> Tuple[UserRole, bool, User]:
    """Добавить существующему контакту роль"""

    user: User = User.get_or_none(tg_id=contact.user_id)

    if user is None:
        return None, None, None

    if contact.last_name and user.last_name != contact.last_name:
        user.last_name = contact.last_name
        user.save()

    if contact.first_name and user.first_name != contact.first_name:
        user.first_name = contact.first_name
        user.save()

    user_role, is_added = UserRole.get_or_create(user=user, role=role)
    return user_role, is_added, user


def get_admins() -> List[User]:
    """Получить список администраторов"""

    return list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .where(UserRole.role == IsAdmin.role)
    )


def get_admins_for_notify() -> List[User]:
    """Получить администраторов, которых нужно уведомить"""

    return list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Admin, on=Admin.user == User.id)
        .where((UserRole.role == IsAdmin.role) & (Admin.is_notify))
    )
