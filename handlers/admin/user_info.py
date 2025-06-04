"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from database.models import User, UserRole, Role, Admin
from handlers.admin.show_employees import show_admins, show_inspectors
from filters.admin import IsAdmin
from keyboards.admin.user_info import get_user_info_kb

router = Router()


@router.callback_query(F.data.startswith("user_info_"),
                       IsAdmin(),
                       StateFilter(None)
                       )
async def handle_user_info(callback: CallbackQuery):
    """Обработчик информации о пользователе"""
    user = User.get_by_id(int(callback.data.split("_")[-1]))
    user_roles = list(UserRole.select().where(UserRole.user == user))
    roles = {ur.role.name for ur in user_roles}

    await callback.message.edit_text(
        text=format_user_info(user, roles),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user.id, roles)
    )


def format_user_info(user, roles):
    """Форматирует информацию о пользователе"""
    return (
        "<b>Информация о пользователе:</b>\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username or 'нет'}\n"
        f"Имя: {user.first_name or 'не указано'}\n"
        f"Фамилия: {user.last_name or 'не указано'}\n"
        f"Роли: {', '.join(roles) or 'нет'}"
    )


@router.callback_query(F.data.startswith("remove_role_"),
                       IsAdmin(),
                       StateFilter(None)
                       )
async def handle_role_removal(callback: CallbackQuery):
    """Удаление ролей пользователя"""
    user_id, role_key = callback.data.split("_")[2:]
    role_name = {"inspector": "Инспектор", "admin": "Администратор"}[role_key]

    (UserRole.delete()
     .where((UserRole.user == user_id) &
            (UserRole.role == Role.get(name=role_name))
            )
     .execute())

    if role_key == "admin":
        Admin.delete().where(Admin.user == user_id).execute()

    await callback.answer(f"Роль {role_name} удалена")
    await handle_user_info(callback)


@router.callback_query(F.data == "back_to_users_list",
                       IsAdmin(),
                       StateFilter(None)
                       )
async def handle_back(callback: CallbackQuery):
    """Возврат к списку пользователей"""
    message_text = callback.message.text.lower()
    await callback.message.delete()

    if 'администратор' in message_text:
        await show_admins(callback.message)
    else:
        await show_inspectors(callback.message)
