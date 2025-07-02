"""Модуль управления блокировками пользователей"""

from datetime import datetime
from typing import List

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from controller.employee import is_employee
from controller.message.delete import delete_messages
from database.models import UserMessage, User

from filters.permition import IsPermition

from controller.admin import get_admins
from controller.ban import ban_user
from controller.message.forward import send_message_to_employee
from controller.message.sending import sending_messages

from keyboards.employee import user_ban_cobfirm_and_cancel_kb, user_ban_kb

router = Router()


@router.callback_query(
    F.data.startswith("ban_"),
    IsPermition("Бан пользователя")
)
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

    except TelegramBadRequest as e:
        await callback.answer(
            text=f"Ошибка при Показать подтверждение бана: {e}"
        )


@router.callback_query(
    F.data.startswith("user_ban_confirm_"),
    IsPermition("Бан пользователя")
)
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

            await sending_messages(
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

    except TelegramBadRequest as e:
        await callback.answer(text=f"Ошибка: {e}")


@router.callback_query(
    F.data.startswith("user_ban_cancel_"),
    IsPermition("Бан пользователя")
)
async def cancel_ban(callback: CallbackQuery) -> None:
    """Отмена бана"""

    user_message_id = int(callback.data.split(sep="_")[-1])
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_kb(
            user_message=UserMessage.get_by_id(pk=user_message_id)
        )
    )
