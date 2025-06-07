"""Включение и выключение уведомлений админестратора"""

from aiogram import Router, F
from aiogram.types import Message
from database.models import User, Admin
from filters.admin import IsAdmin
from keyboards.common import get_kb_by_user

router = Router()


@router.message(F.text == "Получать соощения очевидцев", IsAdmin())
async def enable_notifications(message: Message):
    """Включает получения сообщей очевидцев"""
    user: User = User.get(tg_id=message.from_user.id)
    admin = Admin.get_or_none(user=user)
    if not admin:
        admin = Admin.create(user=user)

    if admin.is_notify:
        await message.answer(
            text="Ранее Вы уже включили получение сообщений от очевидцев",
            reply_markup=get_kb_by_user(user),
        )
        return

    admin.is_notify = True
    admin.save()
    await message.answer(
        text="Теперь Вы будете получать сообщения от очевидцев",
        reply_markup=get_kb_by_user(user),
    )


@router.message(F.text == "Не получать сообщения очевидцев", IsAdmin())
async def disable_notifications(message: Message):
    """Выключает получения сообщей очевидцев"""
    user: User = User.get(tg_id=message.from_user.id)
    admin = Admin.get_or_none(user=user)
    if not admin:
        admin = Admin.create(user=user)

    if not admin.is_notify:
        await message.answer(
            text="Ранее Вы Уже выключили получение сообщений от очевидцев",
            reply_markup=get_kb_by_user(user),
        )
        return

    admin.is_notify = False
    admin.save()
    await message.answer(
        text="Теперь Вы не будете получать сообщения от очевидцев",
        reply_markup=get_kb_by_user(user),
    )
