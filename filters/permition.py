"""Библиотеки для проверки пользователя"""

from datetime import datetime
from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.models import RolePermition, User, UserRole, Permition
from utils import message_answer, telegram_network_error


class IsPermition(BaseFilter):
    """Проверяет наличие привелегии у пользователя"""

    def __init__(self, permition_name: str = None):
        self.permition = (
            Permition.get(name=permition_name) if permition_name else None
        )

    def check(self, user: User) -> bool:
        """Проверяет у пользователя привелегию"""

        permition: Permition = (
            RolePermition.select()
            .join(UserRole, on=UserRole.role == RolePermition.role)
            .where(
                (UserRole.user == user)
                & (RolePermition.permition == self.permition)
            )
            .first()
        )
        return permition is not None

    async def __call__(self, message: Message) -> bool:
        user: User = User.get_or_none(tg_id=message.from_user.id)

        if user is None:
            return False

        if user.is_ban and user.ban_until and user.ban_until > datetime.now():

            ban_until: str = user.ban_until.strftime("%d-%m-%Y %H:%M")

            await message_answer(
                message=message,
                text=(
                    f"Вы не можете отправлять сообщения до срока окончания"
                    f" бана, напишите снова после {ban_until}"
                ),
            )

            return False

        return self.check(user)
