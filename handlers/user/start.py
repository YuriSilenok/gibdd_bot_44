"""Обработка команды start"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database.models import User, UserRole
from keyboards.admin import ADMIN_START_KEYBOARD as ask

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, callback: CallbackQuery):
    """Обработчик команды start"""

    user = User.get_or_none(tg_id=message.from_user.id)

    if not (user is None) and UserRole.get(tg_id=user).role == 'Администратор':
        await callback.message.edit_reply_markup(reply_markup=ask)
        return

    await message.answer(
        text='Добрый день.Через этого бота '
        'Вы можете отправить анонимное сообщение о пьяном водителе'
    )

    if user is None:
        User.create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            last_name=message.from_user.last_name,
            first_name=message.from_user.first_name,
        )

    elif (
        User.username != message.from_user.username or
        User.last_name != message.from_user.last_name or
        User.first_name != message.from_user.first_name
    ):
        user.username = message.from_user.username
        user.last_name = message.from_user.last_name
        user.first_name = message.from_user.first_name
        user.save()
