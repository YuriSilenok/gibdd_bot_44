"""Обработка команды start"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from database.models import Role, User, UserRole
from keyboards.common import get_kb_by_user


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    """Обработчик команды start"""
    user: User = User.get_or_none(tg_id=message.from_user.id)
    if user is None:
        user = User.create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            last_name=message.from_user.last_name,
            first_name=message.from_user.first_name,
        )

    elif (
        User.username != message.from_user.username
        or User.last_name != message.from_user.last_name
        or User.first_name != message.from_user.first_name
    ):
        user.username = message.from_user.username
        user.last_name = message.from_user.last_name
        user.first_name = message.from_user.first_name
        user.save()

    UserRole.get_or_create(
        user=user,
        role=Role.get(name="Очевидец"),
    )

    await message.answer(
        text="❗️Уважаемые участники дорожного движения!\n"
        "🚓Госавтоинспекция Костромской области информирует, что для "
        "предупреждения ДТП с участием нетрезвых водителей создан  чат-бот "
        "gibdd_bot_44📲\n 👉С его помощью можно анонимно сообщать о водителях "
        "с признаками опьянения, которые управляют транспортом.\n"
        "⛔️В сообщении необходимо указать информацию об автомобиле "
        "(номер, марка, цвет, направление движения), "
        "также можешь оставить геопозицию, прикрепить фото или видео.\n"
        "❗️Внимание вся поступившая информация обрабатывается роботом",
        reply_markup=get_kb_by_user(user=user),
    )
