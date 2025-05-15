from aiogram import Router, F
from aiogram.types import Message
from database.models import User

router = Router()

""" Получаем список chat_id инспекторов из базы данных """
def get_inspectors():
    return [user.tg_id for user in User.select().where(User.role == "inspector")]

@router.message(F.text & ~F.text.startswith('/'))
async def handle_user_message(message: Message, bot):
    """ Ответ пользователю """
    await message.answer("Спасибо за обращение. Мы его уже передали инспекторам.")

    """ Получаем список инспекторов """
    inspectors = get_inspectors()

    """ Пересылаем сообщение всем инспекторам """
    for inspector_id in inspectors:
        try:
            await bot.send_message(
                inspector_id,
                f"Новое сообщение от пользователя {message.from_user.id}:\n{message.text}"
            )
        except Exception as e:
            print(f"Ошибка отправки сообщения инспектору {inspector_id}: {e}")

def add_routers(dp):
    dp.include_router(router)
