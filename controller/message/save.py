"""Сохранение сообщения в БД"""

from aiogram.types import Message

from database.models import (
    Location,
    MessageFile,
    MessageType,
    User,
    UserMessage,
)


def save_user_message(message: Message) -> UserMessage:
    """Сохранние сообщения в БД"""

    msg: UserMessage = UserMessage.create(
        from_user=User.get(tg_id=message.from_user.id),
        text=(
            message.text
            if message.text
            else message.caption if message.photo or message.video else None
        ),
        type=MessageType.get(name=message.content_type),
    )

    if message.photo:
        MessageFile.get_or_create(
            message=msg, file_id=message.photo[-1].file_id
        )
    if message.video:
        MessageFile.get_or_create(message=msg, file_id=message.video.file_id)
    if message.animation:
        MessageFile.get_or_create(
            message=msg, file_id=message.animation.file_id
        )

    if message.location:
        Location.get_or_create(
            message=msg,
            longitude=message.location.longitude,
            latitude=message.location.latitude,
        )

    return msg
