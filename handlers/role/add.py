"""Добавление ролей"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.types.contact import Contact
from aiogram.fsm.context import FSMContext
from controller.role import add_role
from filters.permition import IsPermition
from states.admin.inspector import AddInspector
from states.admin.admin import AddAdmin
from database.models import Admin, Role

router = Router()


@router.message(
    F.text == "Добавить администратора", IsPermition("Добавить администратора")
)
async def add_admin_start(message: Message, state: FSMContext) -> None:
    """Обработчик начала добавления администратора"""

    await message.answer(text="Отправьте контакт сотрудника")
    await state.set_state(state=AddAdmin.get_contact)


@router.message(
    F.contact, IsPermition("Добавить администратора"), AddAdmin.get_contact
)
async def get_admin_contact(message: Message, state: FSMContext):
    """Обработчик получения контакта администратора"""

    contact: Contact = message.contact
    _, user_role_is_added, user = add_role(
        contact=contact,
        role=Role.get(name="Администратор"),
    )

    if user is None:
        await message.answer(
            text="Пользователь с таким контактом не запускал бота"
        )
        return

    if not user_role_is_added:
        await message.answer(
            text="Этому сотруднику уже выдавалась роль администратора"
        )
    else:
        Admin.get_or_create(user=user)
        await message.answer(text="Роль администратора добавлена")
    await state.clear()


@router.message(
    F.text == "Добавить инспектора", IsPermition("Добавить инспектора")
)
async def add_inspector_start(message: Message, state: FSMContext):
    """Обработчик начала добавления инспектора"""

    await message.answer(text="Отправьте контакт сотрудника")
    await state.set_state(state=AddInspector.get_contact)


@router.message(
    F.contact, IsPermition("Добавить инспектора"), AddInspector.get_contact
)
async def get_inspector_contact(message: Message, state: FSMContext):
    """Обработчик получения контакта инспектора"""

    contact: Contact = message.contact
    _, user_role_is_added, user = add_role(
        contact=contact,
        role=Role.get(name="Инспектор"),
    )

    if user is None:
        await message.answer(
            text="Пользователь с таким контактом не запускал бота"
        )
        return

    if not user_role_is_added:
        await message.answer(
            text="Этому сотруднику уже выдавалась роль инспектора"
        )
    else:
        await message.answer(text="Роль инспектора добавлена")

    await state.clear()
