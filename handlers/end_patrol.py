"""Завершение патруля"""

from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from database.models import Patrol, User
from filters.permition import IsPermition
from keyboards.common import get_kb_by_user
from controller.patrol import get_patrol


router = Router()


@router.message(
        F.text == "Закончить патрулирование",
        IsPermition("Закончить патрулирование"),
)
async def end_patrol(message: Message):
    """Обработчик кнопки завершения патруля"""

    inspector: User = User.get(tg_id=message.from_user.id)
    patrol: Patrol = get_patrol(inspector=inspector)
    if patrol:
        patrol.end = datetime.now()
        patrol.save()
        await message.answer(
            text="Патрулировнаие закончено, "
            "теперь Вы не будете получать сообщения от граждан",
            reply_markup=get_kb_by_user(user=inspector),
        )
    else:
        await message.answer(
            text="Вы уже не в патруле",
            reply_markup=get_kb_by_user(user=inspector),
        )
