from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but1 = KeyboardButton(text='Добавить инспектора')
but2 = KeyboardButton(text='Показать инспекторов')
but3 = KeyboardButton(text='Добавить администратора')
but4 = KeyboardButton(text='Показать администраторов')

ADMIN_START_KEYBOARD = ReplyKeyboardMarkup().row(but1, but2).row(but3, but4)
