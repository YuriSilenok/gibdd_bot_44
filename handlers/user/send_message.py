"""Пересылка сообщения от пользователя инспекторам"""

from aiogram import Router
from aiogram.types import Message
from filters.user import IsUser, IsBan
from filters.inspector import IsInspector
from keyboards.inspector import user_ban_kb
from database.models import User, UserRole, Message as MessageModel

router = Router()


@router.message(IsUser(), IsBan())
async def get_message_from_user(message: Message):
    """Обработчик сообщения от пользователя"""
    await message.answer(
        "Спасибо за обращение. Мы его уже передали инспекторам"
    )
    user_roles = list(
        UserRole.select().where(UserRole.role == IsInspector().role)
    )
    user = User.get_or_none(User.tg_id == message.from_user.id)
    for user_role in user_roles:
        message = await message.bot.send_message(
            chat_id=user_role.user.tg_id,
            text=message.text,
            reply_markup=user_ban_kb(message.from_user.id),

        )

        MessageModel.get_or_create(
            user_id=user.id,
            text=message.text,
            tg_message_id=message.message_id,
            at_created=message.date,
        )
