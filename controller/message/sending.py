"""Рассылка сообщений"""

from datetime import datetime
from typing import List
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from database.models import ForwardMessage, User


async def sending_messages(
    bot: Bot,
    users: List[User],
    text: str,
    reply_to_message: ForwardMessage = None,
) -> None:
    """Рассылка сообщений указанным пользователям"""

    for user in users:
        try:
            reply_to_message_id: int = (
                reply_to_message.tg_message_id if reply_to_message else None
            )
            await bot.send_message(
                chat_id=user.tg_id,
                text=text,
                reply_to_message_id=reply_to_message_id,
            )
        except TelegramForbiddenError:
            print(
                datetime.now(),
                f"Пользователь заблокировал бота {user}",
            )
