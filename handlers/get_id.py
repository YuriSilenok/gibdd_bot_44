"""полуяение ид пользователя"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()


@router.message(Command("get_id"))
async def get_id_handler(message: Message):
    await message.answer(
        text=f"`{message.from_user.id}`", parse_mode=ParseMode.MARKDOWN_V2
    )
