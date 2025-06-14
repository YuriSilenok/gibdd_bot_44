"""Фильтр для проверки роли Начальник"""

from aiogram.types import Message
from database.models import Role, UserRole
from filters.user import IsUser


class IsChief(IsUser):
    """Проверяет является ли пользователь Начальником"""

    role = Role.get(name="Начальник")

    async def __call__(self, message: Message) -> bool:
        """Проверка роли через обработчик сообщений"""
        if not await super().__call__(message):
            return False

        return await self.check(message.from_user.id)

    async def check(self, user_id: int) -> bool:
        """Проверка роли по ID пользователя"""
        return UserRole.select().where(
            (UserRole.user == user_id)
            & (UserRole.role == self.role)
        ).exists()
