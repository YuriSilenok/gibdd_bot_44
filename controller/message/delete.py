"""Удаление сообщений"""

from typing import List
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.models import ForwardMessage, User, UserMessage


async def delete_messages(callback: CallbackQuery, user: User) -> None:
    """Удаление сообщений пользователя"""

    messages: List[ForwardMessage] = list(
        ForwardMessage.select()
        .join(UserMessage)
        .where((UserMessage.from_user == user) & (~ForwardMessage.is_delete))
    )
    for message in messages:
        try:
            await callback.bot.delete_message(
                chat_id=message.to_user.tg_id,
                message_id=message.tg_message_id,
            )
        except TelegramBadRequest:
            await callback.answer(
                text=f"Не удалось удалить сообщения {message.tg_message_id}"
                f" пользователя {message.to_user.tg_id}"
            )

    ForwardMessage.update(is_delete=True).where(
        (UserMessage.from_user == user) & (~ForwardMessage.is_delete)
    )
