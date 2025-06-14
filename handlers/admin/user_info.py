"""Обработчик информации о пользователе"""

from aiogram import Router, F
from aiogram.types import (CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from database.models import User, Patrol, UserRole
from filters.admin import IsAdmin
from filters.chief import IsChief

router = Router()


class AdminOrChiefFilter:
    """Фильтр для проверки роли Администратор или Начальник"""

    def __init__(self):
        self.admin_filter = IsAdmin()
        self.chief_filter = IsChief()

    async def __call__(self, callback: CallbackQuery) -> bool:
        """Является ли пользователь администратором или начальником"""
        is_admin = await self.admin_filter(callback)
        is_chief = await self.chief_filter(callback)
        return is_admin or is_chief


def format_user_info(user: User) -> str:
    """Форматирует информацию о пользователе"""
    roles = [ur.role.name for ur in user.user_roles]
    info = [
        "<b>Информация о пользователе:</b>",
        f"ID: {user.tg_id}",
        f"Username: @{user.username or 'не указан'}",
        f"Имя: {user.first_name or 'не указано'}",
        f"Фамилия: {user.last_name or 'не указана'}",
        f"Роли: {', '.join(roles) or 'нет'}"
    ]

    if "Инспектор" in roles:
        on_patrol = Patrol.select().where(
            (Patrol.inspector == user)
            & (Patrol.end.is_null())
        ).exists()
        info.append(f"Патрулирование: {'Да' if on_patrol else 'Нет'}")

    return "\n".join(info)


def get_user_info_kb(user: User, current_user: User) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру управления ролями"""
    buttons = []
    current_is_chief = UserRole.select().where(
        (UserRole.user == current_user)
        & (UserRole.role == IsChief.role)
    ).exists()

    for user_role in user.user_roles:
        if current_is_chief and user_role.role.name in ["Администратор",
                                                        "Инспектор"]:
            buttons.append([InlineKeyboardButton(
                text=f"Удалить {user_role.role.name.lower()}",
                callback_data=f"delete_role_{user_role.role.id}_{user.id}"
            )])
        elif user_role.role.name == "Инспектор":
            buttons.append([InlineKeyboardButton(
                text="Удалить инспектора",
                callback_data=f"delete_role_{user_role.role.id}_{user.id}"
            )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data.startswith("user_info_"), AdminOrChiefFilter())
async def handle_user_info(callback: CallbackQuery):
    """Обработчик просмотра информации о пользователе"""
    user = User.get_by_id(int(callback.data.split("_")[-1]))
    current_user = User.get(tg_id=callback.from_user.id)

    await callback.message.edit_text(
        text=format_user_info(user),
        parse_mode="HTML",
        reply_markup=get_user_info_kb(user, current_user)
    )
