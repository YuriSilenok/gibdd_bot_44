"""Обработчик удаления ролей пользователя"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole, Role
from filters.admin import IsAdmin
from handlers.admin.user_info import handle_user_info

router = Router()


@router.callback_query(F.data.startswith("delete_role_"), IsAdmin())
async def handle_role_deletion(callback: CallbackQuery):
    """Обрабатывает удаление роли пользователя"""

    parts = callback.data.split('_')
    if len(parts) < 3:
        raise ValueError("Неверный формат callback_data")

    role_id = parts[-2]
    user_id = parts[-1]

    role = Role.get_by_id(int(role_id))
    user = User.get_by_id(int(user_id))

    deleted_count = UserRole.delete().where(
        (UserRole.user == user) &
        (UserRole.role == role)
    ).execute()

    if deleted_count > 0:
        await callback.message.answer(f"Роль {role.name} удалена")
        await handle_user_info(callback)
    else:
        await callback.message.answer(
            f"Роль {role.name} уже была удалена ранее"
            )
