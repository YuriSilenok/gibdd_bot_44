"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User
from filters.admin import IsAdmin
from keyboards.admin.user_info import get_user_info_kb
from database.models import Patrol

router = Router()


@router.callback_query(F.data.startswith("user_info_"), IsAdmin())
async def handle_user_info(callback: CallbackQuery):
    """Обработчик просмотра информации о пользователе"""
    user = User.get_by_id(int(callback.data.split("_")[-1]))

    await callback.message.edit_text(
        text=format_user_info(user),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user),
    )


def format_user_info(user: User) -> str:
    """Форматирует информацию о пользователе"""
    roles = [ur.role.name for ur in user.user_roles]
    
    patrolled = ''
    if 'Инспектор' in roles:
        patrolled += '\nПатрулирование: '

        is_patrol = Patrol.get_or_none(
            (Patrol.inspector == user) & (Patrol.end.is_null())
        )

        patrolled += 'Да' if is_patrol else 'Нет'

    return (
        "<b>Информация о пользователе:</b>\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username or 'не указан'}\n"
        f"Имя: {user.first_name or 'не указано'}\n"
        f"Фамилия: {user.last_name or 'не указана'}\n"
        f"Роли: {', '.join(roles) or 'нет'}"
        f"{patrolled}"
    )
