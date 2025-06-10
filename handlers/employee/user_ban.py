"""Забанить пользователя"""

from typing import List
from datetime import datetime, timedelta
from aiogram import exceptions
from aiogram import Router, F
from aiogram.types import CallbackQuery
from filters import IsEmployee, IsAdmin
from keyboards.employee import user_ban_cobfirm_and_cancel_kb, user_ban_kb
from database.models import UserMessage, ForwardMessage, User, UserRole

router = Router()


async def is_staff(user: User) -> bool:
    """Проверяет, является ли пользователь сотрудником."""
    return UserRole.select().where(UserRole.user == user).exists()


@router.callback_query(F.data.startswith("ban_"), IsEmployee())
async def show_inspectors(callback: CallbackQuery) -> None:
    """Подтверждение блокирования пользователя."""
    try:
        user_id: str = callback.data.split("_")[-1]
        user_to_block = User.get_by_id(user_id)

        if not user_to_block:
            await callback.answer("Пользователь не найден")
            await callback.message.edit_reply_markup(reply_markup=None)
            return

        if await is_staff(user_to_block):
            await callback.answer("Вы не можете забанить другого сотрудника")
            await callback.message.edit_reply_markup(reply_markup=None)
            return

        await callback.message.edit_reply_markup(
            reply_markup=user_ban_cobfirm_and_cancel_kb(user_id=user_id)
        )
    except Exception as e:
        print(f"Ошибка в show_inspectors: {e}")


@router.callback_query(F.data.startswith("user_ban_confirm_"), IsEmployee())
async def blocking_user(callback: CallbackQuery) -> None:
    """Блокировка пользователя."""
    try:
        user_id: str = callback.data.split(sep="_")[-1]
        user_to_block = User.get_by_id(user_id)

        if not user_to_block:
            await callback.answer("Пользователь не найден")
            await callback.message.edit_reply_markup(reply_markup=None)
            return

        if await is_staff(user_to_block):
            await callback.answer("Вы не можете забанить другого сотрудника")
            await callback.message.edit_reply_markup(reply_markup=None)
            return

        if user_to_block.is_ban and user_to_block.ban_until > datetime.now():
            await callback.answer(text="Пользователь уже заблокирован.")
            await callback.message.delete()
            return

        ban_duration = timedelta(days=30 if user_to_block.ban_count > 0 else 1)
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

        if not await IsAdmin().check(callback):
            admins: List[User] = list(
                User.select().join(UserRole)
                .where(UserRole.role == IsAdmin.role)
            )

            admin_message = (
                f"Пользователь {user_to_block.full_name} заблокирован\n"
                f"Заблокировал: {callback.from_user.full_name}\n"
                f"Бан до: {ban_until_str}"
            )

            message_to_forward = None
            if callback.message.reply_to_message:
                user_message = UserMessage.get_or_none(
                    from_user=user_to_block,
                    text=(callback.message.reply_to_message.text or
                          callback.message.reply_to_message.caption)
                )

                if user_message:
                    if user_message.type.name == "location":
                        for location in user_message.location:
                            admin_message += (f"\n\nЛокация: "
                                              f"широта: {location.latitude}, "
                                              f"долгота: {location.longitude}")
                    else:
                        message_to_forward = (callback.message.
                                              reply_to_message.message_id)

            for admin in admins:
                try:
                    await callback.bot.send_message(
                        chat_id=admin.tg_id,
                        text=admin_message
                    )
                    if message_to_forward:
                        await callback.bot.forward_message(
                            chat_id=admin.tg_id,
                            from_chat_id=callback.message.chat.id,
                            message_id=message_to_forward
                        )
                except exceptions.TelegramBadRequest as e:
                    print(f"Ошибка при отправке сообщения администратору"
                          f"{admin.tg_id}: {e}")

        await callback.answer(text="Пользователь заблокирован.")
        await callback.message.delete()

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
