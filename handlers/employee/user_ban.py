"""Забинить пользователя"""

from typing import List
from datetime import datetime, timedelta
from aiogram import exceptions
from aiogram import Router, F
from aiogram.types import CallbackQuery
from filters import IsEmployee, IsAdmin
from keyboards.employee import user_ban_cobfirm_and_cancel_kb, user_ban_kb
from database.models import UserMessage, ForwardMessage, User, UserRole, Role

router = Router()


@router.callback_query(F.data.startswith("ban_"), IsEmployee())
async def show_inspectors(callback: CallbackQuery) -> None:
    """Подтверждение блокирования пользователя."""
    try:
        user_id: str = callback.data.split("_")[-1]
        user_to_block = User.get_or_none(User.tg_id == user_id)
        if not user_to_block:
            await callback.answer("Пользователь не найден")
            return

        await callback.message.edit_reply_markup(
            reply_markup=user_ban_cobfirm_and_cancel_kb(user_id=user_id)
        )
    except Exception as e:
        print(f"Ошибка в show_inspectors: {e}")
        await callback.answer("Произошла ошибка")


@router.callback_query(F.data.startswith("user_ban_confirm_"), IsEmployee())
async def blocking_user(callback: CallbackQuery) -> None:
    """Блокировка пользователя."""
    try:
        user_id: str = callback.data.split(sep="_")[-1]
        user_to_block = User.get_or_none(User.tg_id == user_id)
        if not user_to_block:
            await callback.answer("Пользователь не найден")
            return

        inspector = User.get_or_none(User.tg_id == callback.from_user.id)
        if not inspector:
            await callback.answer("Ошибка: инспектор не найден")
            return

        if user_to_block.is_ban and user_to_block.ban_until > datetime.now():
            await callback.answer(text="Пользователь уже заблокирован.")
            return

        ban_duration = (timedelta(days=30)
                        if user_to_block.ban_count > 0 else timedelta(days=1))
        user_to_block.ban_until = datetime.now() + ban_duration
        user_to_block.ban_count += 1
        user_to_block.is_ban = True
        user_to_block.save()

        ban_until_str = user_to_block.ban_until.strftime("%d-%m-%Y %H:%M")
        await callback.bot.send_message(
            chat_id=user_to_block.tg_id,
            text=f"Вы получили бан до {ban_until_str}"
        )

        user_ban_messages: List[ForwardMessage] = list(
            ForwardMessage.select()
            .join(UserMessage)
            .where(
                (UserMessage.from_user == user_to_block)
                & (~ForwardMessage.is_delete)
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
            ForwardMessage.tg_message_id.in_([msg.tg_message_id
                                              for msg in user_ban_messages])
        ).execute()

        admins: List[User] = list(
            User.select().join(UserRole).where(UserRole.role == IsAdmin.role)
        )

        user_roles = (Role.select().join(UserRole)
                      .where(UserRole.user == user_to_block))
        roles_str = ", ".join([role.name for role in user_roles])

        admin_message = (
            f"Пользователь {user_to_block.full_name} заблокирован\n"
            f"Роли: {roles_str}\n"
            f"Заблокировал: {inspector.full_name}"
        )

        if callback.message.reply_to_message:
            original_msg = callback.message.reply_to_message
            if original_msg.text:
                admin_message += f"\n\nСообщение: {original_msg.text}"
            elif original_msg.caption:
                admin_message += f"\n\nПодпись: {original_msg.caption}"

        for admin in admins:
            try:
                await callback.bot.send_message(
                    chat_id=admin.tg_id,
                    text=admin_message
                )

                if callback.message.reply_to_message:
                    await callback.bot.forward_message(
                        chat_id=admin.tg_id,
                        from_chat_id=callback.message.chat.id,
                        message_id=callback.message.reply_to_message.message_id
                    )
            except exceptions.TelegramBadRequest as e:
                print(f"Ошибка при отправке сообщения администратору"
                      f" {admin.tg_id}: {e}"
                      )

        await callback.answer(text="Пользователь заблокирован.")

    except Exception as e:
        print(f"Ошибка в blocking_user: {e}")
        await callback.answer("Произошла ошибка при блокировке")


@router.callback_query(F.data.startswith("user_ban_cancel_"), IsEmployee())
async def unblocking_user(callback: CallbackQuery) -> None:
    """Отмена блокировки пользователя."""
    user_id: str = callback.data.split(sep="_")[-1]
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_kb(user_id=user_id)
    )
