from typing import List
from aiogram import Bot

from database.models import Patrol, User
from keyboards.admin.user_info import get_user_info_kb


async def send_message(bot: Bot, chat_id: int, from_user: User, by_user: User):
    await bot.send_message(
        chat_id=chat_id,
        text=get_format_info(user=from_user),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(
            from_user=from_user,
            by_user=by_user,
        ),
    )


def get_format_info(user: User) -> str:
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
