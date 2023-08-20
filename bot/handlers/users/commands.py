from aiogram import types

from loader import bot, dp, Form
from bot.keyboards.inline import *

from database.crud import *
from database.models import *

@dp.message_handler(commands=['menu'])
@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    register_user(message.from_user)
    text, reply_markup = inline_kb_menu(tg_id=message.from_user.id)

    await bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=reply_markup
    )

@dp.message_handler(commands=['catalog'])
async def bot_start(message: types.Message):
    text, reply_markup = inline_kb_catalog()

    await bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=reply_markup
    )

@dp.message_handler(commands=['stores'])
async def bot_start(message: types.Message):
    await Form.city.set()
    reply_markup = InlineConstructor.create_kb([['Отмена','deny']], [1])
    await bot.send_message(
        message.from_user.id,
        text='Введите Ваш город:',
        reply_markup=reply_markup
    )