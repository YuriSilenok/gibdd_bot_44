"""Библиотеки для проверки пользователя"""

from datetime import datetime
from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.models import User, UserRole


class IsUser(BaseFilter):
    """Проверяет, является ли пользователь и не забанен ли он."""

    role = None

    async def __call__(self, message: Message) -> bool:
        """Проверяет что пользователь существует в системе
        и его бан статус"""

        user: User = User.get_or_none(tg_id=message.from_user.id)

        if user is None:
            return False

        if user.is_ban and user.ban_until and user.ban_until > datetime.now():

            ban_until: str = user.ban_until.strftime("%d-%m-%Y %H:%M")

            await message.answer(
                text=(
                    f"Вы не можете отправлять сообщения до срока окончания"
                    f" бана, напишите снова после {ban_until}"
                )
            )

            return False

        if self.role is None:
            return True

        user_role: UserRole = UserRole.get_or_none(
            user=User.get(tg_id=message.from_user.id), role=self.role
        )

        return user_role is not None
