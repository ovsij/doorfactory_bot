from aiogram import types

from loader import bot, dp
from bot.keyboards.inline import *

from database.crud import *
from database.models import *

@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    register_user(message.from_user)
    text, reply_markup = inline_kb_menu()

    await bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=reply_markup
    )