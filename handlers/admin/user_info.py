"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole, Role, Admin
from filters.admin import IsAdmin
from keyboards.admin.user_info import get_user_info_kb

router = Router()


@router.callback_query(F.data.startswith("user_info_"), IsAdmin(),)
async def handle_user_info(callback: CallbackQuery):
    """Обработчик информации о пользователе"""
    user = User.get_by_id(int(callback.data.split("_")[-1]))
    user_roles = list(UserRole.select().where(UserRole.user == user))
    roles = {ur.role.name for ur in user_roles}

    await callback.message.edit_text(
        text=format_user_info(user, roles),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user, roles)
    )


def format_user_info(user: User, roles: set):
    """Форматирует информацию о пользователе"""
    return (
        "<b>Информация о пользователе:</b>\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username or 'нет'}\n"
        f"Имя: {user.first_name or 'не указано'}\n"
        f"Фамилия: {user.last_name or 'не указано'}\n"
        f"Роли: {', '.join(roles) or 'нет'}"
    )


@router.callback_query(F.data.startswith("delete_role_"), IsAdmin(),)
async def handle_role_removal(callback: CallbackQuery):
    """Удаление ролей пользователя"""
    role_id, user_id = map(int, callback.data.split("_")[2:])
    role = Role.get_by_id(role_id)
    user = User.get_by_id(user_id)

    UserRole.delete().where(
        (UserRole.user == user) & (UserRole.role == role)
    ).execute()

    if role.name == "Администратор":
        Admin.delete().where(Admin.user == user).execute()

    await callback.answer(f"Роль {role.name} удалена")
    await handle_user_info(callback)
