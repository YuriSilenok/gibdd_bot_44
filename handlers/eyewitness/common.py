"""Общие функции для очевидца"""

from typing import List
from aiogram.types import Message
from aiogram import exceptions
from filters import IsAdmin, IsInspector
from database.models import (
    User,
    Admin,
    UserRole,
    Photo,
    Patrol,
    Location,
    Message as MessageM,
)
from keyboards.inspector import user_ban_kb
from keyboards.user import get_location_request_kb
# pylint: disable=E1101


async def send_message_to_employ(message: Message, employ: User):
    """Переслать сообщение очевидца конкретному сотруднику"""

    eyewitness: User = User.get(tg_id=message.from_user.id)

    if eyewitness.is_ban:
        # Удаляем все предыдущие сообщения от забаненного пользователя
        messages_to_delete = list(MessageM.select().where(
            (MessageM.from_user == eyewitness)
            )
        )
        for msg in messages_to_delete:
            try:
                await message.bot.delete_message(
                    chat_id=employ.tg_id,
                    message_id=msg.tg_message_id
                )
            except exceptions.TelegramBadRequest as e:
                print(f"Unexpected error when deleting message: {e}")
            msg.is_delete = True
            msg.save()
        return

    last_message: MessageM = (
        MessageM.select()
        .where(
            (MessageM.from_user == eyewitness) & (MessageM.to_user == employ)
        )
        .order_by(MessageM.id.desc())
        .first()
    )

    if last_message is None:
        last_message = (
            MessageM.select()
            .where((MessageM.from_user == eyewitness))
            .order_by(MessageM.id.desc())
            .first()
        )
        if last_message:
            msg: Message = await message.bot.send_message(
                chat_id=employ.tg_id, text=last_message.text
            )
            MessageM.get_or_create(
                to_user=eyewitness,
                from_user=employ,
                text=last_message.text,
                tg_message_id=msg.message_id,
            )

            await send_message_to_employ(message, employ)
            return

    if message.location:
        send_message = await message.bot.send_location(
            chat_id=employ.tg_id,
            latitude=message.location.latitude,
            longitude=message.location.longitude,
            reply_to_message_id=last_message.tg_message_id
            if last_message else None
            )

        loc_message = MessageM.create(
            to_user=employ,
            from_user=eyewitness,
            text="Геолокация",
            tg_message_id=send_message.message_id)

        Location.get_or_create(
            message=loc_message,
            longitude=message.location.longitude,
            latitude=message.location.latitude
        )
        return

    if message.text:
        msg = await message.bot.send_message(
            chat_id=employ.tg_id,
            text=message.text,
            reply_markup=user_ban_kb(eyewitness.tg_id),
            reply_to_message_id=(
                last_message.tg_message_id if last_message else None
            ),
        )
        MessageM.get_or_create(
            from_user=eyewitness,
            to_user=employ,
            text=message.text,
            tg_message_id=msg.message_id,
        )
        return

    if message.photo:

        msg = await message.bot.send_photo(
            chat_id=employ.tg_id,
            photo=message.photo[0].file_id,
            caption=message.caption,
            reply_markup=user_ban_kb(eyewitness.tg_id),
            reply_to_message_id=(
                last_message.tg_message_id if last_message else None
            ),
        )

        message_m, _ = MessageM.get_or_create(
            from_user=eyewitness,
            to_user=employ,
            text=message.caption,
            tg_message_id=msg.message_id,
        )
        Photo.get_or_create(
            message=message_m, file_id=message.photo[0].file_id
        )
        return


async def send_message_to_employees(message: Message):
    """Отправка сообщений сотрудникам"""

    await message.answer(
        "Спасибо за обращение. Мы его уже передали инспекторам. "
        "Вы можете отправить фотографии с места происшествия. "
        "Если хотите отправить геолокацию, нажмите кнопку ниже:",
        reply_markup=get_location_request_kb()
    )
    user = User.get(User.tg_id == message.from_user.id)
    if user.is_ban:
        return

    inspectors: List[User] = list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Patrol, on=Patrol.inspector == User.id)
        .where((UserRole.role == IsInspector.role) & (Patrol.end.is_null()))
    )
    for inspector in inspectors:
        await send_message_to_employ(message, inspector)

    admins: List[User] = list(
        User.select()
        .join(UserRole, on=UserRole.user == User.id)
        .join(Admin, on=Admin.user == User.id)
        .where((Admin.is_notify) & (UserRole.role_id == IsAdmin.role.id))
    )
    for admin in admins:
        await send_message_to_employ(message, admin)
