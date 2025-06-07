"""Общие функции для очевидца"""

from datetime import datetime, timedelta
from typing import List
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from filters import IsAdmin, IsInspector
from database.models import (
    MessageType,
    User,
    Admin,
    UserMessage,
    UserRole,
    Patrol,
    Location,
    MessageFile,
    ForwardMessage,
)
from keyboards.employee import user_ban_kb

# Не находит id у модели, отключаем
# pylint: disable=E1101


def save_user_message(message: Message) -> UserMessage:
    """Сохранние сообщения в БД"""

    msg: UserMessage = UserMessage.get_or_create(
        from_user=User.get(tg_id=message.from_user.id),
        text=(
            message.text if message.text else
            message.caption if message.photo or message.video else
            None
        ),
        type=MessageType.get(name=message.content_type)
    )[0]

    if message.photo or message.video or message.animation:
        MessageFile.get_or_create(
            message=msg, file_id=message.photo[-1].file_id
        )

    if message.location:
        Location.get_or_create(
            message=msg,
            longitude=message.location.longitude,
            latitude=message.location.latitude,
        )

    return msg


def get_prev_message(user_message: UserMessage) -> UserMessage:
    """Получить предыдущее сообщение очевидца"""

    last_hour: datetime = (
        user_message.at_created - timedelta(hours=1)
    )

    return (
        UserMessage
        .select()
        .where(
            UserMessage.at_created >= last_hour
        )
        .order_by(UserMessage.id.desc())
        .first()
    )


async def forward_text_message(
        bot: Bot,
        user_message: UserMessage,
        prev_message: ForwardMessage,
        employee: User) -> Message:
    """Пересылка текстового сообщения"""

    return await bot.send_message(
        chat_id=employee.tg_id,
        text=user_message.text or "-",
        reply_markup=user_ban_kb(
            user_id=user_message.from_user.tg_id
        ),
        reply_to_message_id=prev_message.tg_message_id
        if prev_message else None,
    )


async def forward_photo_message(
        bot: Bot,
        user_message: UserMessage,
        prev_message: ForwardMessage,
        employee: User) -> Message:
    """Пересылка фото"""

    for file in user_message.file:
        return await bot.send_photo(
            chat_id=employee.tg_id,
            photo=file.file_id,
            caption=user_message.text,
            reply_markup=user_ban_kb(
                user_id=user_message.from_user.tg_id
            ),
            reply_to_message_id=prev_message.tg_message_id
            if prev_message else None,
        )


async def forward_video_message(
        bot: Bot,
        user_message: UserMessage,
        prev_message: ForwardMessage,
        employee: User) -> Message:
    """Пересылка фото"""

    for file in user_message.file:
        return await bot.send_video(
            chat_id=employee.tg_id,
            animation=file.file_id,
            caption=user_message.text,
            reply_markup=user_ban_kb(
                user_id=user_message.from_user.tg_id
            ),
            reply_to_message_id=prev_message.tg_message_id
            if prev_message else None,
        )


async def forward_location_message(
        bot: Bot,
        user_message: UserMessage,
        prev_message: ForwardMessage,
        employee: User) -> Message:
    """Пересылка фото"""

    for location in user_message.location:
        return await bot.send_location(
            chat_id=employee.tg_id,
            latitude=location.latitude,
            longitude=location.longitude,
            reply_markup=user_ban_kb(
                user_id=user_message.from_user.tg_id
            ),
            reply_to_message_id=prev_message.tg_message_id
            if prev_message else None,
        )


async def forward_animation_message(
        bot: Bot,
        user_message: UserMessage,
        prev_message: ForwardMessage,
        employee: User) -> Message:
    """Пересылка gif"""

    for file in user_message.file:
        return await bot.send_animation(
            chat_id=employee.tg_id,
            animation=file.file_id,
            caption=user_message.text,
            reply_markup=user_ban_kb(
                user_id=user_message.from_user.tg_id
            ),
            reply_to_message_id=prev_message.tg_message_id
            if prev_message else None,
        )


MESSAGE_TYPE = {
    'text': forward_text_message,
    'photo': forward_photo_message,
    'video': forward_video_message,
    'location': forward_location_message,
    'animation': forward_animation_message,
}


async def send_message_to_employee(
        bot: Bot,
        user_message: UserMessage,
        employee: User) -> None:
    """Переслать сообщение очевидца конкретному сотруднику"""

    # Предыдущее сообщение пользователя
    prev_message: UserMessage = get_prev_message(
        user_message=user_message
    )

    prev_forward_message: ForwardMessage = None
    if prev_message:
        prev_forward_message = (
            ForwardMessage.get_or_none(
                user_message=prev_message,
                to_user=employee,
                is_delete=False,
            )
        )

    try:
        message: Message = (
            await MESSAGE_TYPE[user_message.type.name](
                bot=bot,
                user_message=user_message,
                prev_message=prev_forward_message,
                employee=employee,
            )
        )
    except TelegramBadRequest:
        # Может возникнуть когда сотрудник удалил сообщение,
        # на которое нужно ответить
        prev_forward_message.is_delete = True
        prev_forward_message.save()
        await send_message_to_employee(
            bot=bot,
            user_message=prev_message,
            employee=employee,
        )
        message: Message = (
            await MESSAGE_TYPE[user_message.type.name](
                bot=bot,
                user_message=user_message,
                prev_message=prev_message,
                employee=employee,
            )
        )
    ForwardMessage.get_or_create(
        user_message=user_message,
        to_user=employee,
        tg_message_id=message.message_id,
    )


async def send_message_to_employees(
        bot: Bot,
        user_message: UserMessage) -> None:
    """Отправка сообщений сотрудникам"""

    user: User = user_message.from_user
    if user.is_ban:
        return

    # Список патрульных
    patroles: List[User] = list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Patrol, on=Patrol.inspector == User.id)
        .where(
            (UserRole.role == IsInspector.role)
            & (Patrol.end.is_null())
        )
    )
    for patrole in patroles:
        await send_message_to_employee(
            bot=bot,
            user_message=user_message,
            employee=patrole
        )

    # Список админов
    admins: List[User] = list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Admin, on=Admin.user == User.id)
        .where((Admin.is_notify) & (UserRole.role_id == IsAdmin.role.id))
    )

    for admin in admins:
        await send_message_to_employee(
            bot=bot,
            user_message=user_message,
            employee=admin
        )
