"""Операции над ролями"""

from typing import Tuple
from aiogram.types.contact import Contact

from database.models import Role, User, UserRole


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