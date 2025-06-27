"""Библеотеки для проверки Инспектора"""

from database.models import Role
from filters.user import IsUser


# pylint: disable=R0903
class IsInspector(IsUser):
    """Проверяет является ли пользователь Инспектором"""

    role: Role = Role.get(name="Инспектор")
