"""Обработчик информации о пользователе"""

from typing import List
from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import User, Patrol
from filters.admin import IsAdmin
from keyboards.admin.user_info import get_user_info_kb

router = Router()


@router.callback_query(F.data.startswith("user_info_"), IsAdmin())
async def handle_user_info(callback: CallbackQuery) -> None:
    """Обработчик просмотра информации о пользователе"""

    user_id = int(callback.data.split(sep="_")[-1])
    user: User = User.get_by_id(pk=user_id)

    await callback.message.edit_text(
        text=format_user_info(user=user),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user=user),
    )


def format_user_info(user: User) -> str:
    """Форматирует информацию о пользователе"""

    roles: List = [ur.role.name for ur in user.user_roles]

    username = f"@{user.username}" if user.username else None

    info_lines: List[str] = [
        "<b>Информация о пользователе:</b>",
        f"ID: {user.tg_id}",
        f"Username: {username or 'не указан'}",
        f"Имя: {user.first_name or 'не указано'}",
        f"Фамилия: {user.last_name or 'не указана'}",
        f"Роли: {', '.join(roles) or 'нет'}",
    ]

    is_inspector: bool = "Инспектор" in roles

    if is_inspector:
        is_on_patrol: bool = (
            Patrol.select()
            .where((Patrol.inspector == user) & (Patrol.end.is_null()))
            .exists()
        )
        info_lines.append(f"Патрулирование: {'Да' if is_on_patrol else 'Нет'}")

    return "\n".join(info_lines)
