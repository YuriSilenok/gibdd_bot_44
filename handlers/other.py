from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query()
async def other_handler(callback: CallbackQuery) -> None:
    """Отвечает пушем"""
    await callback.answer(
        text=f"У Вас нет привилегий совершать это действие {callback.data}"
    )
