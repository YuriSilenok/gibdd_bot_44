"""Обработчик незарегистрированных действий"""

from aiogram import Router
from aiogram.types import CallbackQuery

from utils import callback_answer

router = Router()


@router.callback_query()
async def other_handler(callback: CallbackQuery) -> None:
    """Отвечает пушем"""
    await callback_answer(
        callback=callback,
        text=f"У Вас нет привилегий совершать это действие {callback.data}",
    )
