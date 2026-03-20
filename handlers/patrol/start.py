"""Начало патруля"""

from aiogram import Router, F
from aiogram.types import Message
from database.models import Patrol, User
from filters.permition import IsPermition
from keyboards.common import get_kb_by_user
from controller.patrol import get_patrol
from utils import message_answer


router = Router()


@router.message(
    F.text == "Начать патрулирование",
    IsPermition("Начать патрулирование"),
)
async def start_patrol(message: Message) -> None:
    """Обработчик кнопки начала патруля"""

    inspector: User = User.get(tg_id=message.from_user.id)
    patrol: Patrol = get_patrol(inspector=inspector)

    if patrol:
        await message_answer(
            message=message,
            text="Вы уже в патруле",
            reply_markup=get_kb_by_user(user=inspector),
        )
    else:
        Patrol.create(inspector=inspector)
        await message_answer(
            message=message,
            text="Патрулирование начато, "
            "теперь Вы будете получать сообщения от граждан",
            reply_markup=get_kb_by_user(user=inspector),
        )
