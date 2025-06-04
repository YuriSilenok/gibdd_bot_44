"""Список инспекторов"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters.admin import IsAdmin
from filters.inspector import IsInspector
from keyboards.admin.admin import get_kb_by_show_employees

router = Router()


@router.message(F.text == "Показать инспекторов", IsAdmin())
async def show_inspectors(message: Message):
    """Отображает список инспекторов администратору."""

    await message.answer(
        "<b>Список инспекторов:</b>",
        parse_mode="HTML",
        reply_markup=get_kb_by_show_employees(
            role=IsInspector.role,
            page=1
        ),
    )


@router.callback_query(F.data.startswith("users_page_"), IsAdmin())
async def go_to_page_handler(callback: CallbackQuery):
    """Обрабатывает переход по страницам инспекторов"""

    args = callback.data.split("_")
    page = int(args[-1])

    await callback.message.edit_reply_markup(
        reply_markup=get_kb_by_show_employees(
            page=page,
            role=int(args[-2]),
        ),
    )


@router.message(F.text == "Показать администраторов", IsAdmin())
async def show_admins(message: Message):
    """Отображает список администраторов администратору."""

    await message.answer(
        "<b>Список администраторов:</b>",
        parse_mode="HTML",
        reply_markup=get_kb_by_show_employees(
            role=IsAdmin.role,
            page=1
        ),
    )
