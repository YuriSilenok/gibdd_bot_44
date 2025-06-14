"""Библеотеки для проверки Инспектора"""

from aiogram.types import Message
from filters.user import IsUser
from filters.admin import IsAdmin
from filters.inspector import IsInspector
from filters.chief import IsChief
from database.models import User, UserRole


# pylint: disable=R0903
class IsEmployee(IsUser):
    """Проверяет является ли пользователь Сотрудником"""

    async def __call__(self, message: Message) -> bool:
        if not await super().__call__(message):
            return False

        user_role = UserRole.get_or_none(
            (UserRole.user == User.get(tg_id=message.from_user.id))
            & (UserRole.role.in_((IsAdmin.role, IsInspector.role,
                                  IsChief.role)))
        )
        return user_role is not None
