from aiogram import types

from loader import dp, bot

from database.crud import *
from database.models import *
from keyboards.inline import *


@dp.callback_query_handler(lambda c: c.data.startswith('menu'))
async def btn_callback(callback_query: types.CallbackQuery):
    code = callback_query.data.split('_')
    print(f'User {callback_query.from_user.id} open {code}')
    # Вызов главного меню
    if code[0] == 'menu':
        text, reply_markup = inline_kb_menu()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    # Раздел "Что нового?"
    if code[0] == 'menu/whatnew':
        text, reply_markup = inline_kb_whatnew()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/whatnew/sales':
        text, reply_markup = inline_kb_sales()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/whatnew/sales/wheretobuy' or \
        code[0] == 'menu/about/production/wheretobuy' or \
        code[0] == 'menu/catalog/novelty/wheretobuy':
        text, reply_markup = inline_kb_wheretobuy()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/whatnew/news':
        text, reply_markup = inline_kb_news()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=types.ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=types.ParseMode.MARKDOWN_V2, 
                disable_web_page_preview=True
            )
    
    if code[0] == 'menu/whatnew/webinars':
        text, reply_markup = inline_kb_webinars()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )

    # Раздел "О фабрике"
    if code[0] == 'menu/about':
        text, reply_markup = inline_kb_about()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/about/production':
        text, reply_markup = inline_kb_production()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/about/call':
        text, reply_markup = inline_kb_call()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    # Раздел "Каталог"
    if code[0] == 'menu/catalog':
        text, reply_markup = inline_kb_catalog()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/catalog/novelty':
        text, reply_markup = inline_kb_novelty()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/catalog/collections':
        text, reply_markup = inline_kb_collections()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/catalog/models':
        text, reply_markup = inline_kb_models()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/catalog/covering':
        text, reply_markup = inline_kb_covering()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    
    if code[0] == 'menu/catalog/search':
        text, reply_markup = inline_kb_search()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )

    # Раздел "Задать свой вопрос"
    if code[0] == 'menu/askquestion':
        text, reply_markup = inline_kb_askquestion()
        try:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        except:
            await callback_query.message.delete()
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )