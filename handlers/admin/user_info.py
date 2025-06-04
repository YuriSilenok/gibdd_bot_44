"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User
from filters.admin import IsAdmin
from keyboards.admin.user_info import get_user_info_kb

router = Router()


@router.callback_query(F.data.startswith("user_info_"), IsAdmin())
async def handle_user_info(callback: CallbackQuery):
    """Обрабатывает запрос на просмотр информации о пользователе"""
    user = User.get_by_id(int(callback.data.split("_")[-1]))

    await callback.message.edit_text(
        text=_format_user_info(user),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user)
    )


def _format_user_info(user: User) -> str:
    """Форматирует информацию о пользователе"""
    roles = [user_role.role.name for user_role in user.user_roles]
    return (
        "<b>Информация о пользователе:</b>\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username or 'не указан'}\n"
        f"Имя: {user.first_name or 'не указано'}\n"
        f"Фамилия: {user.last_name or 'не указана'}\n"
        f"Роли: {', '.join(roles) or 'нет'}"
    )
