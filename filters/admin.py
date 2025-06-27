"""Библеотеки для проверки Администратора"""

from database.models import Role
from filters.user import IsUser


# pylint: disable=R0903
class IsAdmin(IsUser):
    """Проверяет является ли пользователь Администратором"""

    role: Role = Role.get(name="Администратор")
