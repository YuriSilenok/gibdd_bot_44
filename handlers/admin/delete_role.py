"""Обработчик удаления ролей пользователя"""

from typing import List
from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole, Role
from filters.admin import IsAdmin
from handlers.admin.user_info import handle_user_info

router = Router()


@router.callback_query(F.data.startswith("delete_role_"), IsAdmin())
async def handle_role_deletion(callback: CallbackQuery):
    """Обрабатывает удаление роли пользователя"""

    parts: List[str] = callback.data.split(sep="_")

    role_id = int(parts[-2])
    user_id = int(parts[-1])

    role: Role = Role.get_by_id(pk=role_id)
    user: User = User.get_by_id(pk=user_id)

    deleted_count: int = (
        UserRole.delete()
        .where((UserRole.user == user) & (UserRole.role == role))
        .execute()
    )

    if deleted_count > 0:
        await callback.message.answer(text=f"Роль {role.name} удалена")
        await handle_user_info(callback)
    else:
        await callback.message.answer(
            text=f"Роль {role.name} уже была удалена ранее"
        )
