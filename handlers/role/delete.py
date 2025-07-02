"""Обработчик удаления ролей пользователя"""

from typing import List
from aiogram import Router, F
from aiogram.types import CallbackQuery
from controller.user_info import send_message
from database.models import User, UserRole, Role
from filters.permition import IsPermition

router = Router()


@router.callback_query(
    F.data.startswith(f"delete_role_{Role.get(name='Администратор').id}_"),
    IsPermition("Удалить роль администратора"),
)
@router.callback_query(
    F.data.startswith(f"delete_role_{Role.get(name='Инспектор').id}_"),
    IsPermition("Удалить роль инспектора"),
)
async def handle_role_deletion(callback: CallbackQuery):
    """Обрабатывает удаление роли пользователя"""

    parts: List[str] = callback.data.split(sep="_")

    user_role_id = int(parts[-1])

    user_role: UserRole = UserRole.get_or_none(id=user_role_id)

    if user_role:
        await callback.message.answer(
            text=f"Роль {user_role.role.name} удалена"
        )
        user_role.delete_instance()
        await send_message(
            bot=callback.bot,
            chat_id=callback.from_user.id,
            from_user=user_role.user,
            by_user=User.get(tg_id=callback.from_user.id),
        )
    else:
        await callback.message.answer(text="Роль уже была удалена ранее")
        await callback.message.edit_reply_markup(reply_markup=None)
