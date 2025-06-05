"""Показ информации"""

from aiogram import Router, F
from aiogram.types import Message
from filters.inspector import IsInspector
from database.models import User, Patrol

router = Router()


@router.message(F.text == "\U0001F6A8", IsInspector())
async def end_patrl(message: Message):
    """Обработчик кнопки отображения информации"""
    inspector = User.get_or_none(User.tg_id == message.from_user.id)

    is_patrol = Patrol.get_or_none(
        (Patrol.inspector == inspector) & (Patrol.end.is_null())
    )

    if inspector:
        await message.answer(
            f"Имя: <b>{inspector.username}</b>\n"
            f"Статус: <b>инспектор</b>\n"
            f"Патрулирование:<b>{'Да' 
                if is_patrol 
                else 'Нет'
            }</b>",
            parse_mode="HTML"
        )
    return