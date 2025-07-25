"""Общие функции для очевидца"""

import functools
from datetime import datetime, timedelta
from typing import List
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from database.models import (
    Role,
    User,
    Admin,
    UserMessage,
    UserRole,
    Patrol,
    ForwardMessage,
)
from keyboards.employee import user_ban_kb


def get_prev_message(user_message: UserMessage) -> UserMessage:
    """Получить предыдущее сообщение очевидца"""

    last_hour: datetime = user_message.at_created - timedelta(hours=1)

    return (
        UserMessage.select()
        .where(
            (UserMessage.at_created >= last_hour)
            & (UserMessage.id < user_message.id)
            & (UserMessage.from_user == user_message.from_user)
        )
        .order_by(UserMessage.id.desc())
        .first()
    )


async def forward_text_message(
    bot: Bot,
    user_message: UserMessage,
    prev_message: ForwardMessage,
    employee: User,
) -> Message:
    """Пересылка текстового сообщения"""

    return await bot.send_message(
        chat_id=employee.tg_id,
        text=user_message.text or "-",
        reply_markup=user_ban_kb(user_message=user_message),
        reply_to_message_id=(
            prev_message.tg_message_id if prev_message else None
        ),
    )


async def forward_photo_message(
    bot: Bot,
    user_message: UserMessage,
    prev_message: ForwardMessage,
    employee: User,
) -> Message:
    """Пересылка фото"""

    for file in user_message.file:
        return await bot.send_photo(
            chat_id=employee.tg_id,
            photo=file.file_id,
            caption=user_message.text,
            reply_markup=user_ban_kb(user_message=user_message),
            reply_to_message_id=(
                prev_message.tg_message_id if prev_message else None
            ),
        )


async def forward_video_message(
    bot: Bot,
    user_message: UserMessage,
    prev_message: ForwardMessage,
    employee: User,
) -> Message:
    """Пересылка фото"""

    for file in user_message.file:
        return await bot.send_video(
            chat_id=employee.tg_id,
            video=file.file_id,
            caption=user_message.text,
            reply_markup=user_ban_kb(user_message=user_message),
            reply_to_message_id=(
                prev_message.tg_message_id if prev_message else None
            ),
        )


async def forward_location_message(
    bot: Bot,
    user_message: UserMessage,
    prev_message: ForwardMessage,
    employee: User,
) -> Message:
    """Пересылка фото"""

    for location in user_message.location:
        return await bot.send_location(
            chat_id=employee.tg_id,
            latitude=location.latitude,
            longitude=location.longitude,
            reply_markup=user_ban_kb(user_message=user_message),
            reply_to_message_id=(
                prev_message.tg_message_id if prev_message else None
            ),
        )


async def forward_animation_message(
    bot: Bot,
    user_message: UserMessage,
    prev_message: ForwardMessage,
    employee: User,
) -> Message:
    """Пересылка gif"""

    for file in user_message.file:
        return await bot.send_animation(
            chat_id=employee.tg_id,
            animation=file.file_id,
            caption=user_message.text,
            reply_markup=user_ban_kb(user_message=user_message),
            reply_to_message_id=(
                prev_message.tg_message_id if prev_message else None
            ),
        )


MESSAGE_TYPE = {
    "text": forward_text_message,
    "photo": forward_photo_message,
    "video": forward_video_message,
    "location": forward_location_message,
    "animation": forward_animation_message,
}


def telegram_forbidden_error(func):
    """Декоратор для обработки заблокированного бота"""

    @functools.wraps(func)
    async def wrapper(*args, **qwargs):
        try:
            return await func(*args, **qwargs)
        except (TelegramForbiddenError, TelegramBadRequest) as ex:
            employee = qwargs.get("employee", None)
            if employee:
                print(
                    datetime.now(),
                    f"Сотрудник {employee} заблокировал телеграм бота",
                    ex,
                )
                user_roles: List[UserRole] = employee.user_roles
                for user_role in user_roles:
                    user_role.delete_instance()
            else:
                print(
                    datetime.now(),
                    "Сотрудник заблокировал телеграм бота",
                    ex,
                )

    return wrapper


@telegram_forbidden_error
async def send_message_to_employee(
    bot: Bot,
    user_message: UserMessage,
    employee: User,
    restore_message_chain: bool = True,
) -> ForwardMessage:
    """Переслать сообщение очевидца конкретному сотруднику"""

    # Предыдущее сообщение пользователя
    prev_message: UserMessage = get_prev_message(user_message=user_message)

    prev_forward_message: ForwardMessage = None
    if prev_message:
        prev_forward_message = ForwardMessage.get_or_none(
            user_message=prev_message,
            to_user=employee,
            is_delete=False,
        )
    if prev_message and prev_forward_message is None and restore_message_chain:
        prev_forward_message = await send_message_to_employee(
            bot=bot,
            user_message=prev_message,
            employee=employee,
        )

    try:
        message: Message = await MESSAGE_TYPE[user_message.type.name](
            bot=bot,
            user_message=user_message,
            prev_message=prev_forward_message,
            employee=employee,
        )
    except TelegramBadRequest:
        # Может возникнуть когда сотрудник удалил сообщение,
        # на которое нужно ответить
        if prev_forward_message:
            prev_forward_message.is_delete = True
            prev_forward_message.save()

        prev_forward_message = (
            await send_message_to_employee(
                bot=bot,
                user_message=prev_message,
                employee=employee,
            )
            if restore_message_chain and prev_message
            else None
        )

        message: Message = await MESSAGE_TYPE[user_message.type.name](
            bot=bot,
            user_message=user_message,
            prev_message=prev_forward_message,
            employee=employee,
        )

    # сообщение не было переслано
    if message is None:
        return None

    if prev_forward_message and message.reply_to_message is None:
        prev_forward_message.is_delete = True
        prev_forward_message.save()

    return ForwardMessage.get_or_create(
        user_message=user_message,
        to_user=employee,
        tg_message_id=message.message_id,
    )[0]


async def send_message_to_employees(
    bot: Bot, user_message: UserMessage
) -> None:
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
            (UserRole.role == Role.get(name="Инспектор"))
            & (Patrol.end.is_null())
        )
    )

    for patrole in patroles:
        await send_message_to_employee(
            bot=bot, user_message=user_message, employee=patrole
        )

    # Список админов
    admins: List[User] = list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Admin, on=Admin.user == User.id)
        .where(
            (Admin.is_notify)
            & (
                UserRole.role.in_(
                    [
                        Role.get(name="Администратор"),
                        Role.get(name="Начальник"),
                    ]
                )
            )
        )
    )

    for admin in admins:
        await send_message_to_employee(
            bot=bot, user_message=user_message, employee=admin
        )
