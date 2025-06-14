"""Фильтр для проверки роли Начальник"""

from aiogram.types import Message
from database.models import UserRole, Role
from filters.user import IsUser


class IsChief(IsUser):
    """Проверяет является ли пользователь Начальником"""

    @staticmethod
    async def check(user_id: int) -> bool:
        """Проверка роли"""
        chief_role = Role.get_or_none(name="Начальник")
        if not chief_role:
            return False
        return UserRole.select().where(
            (UserRole.user == user_id)
            & (UserRole.role == chief_role)
        ).exists()

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)
