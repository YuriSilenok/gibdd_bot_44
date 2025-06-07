"""Забинить пользователя"""

from typing import List
from aiogram import exceptions
from aiogram import Router, F
from aiogram.types import CallbackQuery
from filters import IsEmployee, IsAdmin
from keyboards.employee import (
    user_ban_cobfirm_and_cancel_kb,
    user_ban_kb
)
from database.models import (
    UserMessage,
    ForwardMessage,
    User,
    UserRole
)

router = Router()


# @router.callback_query(F.data.startswith("ban_"), IsEmployee())
async def show_inspectors(callback: CallbackQuery) -> None:
    """Подтверждение блокирования пользователя."""
    user_id: str = callback.data.split("_")[-1]
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_cobfirm_and_cancel_kb(user_id=user_id)
    )


# @router.callback_query(F.data.startswith("user_ban_confirm_"), IsEmployee())
async def blocking_user(callback: CallbackQuery) -> None:
    """Блокировка пользователя."""
    user_id: str = callback.data.split(sep="_")[-1]
    user_to_block: User = User.get(User.tg_id == user_id)

    if user_to_block.is_ban:
        await callback.answer(text="Пользователь заблокирован.")
        return

    user_to_block.is_ban = True
    user_to_block.save()

    user_ban_messages: List[ForwardMessage] = list(
        ForwardMessage
        .select()
        .join(UserMessage)
        .where(
            (UserMessage.from_user == user_to_block) &
            (~ForwardMessage.is_delete)
        )
    )

    for forward_message in user_ban_messages:

        try:
            await callback.bot.delete_message(
                chat_id=forward_message.to_user.tg_id,
                message_id=forward_message.tg_message_id,
            )
        except exceptions.TelegramBadRequest:
            print(f"Сообщение {forward_message.tg_message_id} не найдено")
    ForwardMessage.update(is_delete=True).where(
        ForwardMessage.tg_message_id.in_(user_ban_messages)
    ).execute()

    admins: List[User] = list(
        User.select().join(UserRole).where(
            UserRole.role == IsAdmin.role
        )
    )
    inspector: User = User.get(User.tg_id == callback.from_user.id)
    for admin in admins:
        await callback.bot.send_message(
            chat_id=admin.tg_id,
            text=(
                f"Пользователь {user_to_block.full_name} "
                f"заблокирован инспектором {inspector.full_name}"
            ),
        )


@router.callback_query(F.data.startswith("user_ban_cancel_"), IsEmployee())
async def unblocking_user(callback: CallbackQuery) -> None:
    """Отмена блокировки пользователя."""
    user_id: str = callback.data.split(sep="_")[-1]
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_kb(user_id=user_id)
    )
