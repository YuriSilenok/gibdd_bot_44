"""Библеотеки для проверки пользователя"""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.models import User, UserRole


class IsUser(BaseFilter):
    """Проверяет, является ли пользователь."""

    role = None

    async def __call__(self, message: Message) -> bool:
        user = User.get_or_none(tg_id=message.from_user.id) is not None
        if user is None:
            return False

        if self.role is None:
            return True

        user_role = UserRole.get_or_none(
            user=User.get(tg_id=message.from_user.id), role=self.role
        )
        return user_role is not None


class IsBan(BaseFilter):
    """Проверяет, является ли пользователь забаненным."""

    async def __call__(self, message: Message) -> bool:
        user = User.get_or_none(tg_id=message.from_user.id)
        return not user.is_ban
