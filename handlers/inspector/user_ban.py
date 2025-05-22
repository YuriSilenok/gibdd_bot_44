"""Забинить пользователя"""
from aiogram import exceptions

from aiogram import Router, F
from aiogram.types import CallbackQuery

from filters.inspector import IsInspector
from filters.admin import IsAdmin
from keyboards.inspector import user_ban_cobfirm_and_cancel_kb
from database.models import Message, User, UserRole


router = Router()


@router.callback_query(F.data.startswith("ban_"), IsInspector())
async def show_inspectors(callback: CallbackQuery):
    """Подтверждение блокирования пользователя."""
    user_id = callback.data.split("_")[1]
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_cobfirm_and_cancel_kb(user_id)
    )


@router.callback_query(F.data.startswith("user_ban_confirm_"), IsInspector())
async def blocking_user(callback: CallbackQuery):
    """Блокировка пользователя."""
    user_id = callback.data.split("_")[3]
    inspector = User.get_or_none(User.tg_id == callback.from_user.id)
    user_to_block = User.get_or_none(User.tg_id == user_id)

    if user_to_block is None:
        await callback.answer("Пользователь не найден.")
        return

    message_list = list(
        Message.select().where(Message.user == user_to_block)
    )

    full_name_inspector = (
        f"{inspector.first_name or ''} "
        f"{inspector.last_name or ''}"
    ).strip()
    full_name_user = (
        f"{user_to_block.first_name or ''} "
        f"{user_to_block.last_name or ''}"
    ).strip()
    admins = User.select().join(UserRole).where(UserRole.role == IsAdmin.role)

    for message in message_list:
        try:
            await callback.bot.delete_message(
                    chat_id=message.user.tg_id,
                    message_id=message.tg_message_id
                )
            message.delete_instance()
        except exceptions.TelegramBadRequest:
            pass

    user_to_block.is_ban = True
    user_to_block.save()

    for admin in admins:
        await callback.bot.send_message(
            chat_id=admin.tg_id,
            text=(
                f"Пользователь {full_name_user} "
                f"заблокирован инспектором {full_name_inspector}"
            )
        )


@router.callback_query(F.data.startswith("user_ban_cancel"), IsInspector())
async def unblocking_user(callback: CallbackQuery):
    """Отмена блокировки пользователя."""
    await callback.message.edit_reply_markup(reply_markup=None)
