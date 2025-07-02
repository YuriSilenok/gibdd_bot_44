"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from controller.user_info import send_message
from database.models import User
from filters.permition import IsPermition

router = Router()


@router.callback_query(
    F.data.startswith("user_info_"),
    IsPermition("Показать информацию о пользователе"),
)
async def handle_user_info(callback: CallbackQuery) -> None:
    """Обработчик просмотра информации о пользователе"""

    user_id = int(callback.data.split(sep="_")[-1])
    user: User = User.get_by_id(pk=user_id)

    await send_message(
        bot=callback.bot,
        chat_id=callback.from_user.id,
        from_user=user,
        by_user=User.get(tg_id=callback.from_user.id),
    )
