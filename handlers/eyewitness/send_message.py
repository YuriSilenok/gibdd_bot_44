"""Пересылка сообщения от пользователя инспекторам"""

from aiogram import Router, F
from aiogram.types import Message
from filters.user import IsUser
from handlers.eyewitness.common import send_message_to_employees


# pylint: disable=E1101

router = Router()


@router.message(F.text, ~F.text.startswith("/"), IsUser())
async def get_message_from_user(message: Message):
    """Обработчик сообщения от пользователя"""

    await send_message_to_employees(message)
