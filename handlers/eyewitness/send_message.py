"""Пересылка сообщения от пользователя инспекторам"""

from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, ContentType
from filters.user import IsUser
from handlers.eyewitness.logic import (save_user_message,
                                       send_message_to_employees
                                       )
from keyboards.eyewitness import KB as eyewitness_kb
from database.models import User


router = Router()


async def check_user_ban(user_id: int, bot: Bot, chat_id: int) -> bool:
    """Проверить, забанен ли пользователь"""
    user = User.get(User.tg_id == user_id)
    if user.is_ban and user.ban_until and user.ban_until > datetime.now():
        ban_until_str = user.ban_until.strftime("%d-%m-%Y %H:%M")
        await bot.send_message(
            chat_id=chat_id,
            text=(f"Вы не можете писать до срока окончания бана,"
                  f" напишите снова после {ban_until_str}"
                  )
        )
        return True
    return False


@router.message(F.text, ~F.text.startswith("/"), IsUser())
async def get_message_from_user(message: Message) -> None:
    """Обработчик сообщения от пользователя"""
    if await check_user_ban(message.from_user.id,
                            message.bot, message.chat.id
                            ):
        return

    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.ANIMATION, IsUser())
async def get_animation_from_user(message: Message) -> None:
    """Обработчик видео от пользователя"""
    if await check_user_ban(message.from_user.id,
                            message.bot, message.chat.id
                            ):
        return

    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.VIDEO, IsUser())
async def get_video_from_user(message: Message) -> None:
    """Обработчик видео от пользователя"""
    if await check_user_ban(message.from_user.id,
                            message.bot, message.chat.id
                            ):
        return

    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.PHOTO, IsUser())
async def get_photo_from_user(message: Message) -> None:
    """Обработчик фотографий от пользователя"""
    if await check_user_ban(message.from_user.id,
                            message.bot, message.chat.id
                            ):
        return

    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.LOCATION, IsUser())
async def get_location_from_user(message: Message) -> None:
    """Обработчик локации от пользователя"""
    if await check_user_ban(message.from_user.id,
                            message.bot, message.chat.id
                            ):
        return

    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


async def answer(message: Message):
    """Стандартный ответ длч очевидца"""

    await message.answer(
        text="Спасибо за обращение. "
        "Мы его уже передали инспекторам. "
        "Вы можете отправить фотографии или видео с места происшествия. "
        "Если хотите отправить геолокацию, нажмите кнопку ниже: "
        "<b>Отправить геолокацию</b>",
        reply_markup=eyewitness_kb,
        parse_mode="HTML",
    )
