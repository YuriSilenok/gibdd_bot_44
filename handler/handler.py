from aiogram import Router
from magic_filter import F
from aiogram.types import Message
from database.models import User

# pylint: disable=no-member
router = Router(name="")


def get_inspectors():
    """Получить список всех пользователей с ролью 'inspector'."""
    inspectors = User.select().where(User.role == "inspector").execute()
    return [user.tg_id for user in inspectors]


@router.message(F.text & ~F.text.startswith("/"))
async def handle_user_message(message: Message):
    """Обработка сообщения пользователя"""
    await message.answer(
        "Спасибо за обращение. "
        "Мы его уже передали инспекторам."
    )

    inspectors = get_inspectors()
    for inspector_id in inspectors:
        try:
            await message.bot.send_message(
                inspector_id,
                (
                    f"Новое сообщение от пользователя "
                    f"{message.from_user.id}:\n"
                    f"{message.text}"
                ),
            )
        except Exception as error:
            print(
                f"Ошибка отправки сообщения инспектору {inspector_id}: "
                f"{error}"
            )


def add_routers(dp):
    """Добавить маршруты в диспетчер."""
    dp.include_router(router)
