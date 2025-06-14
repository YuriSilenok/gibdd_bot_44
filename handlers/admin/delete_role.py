"""Обработчик удаления ролей пользователя"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole, Role
from filters.admin_or_chief import AdminOrChiefFilter

router = Router()
admin_or_chief = AdminOrChiefFilter()


@router.callback_query(F.data.startswith("delete_role_"), admin_or_chief)
async def handle_role_deletion(callback: CallbackQuery):
    """Обработчик удаления роли пользователя"""
    parts = callback.data.split("_")
    role_id, user_id = int(parts[-2]), int(parts[-1])

    current_user = User.get(tg_id=callback.from_user.id)
    target_user = User.get_by_id(user_id)
    role = Role.get_by_id(role_id)

    if not admin_or_chief.check_permissions(current_user, role.name):
        await callback.answer("Недостаточно прав для удаления администратора")
        return

    deleted_count = UserRole.delete().where(
        (UserRole.user == target_user)
        & (UserRole.role == role)
    ).execute()

    await callback.answer(
        f"Роль {role.name} удалена" if deleted_count > 0
        else "Роль уже была удалена"
    )
