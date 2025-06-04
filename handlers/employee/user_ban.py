"""Забинить пользователя"""

from asyncio import sleep
from aiogram import exceptions
from aiogram import Router, F
from aiogram.types import CallbackQuery
from filters import IsEmployee, IsAdmin
from keyboards.employee import user_ban_cobfirm_and_cancel_kb, user_ban_kb
from database.models import Message, User, UserRole

router = Router()


# @router.callback_query(F.data.startswith("ban_"), IsEmployee())
async def show_inspectors(callback: CallbackQuery):
    """Подтверждение блокирования пользователя."""
    user_id = callback.data.split("_")[-1]
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_cobfirm_and_cancel_kb(user_id)
    )


# @router.callback_query(F.data.startswith("user_ban_confirm_"), IsEmployee())
async def blocking_user(callback: CallbackQuery):
    """Блокировка пользователя."""
    user_id = callback.data.split("_")[-1]
    user_to_block = User.get(User.tg_id == user_id)

    if user_to_block.is_ban:
        await callback.answer("Пользователь заблокирован.")
        return

    user_to_block.is_ban = True
    user_to_block.save()

    message_list = list(
        Message.select().where(Message.from_user == user_to_block)
    )

    for message in message_list:
        try:
            await callback.bot.delete_message(
                chat_id=message.to_user.tg_id,
                message_id=message.tg_message_id,
            )
        except exceptions.TelegramBadRequest:
            print(f"Сообщение {message.tg_message_id} не найдено")
    Message.update(is_delete=True).where(
        Message.tg_message_id.in_(message_list)
    ).execute()

    admins = User.select().join(UserRole).where(UserRole.role == IsAdmin.role)
    inspector = User.get(User.tg_id == callback.from_user.id)
    for admin in admins:
        await callback.bot.send_message(
            chat_id=admin.tg_id,
            text=(
                f"Пользователь {user_to_block.full_name} "
                f"заблокирован инспектором {inspector.full_name}"
            ),
        )
        await sleep(0.5)


@router.callback_query(F.data.startswith("user_ban_cancel_"), IsEmployee())
async def unblocking_user(callback: CallbackQuery):
    """Отмена блокировки пользователя."""
    user_id = callback.data.split("_")[-1]
    await callback.message.edit_reply_markup(reply_markup=user_ban_kb(user_id))
