"""Обработчик удаления ролей пользователя"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole, Role
from filters.admin import IsAdmin
from filters.chief import IsChief
from handlers.admin.user_info import handle_user_info

router = Router()


@router.callback_query(F.data.startswith("delete_role_"),
                       IsAdmin() | IsChief())
async def handle_role_deletion(callback: CallbackQuery):
    """Обрабатывает удаление роли пользователя"""
    parts = callback.data.split("_")
    if len(parts) < 3:
        print("Неверный формат callback_data")
        return

    role_id = int(parts[-2])
    user_id = int(parts[-1])
    current_user = User.get(tg_id=callback.from_user.id)

    role = Role.get_by_id(role_id)
    user = User.get_by_id(user_id)

    is_chief = UserRole.get_or_none(user=current_user, role=IsChief.role)
    if not is_chief and role.name == "Администратор":
        await callback.message.answer("У вас недостаточно прав")
        return

    deleted_count = (
        UserRole.delete()
        .where((UserRole.user == user) & (UserRole.role == role))
        .execute()
    )

    if deleted_count > 0:
        await callback.message.answer(f"Роль {role.name} удалена")
        await handle_user_info(callback)
    else:
        await callback.message.answer(f"Роль {role.name}"
                                      f" уже была удалена ранее")
