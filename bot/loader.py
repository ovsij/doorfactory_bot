from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from dotenv import load_dotenv
import os

load_dotenv()


bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    search = State()
    city = State()
    new_message = State()
    add_admin = State()
    changepicture = State()
    add_news = State()