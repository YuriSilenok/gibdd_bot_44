"""Модуль управления блокировками пользователей"""

from datetime import datetime
from typing import List

from aiogram import exceptions, Router, F
from aiogram.types import CallbackQuery

from database.models import UserMessage, ForwardMessage, User

from filters import IsEmployee

from handlers.admin.logic import get_admins
from handlers.employee.logic import ban_user, is_employee
from handlers.eyewitness.logic import send_message_to_employee
from handlers.user.logic import notify_users

from keyboards.employee import user_ban_cobfirm_and_cancel_kb, user_ban_kb

router = Router()


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
        except exceptions.TelegramBadRequest:
            await callback.answer(
                text=f"Не удалось удалить сообщения {message.tg_message_id}"
                f" пользователя {message.to_user.tg_id}"
            )

    ForwardMessage.update(is_delete=True).where(
        (UserMessage.from_user == user) & (~ForwardMessage.is_delete)
    )


@router.callback_query(F.data.startswith("ban_"), IsEmployee())
async def show_confirm(callback: CallbackQuery) -> None:
    """Показать подтверждение бана"""

    try:
        user_message_id = int(callback.data.split(sep="_")[-1])
        user_message: UserMessage = UserMessage.get_by_id(pk=user_message_id)
        user: User = user_message.from_user

        if is_employee(user=user):
            await callback.answer(text="Нельзя заблокировать сотрудника")
            await callback.message.edit_reply_markup(reply_markup=None)

        else:
            await callback.message.edit_reply_markup(
                reply_markup=user_ban_cobfirm_and_cancel_kb(
                    user_message=user_message
                )
            )

    except exceptions.TelegramBadRequest as e:
        await callback.answer(
            text=f"Ошибка при Показать подтверждение бана: {e}"
        )


@router.callback_query(F.data.startswith("user_ban_confirm_"), IsEmployee())
async def confirm_ban(callback: CallbackQuery) -> None:
    """Подтверждение бана"""

    try:
        employee: User = User.get(tg_id=callback.from_user.id)
        user_message_id = int(callback.data.split(sep="_")[-1])
        user_message: UserMessage = UserMessage.get_by_id(pk=user_message_id)
        user_banned: User = user_message.from_user

        if is_employee(user=user_banned):
            await callback.answer(text="Нельзя заблокировать сотрудника")
            await callback.message.edit_reply_markup(reply_markup=None)

        elif user_banned.is_ban and user_banned.ban_until > datetime.now():
            await callback.answer(text="Пользователь уже заблокирован")
            await callback.message.delete()

        else:
            ban_user(user_banned=user_banned)

            await callback.bot.send_message(
                chat_id=user_banned.tg_id,
                text=f"Вы заблокированы до" f" {user_banned.ban_until_strf}",
            )

            await delete_messages(
                callback=callback,
                user=user_banned,
            )

            admins: List[User] = get_admins()

            for admin in admins:
                await send_message_to_employee(
                    bot=callback.bot,
                    user_message=user_message,
                    employee=admin,
                    restore_message_chain=False,
                )

            await notify_users(
                bot=callback.bot,
                users=admins,
                text=(
                    f"Пользователь {user_banned} заблокирован\n"
                    f"Заблокировал: {employee}\n"
                    f"Бан до: {user_banned.ban_until_strf}"
                ),
            )

            await callback.answer(text="Пользователь заблокирован")
            await callback.message.delete()

    except exceptions.TelegramBadRequest as e:
        await callback.answer(text=f"Ошибка: {e}")


@router.callback_query(F.data.startswith("user_ban_cancel_"), IsEmployee())
async def cancel_ban(callback: CallbackQuery) -> None:
    """Отмена бана"""

    user_message_id = int(callback.data.split(sep="_")[-1])
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_kb(
            user_message=UserMessage.get_by_id(pk=user_message_id)
        )
    )
