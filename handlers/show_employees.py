"""Список инспекторов"""

from typing import List
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.models import Role
from filters.permition import IsPermition
from keyboards.admin.admin import get_kb_by_show_employees
from utils import message_answer, message_edit_reply_markup, telegram_network_error

router = Router()


@router.message(
    F.text == "Показать инспекторов", IsPermition("Показать инспекторов")
)
async def show_inspectors(message: Message) -> None:
    """Отображает список инспекторов администратору."""
    await send_show_inspectors(message)


@telegram_network_error
async def send_show_inspectors(message: Message):
    await message_answer(
        text="<b>Список инспекторов:</b>",
        parse_mode="HTML",
        reply_markup=get_kb_by_show_employees(role=Role.get(name="Инспектор")),
    )


@router.callback_query(
    F.data.startswith("users_page_"), IsPermition("Показать инспекторов")
)
async def go_to_page_handler(callback: CallbackQuery) -> None:
    """Обрабатывает переход по страницам инспекторов"""

    args: List[str] = callback.data.split(sep="_")
    page = int(args[-1])
    role_id = int(args[-2])
    role: Role = Role.get_by_id(pk=role_id)
    await send_go_to_page_handler(callback, role, page)

@telegram_network_error
async def send_go_to_page_handler(callback: CallbackQuery, role, page):

    await message_edit_reply_markup(message=callback.message,
        reply_markup=get_kb_by_show_employees(
            role=role,
            page=page,
        ),
    )


@router.message(
    F.text == "Показать администраторов",
    IsPermition("Показать администраторов"),
)
async def show_admins(message: Message):
    """Отображает список администраторов администратору."""

    await message_answer(
        text="<b>Список администраторов:</b>",
        parse_mode="HTML",
        reply_markup=get_kb_by_show_employees(
            role=Role.get(name="Администратор")
        ),
    )
