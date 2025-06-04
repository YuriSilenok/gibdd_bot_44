"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole
from filters.admin import IsAdmin
from keyboards.admin.user_info import get_user_info_kb

router = Router()


@router.callback_query(F.data.startswith("user_info_"), IsAdmin())
async def handle_user_info(callback: CallbackQuery):
    """Отображение информации о пользователе"""
    user = User.get_by_id(int(callback.data.split("_")[-1]))
    user_roles = list(UserRole.select().where(UserRole.user == user))
    roles = {ur.role.name for ur in user_roles}

    list_type = ("admin" if "администратор" in callback.message.text.lower()
                 else "inspector"
                 )

    await callback.message.edit_text(
        text=format_user_info(user, roles),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user, list_type)
    )


def format_user_info(user: User, roles: set):
    """Форматирование информации о пользователе"""
    return (
        "<b>Информация о пользователе:</b>\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username or 'нет'}\n"
        f"Имя: {user.first_name or 'не указано'}\n"
        f"Фамилия: {user.last_name or 'не указано'}\n"
        f"Роли: {', '.join(roles) or 'нет'}"
    )
