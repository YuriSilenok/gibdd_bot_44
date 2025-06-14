"""Обработчик удаления ролей пользователя"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, UserRole, Role
from filters.admin import IsAdmin
from filters.chief import IsChief

router = Router()


class IsAdminOrChief:
    """Комбинированный фильтр для проверки ролей"""

    async def __call__(self, callback: CallbackQuery) -> bool:
        is_admin = await IsAdmin().check(callback.from_user.id)
        is_chief = await IsChief().check(callback.from_user.id)
        return is_admin or is_chief


@router.callback_query(F.data.startswith("delete_role_"), IsAdminOrChief())
async def handle_role_deletion(callback: CallbackQuery):
    """Обработчик удаления роли пользователя"""
    parts = callback.data.split("_")
    role_id, user_id = int(parts[-2]), int(parts[-1])

    current_user = User.get(tg_id=callback.from_user.id)
    target_user = User.get_by_id(user_id)
    role = Role.get_by_id(role_id)

    is_chief = UserRole.select().where(
        (UserRole.user == current_user)
        & (UserRole.role == IsChief.role)
    ).exists()

    if not is_chief and role.name == "Администратор":
        await callback.answer("Недостаточно прав для удаления администратора")
        return

    deleted_count = UserRole.delete().where(
        (UserRole.user == target_user)
        & (UserRole.role == role)
    ).execute()

    if deleted_count > 0:
        await callback.answer(f"Роль {role.name} удалена")
    else:
        await callback.answer("Роль уже была удалена")
