import asyncio
import functools
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramNetworkError


def telegram_network_error(func):
    """Декоратор для сбоев сети интернет"""

    @functools.wraps(func)
    async def wrapper(*args, **qwargs):
        for delay in range(1, 10):
            try:
                return await func(*args, **qwargs)
            except TelegramNetworkError as ex:
                print(str(ex))
                await asyncio.sleep(delay=delay)

    return wrapper


@telegram_network_error
async def message_answer(
    message: Message, text, reply_markup=None, parse_mode=None
):
    await message.answer(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


@telegram_network_error
async def callback_answer(callback: CallbackQuery, text):
    await callback.answer(text=text)


@telegram_network_error
async def message_edit_reply_markup(message: Message, reply_markup=None):
    await message.edit_reply_markup(reply_markup=reply_markup)


@telegram_network_error
async def message_delete(message: Message):
    await message.delete()


@telegram_network_error
async def bot_delete_message(bot: Bot, chat_id, message_id):
    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id,
    )


@telegram_network_error
async def bot_send_message(bot: Bot, chat_id, text):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )
