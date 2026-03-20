"""Включение и выключение уведомлений администратора"""

from aiogram import Router, F
from aiogram.types import Message
from database.models import User, Admin
from filters.permition import IsPermition
from keyboards.common import get_kb_by_user
from utils import message_answer

router = Router()


@router.message(
    F.text == "Получать сообщения очевидцев",
    IsPermition("Получать сообщения очевидцев"),
)
async def enable_notifications(message: Message):
    """Включает получения сообщей очевидцев"""

    user: User = User.get(tg_id=message.from_user.id)
    admin: Admin = Admin.get_or_none(user=user)

    if not admin:
        admin = Admin.create(user=user)

    if admin.is_notify:
        await message_answer(
            message=message,
            text="Ранее Вы уже включили получение сообщений от очевидцев",
            reply_markup=get_kb_by_user(user=user),
        )
        return

    admin.is_notify = True
    admin.save()

    await message_answer(
        message=message,
        text="Теперь Вы будете получать сообщения от очевидцев",
        reply_markup=get_kb_by_user(user=user),
    )


@router.message(
    F.text == "Не получать сообщения очевидцев",
    IsPermition("Не получать сообщения очевидцев"),
)
async def disable_notifications(message: Message):
    """Выключает получения сообщей очевидцев"""

    user: User = User.get(tg_id=message.from_user.id)
    admin: Admin = Admin.get_or_none(user=user)

    if not admin:
        admin = Admin.create(user=user)

    if not admin.is_notify:
        await message_answer(
            message=message,
            text="Ранее Вы Уже выключили получение сообщений от очевидцев",
            reply_markup=get_kb_by_user(user=user),
        )
        return

    admin.is_notify = False
    admin.save()

    await message_answer(
        message=message,
        text="Теперь Вы не будете получать сообщения от очевидцев",
        reply_markup=get_kb_by_user(user=user),
    )
