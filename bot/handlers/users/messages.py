from aiogram import types
from aiogram.dispatcher import FSMContext
from fuzzywuzzy import process
import requests
from typing import List, Union

from loader import bot, dp, Form

from database.crud import *
from database.models import *
from keyboards.inline import *

# поиск по каталогу
@dp.message_handler(state=Form.search)
async def search(message: types.Message, state: FSMContext):
    await state.finish()
    collections = get_collection()
    coverings = get_covering()
    models = get_model()
    text = None
    for c in collections:
        if message.text.lower() == c.name.lower():
            collection_coverings = set([prod.covering.id for prod in get_product(collection=c.id)])
            print(collection_coverings)
            if len(collection_coverings) > 1:
                text, reply_markup = inline_kb_choose_covering(collection=c, coverings=collection_coverings)
                await bot.send_message(
                    message.from_user.id,
                    text=text,
                    reply_markup=reply_markup
                )
                return
            for cov_id in collection_coverings:
                print(get_covering(id=cov_id).name)
                text, reply_markup = inline_kb_models_by_covering_collection(page=1, collection_id=c.id, covering_id=cov_id)
                await bot.send_message(
                    message.from_user.id,
                    text=text,
                    reply_markup=reply_markup
                )
            return
    for c in coverings:
        if message.text.lower() == c.name.lower():
            text, reply_markup = inline_kb_collections_by_covering(covering_id=c.id, page=1)
    
    for m in models:
        if message.text.lower() == m.name.lower():
            model_coverings = list(set([prod.covering.id for prod in get_product(model=m.id)]))
            print(model_coverings)
            if len(model_coverings) > 1:
                text, reply_markup = inline_kb_choose_covering(model=m, coverings=model_coverings)
                await bot.send_message(
                    message.from_user.id,
                    text=text,
                    reply_markup=reply_markup
                )
                return
                
            for cov_id in model_coverings:
                model_collections = set([prod.collection.id for prod in get_product(model=m.id)])
                for collection in model_collections:
                    text, reply_markup = inline_kb_colors(page=1, collection_id=collection, covering_id=cov_id, model_id=m.id)
                    await bot.send_message(
                        message.from_user.id,
                        text=text,
                        reply_markup=reply_markup
                    )
            return
    
    if not text:
        text, reply_markup = inline_kb_nosearch(request=message.text)

    await bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=reply_markup
    )

# поиск по городу
@dp.message_handler(state=Form.city)
async def search_city(message: types.Message, state: FSMContext):
    

    await state.finish()
    cities = set([shop.city for shop in get_shop()])
    match_city = process.extractOne(message.text.lower(), cities)
    if match_city[1] > 60 and len(message.text) - len(match_city[0]) <= 3 and message.text[0].lower() == match_city[0][0].lower():
        #return match_city[0]
        shops = get_shop(city=match_city[0])
        sorted_shops = []
        for shop in shops:
            if 'фирменный' in shop.name.lower() or 'Albero' in shop.name.lower():
                sorted_shops.insert(0, shop)
            else:
                sorted_shops.append(shop)
        
        for shop in sorted_shops:
            time = f'Время работы: {shop.time}' if shop.time != 'nan' else ''
            text = markdown.text(
                shop.name,
                '',
                f'Тел.: +{shop.phone}',
                f'Адрес: {shop.city}, {shop.address}',
                time,
                'Координаты:',
                sep='\n'
            )
            
            if shop.image:
                resp = requests.get(shop.image)
                #photo = types.InputFile(resp.content)
                await bot.send_photo(
                    message.from_user.id,
                    photo=resp.content,
                    caption=text
                )
            else:
                await bot.send_message(
                    message.from_user.id,
                    text=text)
            
            await bot.send_location(
                message.from_user.id,
                latitude=shop.geocode.split(',')[0],
                longitude=shop.geocode.split(',')[1]
            )
    else:
        await bot.send_message(
            message.from_user.id,
            text='Города с таким названием не найдено')


# получаем текст сообщения для рассылки
@dp.message_handler(state=Form.new_message)
async def sendmessate_text(message: types.Message, state: FSMContext):
    text = message.text
    #Form.new_message = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=Form.prev_message.message_id)
    await message.delete()
    reply_markup = inline_sendmessage()
    Form.prev_message = await bot.send_message(
            message.from_user.id,
            text=text,
            reply_markup=reply_markup,
            )

# добавить админа
@dp.message_handler(state=Form.add_admin)
async def search(message: types.Message, state: FSMContext):
    username = message.text.strip('@')
    user = get_user(username=username)
    if not user:
        reply_markup = InlineConstructor.create_kb([['Отмена','deny']], [1])
        await bot.send_message(
            message.from_user.id,
            text='Пользователь с таким username не найден. Проверьте запускал ли пользователь бота.',
            reply_markup=reply_markup
        )
        return
    await state.finish()
    if not user.is_admin:
        update_user(tg_id=user.tg_id, is_admin=True)
        text=f'Пользователь @{username} назначен администратором'
    else:
        text=f'Пользователь @{username} уже является администратором'

    await bot.send_message(
        message.from_user.id,
        text=text
    )



@dp.message_handler(content_types=['photo'], state=Form.changepicture)
async def photo_handler(message: types.Message, state:FSMContext):
    # we are here if the first message.content_type == 'photo'
    # save the largest photo (message.photo[-1]) in FSM, and start photo_counter
    await state.update_data(photo_0=message.photo[-1], photo_counter=0)

    await state.set_state('next_photo') 

    with open('photo.txt', 'w') as file:
        file.write(message.photo[-1].file_id)
    
    reply_markup = InlineConstructor.create_kb([['Завершить','deny_nextphoto']], [1])

    await bot.send_message(
        message.from_user.id,
        text='Пришлите следующее фото или нажмите "Завершить"',
        reply_markup=reply_markup
    )


@dp.message_handler(content_types=['photo'], state='next_photo')
async def next_photo_handler(message: types.Message, state:FSMContext):
    # we are here if the second and next messages are photos
    async with state.proxy() as data:
        data['photo_counter'] += 1
        photo_counter = data['photo_counter']
        data[f'photo_{photo_counter}']=message.photo[-1]
    await state.set_state('next_photo')

    with open('photo.txt', 'r') as file:
        files = file.read()
    
    files += f'//{message.photo[-1].file_id}'

    with open('photo.txt', 'w') as file:
        file.write(files)

    if len(files.split('//')) == 3:
        await state.finish()

        media = types.MediaGroup()
        for id in files.split('//'):
            media.attach_photo(id)
        await bot.send_media_group(
            message.from_user.id, 
            media=media,
        )
        _, reply_markup = inline_kb_sales(tg_id=message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            text='Вернуться в предыдущее меню',
            reply_markup=reply_markup
        )
        return
    


# добавить новость
@dp.message_handler(state=Form.add_news)
async def add_news(message: types.Message, state: FSMContext):
    create_news(text=message.text)

    reply_markup = InlineConstructor.create_kb([['Завершить','deny_addnews']], [1])
    await bot.send_message(
        message.from_user.id,
        text='Пришлите фотографию к этой новости или нажмите "Завершить", если хотите загрузить новость без фото.',
        reply_markup=reply_markup
    )

# добавить фото к новости
@dp.message_handler(state=Form.add_news, content_types=['photo'])
async def add_news(message: types.Message, state: FSMContext):
    news = get_news(id=get_news()[0].id)

    update_news(id=get_news()[0].id, image=message.photo[-1].file_id)

    text, reply_markup, image = inline_kb_news(message.from_user.id, news.id)
    if image:
        await bot.send_photo(
            message.from_user.id, 
            photo=image, 
            caption=text,
            reply_markup=reply_markup,
        )
    else:
        
        await bot.send_message(
            message.from_user.id,
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    await state.finish()



@dp.message_handler(content_types=['video', 'document'])
async def get_video_id(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, message.video.file_id)
    except:
        pass
    try:
        await bot.send_message(message.from_user.id, message.document.file_id)
    except:
        pass


