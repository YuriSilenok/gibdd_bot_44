"""Модуль управления статусом патруля"""

from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from database.models import Patrol, User
from filters.inspector import IsInspector
from keyboards.common import get_kb_by_user


router = Router()


def get_active_patrol(inspector: User) -> Patrol | None:
    """Проверка, находится ли инспектор в патруле"""
    return Patrol.get_or_none(
        (Patrol.inspector == inspector) &
        (Patrol.end.is_null())
    )


@router.message(F.text == 'Начать патрулирование', IsInspector())
async def start_patrol(message: Message):
    """Обработчик кнопки начала патруля"""
    inspector = User.get(tg_id=message.from_user.id)
    is_patrol = get_active_patrol(inspector=inspector)
    if is_patrol:
        await message.answer("Вы уже в патруле",
                             reply_markup=get_kb_by_user(inspector),
                             )
    else:
        Patrol.create(inspector=inspector)
        await message.answer(
            "Патрулирование начато, "
            "теперь Вы будете получать сообщения от граждан",
            reply_markup=get_kb_by_user(inspector),
            )


@router.message(F.text == 'Закончить патрулирование', IsInspector())
async def end_patrol(message: Message):
    """Обработчик кнопки завершения патруля"""
    inspector = User.get(tg_id=message.from_user.id)
    is_patrol = get_active_patrol(inspector=inspector)
    if is_patrol:
        is_patrol.end = datetime.now()
        is_patrol.save()
        await message.answer(
            "Патрулировнаие закончено, "
            "теперь Вы не будете получать сообщения от граждан",
            reply_markup=get_kb_by_user(inspector)
        )
    else:
        await message.answer(
            "Вы уже не в патруле",
            reply_markup=get_kb_by_user(inspector)
        )
