"""Обработка команды start"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from database.models import User
from keyboards.common import get_kb_by_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды start"""
    user = User.get_or_none(tg_id=message.from_user.id)
    if user is None:
        User.create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            last_name=message.from_user.last_name,
            first_name=message.from_user.first_name,
        )

    elif (
        User.username != message.from_user.username
        or User.last_name != message.from_user.last_name
        or User.first_name != message.from_user.first_name
    ):
        user.username = message.from_user.username
        user.last_name = message.from_user.last_name
        user.first_name = message.from_user.first_name
        user.save()

    await message.answer(
        "Добрый день.Через этого бота Вы можете "
        "отправить анонимное сообщение о пьяном водителе.",
        reply_markup=get_kb_by_user(user),
    )
