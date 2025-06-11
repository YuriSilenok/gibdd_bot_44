"""Модуль управления блокировками пользователей"""

from datetime import datetime, timedelta
from aiogram import exceptions, Router, F
from aiogram.types import CallbackQuery
from database.models import UserMessage, ForwardMessage, User, UserRole
from filters import IsEmployee, IsAdmin
from keyboards.employee import user_ban_cobfirm_and_cancel_kb, user_ban_kb

router = Router()


async def is_staff(user: User) -> bool:
    """Проверка является ли пользователь сотрудником"""
    return UserRole.select().where(UserRole.user == user).exists()


async def process_ban(user: User, callback: CallbackQuery, days: int) -> str:
    """Обработка бана пользователя"""
    user.ban_until = datetime.now() + timedelta(days=days)
    user.ban_count += 1
    user.is_ban = True
    user.save()
    ban_until = user.ban_until.strftime("%d-%m-%Y %H:%M")
    await callback.bot.send_message(
        user.tg_id, f"Вы заблокированы до" f" {ban_until}"
    )
    return ban_until


async def delete_messages(callback: CallbackQuery, user: User) -> None:
    """Удаление сообщений пользователя"""
    messages = list(
        ForwardMessage.select()
        .join(UserMessage)
        .where((UserMessage.from_user == user) & (~ForwardMessage.is_delete))
    )
    for msg in messages:
        try:
            await callback.bot.delete_message(
                msg.to_user.tg_id, msg.tg_message_id
            )
        except exceptions.TelegramBadRequest:
            await callback.answer("Не удалось удалить некоторые сообщения")
    ForwardMessage.update(is_delete=True).where(
        ForwardMessage.tg_message_id.in_([m.tg_message_id for m in messages])
    )


async def notify_admins(
    callback: CallbackQuery, user: User, ban_until: str
) -> None:
    """Уведомление администраторов"""

    if UserRole.get_or_none(user=callback.from_user.id, role=IsAdmin.role):
        return

    admins = list(
        User.select().join(UserRole).where(UserRole.role == IsAdmin.role)
    )
    msg = (
        f"Пользователь {user.full_name} заблокирован\nЗаблокировал:"
        f"{callback.from_user.full_name}\nБан до: {ban_until}"
    )
    msg_id = None

    if callback.message.reply_to_message:
        user_msg = UserMessage.get_or_none(
            from_user=user,
            text=(
                callback.message.reply_to_message.text
                or callback.message.reply_to_message.caption
            ),
        )

        if user_msg and user_msg.type.name == "location":
            loc = user_msg.location[0]
            msg += (
                f"\n\nЛокация: широта: {loc.latitude},"
                f"долгота: {loc.longitude}"
            )
        else:
            msg_id = callback.message.reply_to_message.message_id

    for admin in admins:
        try:
            await callback.bot.send_message(admin.tg_id, msg)
            if msg_id:
                await callback.bot.forward_message(
                    admin.tg_id, callback.message.chat.id, msg_id
                )
        except exceptions.TelegramBadRequest:
            await callback.answer("Ошибка уведомления админа")


@router.callback_query(F.data.startswith("ban_"), IsEmployee())
async def show_confirm(callback: CallbackQuery) -> None:
    """Показать подтверждение бана"""
    try:
        user = User.get_by_id(callback.data.split("_")[-1])
        if not user:
            await callback.answer("Пользователь не найден")
            await callback.message.edit_reply_markup(reply_markup=None)
        elif await is_staff(user):
            await callback.answer("Нельзя заблокировать сотрудника")
            await callback.message.edit_reply_markup(reply_markup=None)
        else:
            await callback.message.edit_reply_markup(
                reply_markup=user_ban_cobfirm_and_cancel_kb(user_id=user.id)
            )
    except exceptions.TelegramBadRequest as e:
        await callback.answer(f"Ошибка: {str(e)}")


@router.callback_query(F.data.startswith("user_ban_confirm_"), IsEmployee())
async def confirm_ban(callback: CallbackQuery) -> None:
    """Подтверждение бана"""
    try:
        user = User.get_by_id(callback.data.split("_")[-1])
        if not user:
            await callback.answer("Пользователь не найден")
            await callback.message.edit_reply_markup(reply_markup=None)
        elif await is_staff(user):
            await callback.answer("Нельзя заблокировать сотрудника")
            await callback.message.edit_reply_markup(reply_markup=None)
        elif user.is_ban and user.ban_until > datetime.now():
            await callback.answer("Пользователь уже заблокирован")
            await callback.message.delete()
        else:
            ban_until = await process_ban(
                user, callback, 30 if user.ban_count > 0 else 1
            )
            await delete_messages(callback, user)
            await notify_admins(callback, user, ban_until)
            await callback.answer("Пользователь заблокирован")
            await callback.message.delete()
    except exceptions.TelegramBadRequest as e:
        await callback.answer(f"Ошибка: {str(e)}")


@router.callback_query(F.data.startswith("user_ban_cancel_"), IsEmployee())
async def cancel_ban(callback: CallbackQuery) -> None:
    """Отмена бана"""
    await callback.message.edit_reply_markup(
        reply_markup=user_ban_kb(user_id=callback.data.split("_")[-1])
    )
