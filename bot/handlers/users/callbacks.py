from aiogram import types
from aiogram.dispatcher import FSMContext

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
import re

from loader import dp, bot, Form

from database.crud import *
from database.models import *
from keyboards.inline import *
from keyboards.constructor import InlineConstructor


@dp.callback_query_handler(lambda c: c.data.startswith('menu'))
async def btn_callback(callback_query: types.CallbackQuery):
    code = callback_query.data
    print(f'User {callback_query.from_user.id} open {code}')
    update_user(tg_id=callback_query.from_user.id, last_usage=True)
    # Вызов главного меню
    if code == 'menu':
        text, reply_markup = inline_kb_menu(tg_id=callback_query.from_user.id)
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
    
    # Раздел "Межкомнатные двери"
    if code == 'menu/doors':
        text, reply_markup = inline_kb_doors()
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
    
    # Раздел "Межкомнатные двери" переход в коллекцию
    if re.fullmatch('menu/doors/\d*', code):
        collection_id = int(code.split('/')[-1])
        text, reply_markup = inline_kb_doorscollections(collection_id=collection_id)
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
    
    # Раздел "Межкомнатные двери" переход в модель
    if re.fullmatch('menu/doors/\d*/\d*', code):
        model_id = int(code.split('/')[-1])
        collection_id = int(code.split('/')[-2])
        model = get_model(id=model_id)
        collection = get_collection(id=collection_id)
        #print(collection.name)

        product_imgs = list(set([p.image for p in get_product(model=model_id) if os.path.exists(p.image) and str(p.width) == '800.0' and p.collection.id == collection_id]))

        if len(product_imgs) == 0:
            product_imgs = list(set([p.image for p in get_product(model=model_id) if os.path.exists(p.image) and str(p.width) == '700.0' and p.collection.id == collection_id]))
        if len(product_imgs) == 0:
            product_imgs = list(set([p.image for p in get_product(model=model_id) if os.path.exists(p.image) and str(p.width) == '600.0' and p.collection.id == collection_id]))
        if len(product_imgs) == 0:
            product_imgs = list(set([p.image for p in get_product(model=model_id) if os.path.exists(p.image) and str(p.width) == '900.0' and p.collection.id == collection_id]))
        if len(product_imgs) == 0:
            product_imgs = list(set([p.image for p in get_product(model=model_id) if os.path.exists(p.image) and str(p.width) == '400.0' and p.collection.id == collection_id]))

        path = f"database/Doors/{collection.name}/{model.name}/"
        for root, dirs, files in os.walk(path):
            for filename in sorted(files):
                if '.jpg' in filename or '.png' in filename:
                    product_imgs.append(f"{path}{filename}")
        
        path = f"database/Doors/{collection.name}/"
        for root, dirs, files_ in os.walk(path):
            for filename_ in sorted(files_):
                if '.jpg' in filename_ or '.png' in filename_:
                    product_imgs.append(f"{path}{filename_}")
            break
        
        if collection.videos:
            for vid in collection.videos.split('//'):
                product_imgs.append(vid)
        
        if len(product_imgs) % 10 > 0:
            r = len(product_imgs) // 10 + 1
        else:
            r = len(product_imgs) / 10
        #print(product_imgs)
        for i in range(int(r)):
            photo = []
            for img in product_imgs[i * 10:(i+1) * 10]:
                if img.endswith('.jpg') or img.endswith('.png'):
                    photo.append(types.InputMedia(media=open(img, 'rb')))
                else:
                    photo.append(types.InputMediaVideo(media=img))
                    
            try:
                await bot.send_media_group(
                    callback_query.message.chat.id, 
                    media=photo,
                )
            except Exception as ex:
                print(ex)
                
        
        if collection.documents:
            for doc in collection.documents.split('//'):
                await bot.send_document(callback_query.from_user.id, doc)
        
        text, reply_markup = inline_kb_doorsmodel(collection_id=collection_id, model_id=model_id)
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )

    # Раздел "Что нового?"
    if code == 'menu/whatnew':
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
    
    if code == 'menu/whatnew/sales':
        try:
            await callback_query.message.delete()
        except:
            pass

        _, reply_markup = inline_kb_sales(tg_id=callback_query.from_user.id)
        
        #photo = types.InputFile('database/sales.jpg')
        with open('photo.txt', 'r') as file:
            files = file.read().split('//')

        if len(files) == 1:    
            await bot.send_photo(
                callback_query.from_user.id, 
                photo=files[0], 
                reply_markup=reply_markup
            )
        else:
            media = types.MediaGroup()
            for id in files:
                media.attach_photo(id)
            await bot.send_media_group(
                callback_query.from_user.id, 
                media=media,
            )
            _, reply_markup = inline_kb_sales(tg_id=callback_query.from_user.id)
            await bot.send_message(
                callback_query.from_user.id,
                text='Вернуться в предыдущее меню',
                reply_markup=reply_markup
            )

    
    if code == 'menu/sales/changepicture':
        await Form.changepicture.set()
        await bot.send_message(
            callback_query.from_user.id,
            'Пришлите от 1 до 3 фотографий для этого меню'
        )


    
    if code.split('/')[-1] == 'wheretobuy':
        await Form.city.set()
        reply_markup = InlineConstructor.create_kb([['Отмена','deny']], [1])
        await bot.send_message(
            callback_query.from_user.id,
            text='Введите Ваш город:',
            reply_markup=reply_markup
        )
    
    if re.fullmatch('menu/whatnew/news/\d*', code) or re.fullmatch('menu/whatnew/news/None', code):
        if code.split('/')[-1] == 'None':
            news_index = None
        else:
            news_index = int(code.split('/')[-1])
        
        print(news_index)
        text, reply_markup, image = inline_kb_news(callback_query.from_user.id, news_index)
        if image:
            await callback_query.message.delete()
            await bot.send_photo(
                callback_query.from_user.id, 
                photo=image, 
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            try:
                await callback_query.message.edit_text(
                    text=text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
            except:
                await callback_query.message.delete()
                await bot.send_message(
                    callback_query.from_user.id,
                    text=text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )

    
    if code == 'menu/whatnew/news/add':
        reply_markup = InlineConstructor.create_kb([['Отмена','deny_addnews']], [1])
        await Form.add_news.set()
        await bot.send_message(
            callback_query.from_user.id,
            text='Пришлите текст новости:',
            reply_markup=reply_markup
        )
    if re.fullmatch('menu/whatnew/news/delete/\d*', code):
        news_index = int(code.split('/')[-1])
        all_news = [n.id for n in get_news()]
        prew_index = all_news[all_news.index(news_index) - 1] if all_news.index(news_index) != 0 else None
        delete_news(id=news_index)            

        text, reply_markup, image = inline_kb_news(callback_query.from_user.id, prew_index)
        if image:
            await callback_query.message.delete()
            await bot.send_photo(
                callback_query.from_user.id, 
                photo=image, 
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            try:
                await callback_query.message.edit_text(
                    text=text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
            except:
                await callback_query.message.delete()
                await bot.send_message(
                    callback_query.from_user.id,
                    text=text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )

    
    if code == 'menu/whatnew/webinars':
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
    if code == 'menu/about':
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
    
    if code == 'menu/about/production':
        try:
            await callback_query.message.delete()
        except:
            pass
        
        images = ['database/about1.png', 'database/about2.png']
        msg_ids = ''
        for image in images:
            photo = types.InputFile(image)
            await bot.send_photo(
                callback_query.message.chat.id, 
                photo=photo, 
            )

        text, reply_markup = inline_kb_production()
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )

    if code == 'menu/about/video':
        text, reply_markup = inline_kb_video()
        try:
            await callback_query.message.delete()
        except:
            pass
        await bot.send_video(callback_query.from_user.id, caption='Межкомнатные двери от фабрики-производителя ALBERO', video='BAACAgIAAxkBAAIeKGTniynq1CTUaI3pgjhjgoLgSOWHAALXNwACrFE5S-V6idjfI-1gMAQ')
        await bot.send_video(callback_query.from_user.id, caption='Модные межкомнатные двери. Интервью с дизайнером Мариной Семеновой', video='BAACAgIAAxkBAAIeKWTniyl2Ak021ix052x8lj8xA-CiAALYNwACrFE5S9DCWxZdSqdSMAQ')
        await bot.send_video(callback_query.from_user.id, caption='Производство дверей в эмали г. Балаково', video='BAACAgIAAxkBAAIeKmTniyliYt1uOrkXcCn3vJkPFj3rAALZNwACrFE5S0jjBeWVw8RnMAQ')

        await bot.send_message(
            callback_query.from_user.id,
            text='Вернуться в предыдущее меню',
            reply_markup=reply_markup
        )
    
    if code == 'menu/about/call':
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
    if code == 'menu/catalog':
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
    
    if code == 'menu/catalog/novelty':
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
    
    if code == 'menu/catalog/collections':
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

    # модели/продукты ко коллекциям
    #if re.fullmatch('menu/catalog/collections/\d*-\d*/', code):
    if re.fullmatch('menu/catalog/covering/\d*/\d*-\d*/', code):
        
        collection = get_collection(id=int(code.split('/')[-2].split('-')[0]))
        if int(code.split('/')[-2].split('-')[1]) == 1:
            try:
                await callback_query.message.delete()
            except:
                pass
            text = None
            if collection.name == 'Status':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/g7kMSefuJRk?si=is__sIQP-rJ7Fy0w\n\n Презентация коллекции: https://disk.yandex.ru/d/CuSYCDrjVIa4xQ'
            if collection.name == 'НеоКлассика':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/hl5xnnT1Eqk?si=bW0sE39UOxXswIty'
            if collection.name == 'Геометрия':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/ZbZRnUDHDqU?si=906sCWpQ8Gygrq5h\n\n Презентация коллекции: https://disk.yandex.ru/d/J9BRnGO36jBWTg'
            if collection.name == 'Альянс':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/1hp5ijrdLLc?si=sBIcvHLWH3FKdJga\n\nПрезентация коллекции: https://disk.yandex.ru/d/8Psy0ZA_ugH32A'
            if collection.name == 'Классика':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/S980dRQxUr8?si=-SXDQa7CBJiuRDCz\n\n Презентация коллекции: https://disk.yandex.ru/d/bPmUoch_JiMr7Q'
            if collection.name == 'Стиль':
                text=f'Коллекция {collection.name}\n\nПрезентация коллекции: https://disk.yandex.ru/d/xFFl71wcA-4kng'
            if collection.name == 'Галерея':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/IOVG-8FnZMo?si=xoFRuPaEE8VTNjM7'
            if collection.name == 'Империя':
                text=f'Коллекция {collection.name}\n\nПрезентация коллекции: https://disk.yandex.ru/d/1iD5H_ysZpP8Xg'
            if collection.name == 'Мегаполис':
                text=f'Коллекция {collection.name}\n\nВидео коллекции: https://youtu.be/ih5ZiI_MFhE?si=XquF3tOKigvV2Y4Q'
            if collection.name == 'Мегаполис Лофт':
                text=f'Коллекция {collection.name}\n\nПрезентация коллекции: https://disk.yandex.ru/d/x8T7uY1v0McxTA'
            if collection.name == 'WEST':
                text=f'Коллекция {collection.name}\n\nПрезентация коллекции: https://disk.yandex.ru/d/ZAFYQw6i1spg0Q'
            if collection.name == 'Тренд':
                text=f'Коллекция {collection.name}\n\nПрезентация коллекции: https://disk.yandex.ru/d/wTPHd9iWgpXWtQ'
            if text:
                await bot.send_message(
                    callback_query.from_user.id,
                    text=text
                )

        text, reply_markup = inline_kb_models_by_covering_collection(
            covering_id=int(code.split('/')[-3]),
            collection_id=int(code.split('/')[-2].split('-')[0]),
            page=int(code.split('/')[-2].split('-')[1])
        )
        
    
        if int(code.split('/')[-2].split('-')[1]) > 1:
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        else:
            await bot.send_message(
                callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup
            )

    # цвета покрытия для модели
    if re.fullmatch('menu/catalog/covering/\d*/\d*/\d*/', code):
        await callback_query.message.delete()
        model = get_model(id=int(code.split('/')[-2]))
        text = None
        if model.name == 'Геометрия-1' or model.name == 'Геометрия-2' or model.name == 'Геометрия-3' or model.name == 'Геометрия-4':
            text=f'Презентация модели {model.name}: https://disk.yandex.ru/i/hqBnB5NugK9-kw'
        if model.name == 'Геометрия-5' or model.name == 'Геометрия-6' or model.name == 'Геометрия-7' or model.name == 'Геометрия-8':
            text=f'Презентация модели {model.name}: https://disk.yandex.ru/i/IGQMgU2Hzdj-Uw'
        if model.name == 'Византия' or model.name == 'Спарта-2' or model.name == 'Спарта-2 с молдингом' or model.name == 'Рим' or model.name == 'Прадо':
            text=f'Презентация модели {model.name}: https://disk.yandex.ru/i/hDyhx-PmpWr6dA'
        if model.name == 'Олимпия':
            text=f'Презентация модели {model.name}: https://disk.yandex.ru/i/QjKX5K1y3gUfsw'
        if model.name == 'Афина-1' or model.name == 'Афина-2' or model.name == 'Киото':
            text=f'Презентация модели {model.name}: https://disk.yandex.ru/i/z_wB3scmvuH09Q'
        if model.name == 'Вена' or model.name == 'Сеул' or model.name == 'Дрезден' or model.name == 'Дублин' or model.name == 'Мюнхен':
            text=f'Презентация модели {model.name}: https://disk.yandex.ru/i/rxdAcUdWjcys4A'
        if text:
            await bot.send_message(
                callback_query.from_user.id,
                text=text
            )
        text, reply_markup = inline_kb_colors(covering_id=int(code.split('/')[-4]), collection_id=int(code.split('/')[-3]), model_id=int(code.split('/')[-2]))
        
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )
    
    # Типы стекла для цвета
    if re.fullmatch('menu/catalog/covering/\d*/\d*/\d*/\d*/', code):
        text, reply_markup = inline_kb_glases(covering_id=int(code.split('/')[-5]), collection_id=int(code.split('/')[-4]), model_id=int(code.split('/')[-3]), color_id=int(code.split('/')[-2]))
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

    # карточка товара 
    if re.fullmatch('menu/catalog/covering/\d*/\d*/\d*/\d*/\d*/', code):
        if 'collections' in code:
            text, reply_markup = inline_kb_model_by_collection(model_id=int(code.split('/')[-2]), collection_id=int(code.split('/')[-3]))
        elif 'covering' in code:
            text, reply_markup = inline_kb_model(covering_id=int(code.split('/')[-6]), collection_id=int(code.split('/')[-5]), model_id=int(code.split('/')[-4]), color_id=int(code.split('/')[-3]), glasstype_id=int(code.split('/')[-2]))
        print([p for p in get_product(model=int(code.split('/')[-4]), color=int(code.split('/')[-3]), glass_type=int(code.split('/')[-2]))])
        for product in [p for p in get_product(model=int(code.split('/')[-4]), color=int(code.split('/')[-3]), glass_type=int(code.split('/')[-2]))]:
            try:
                print('try')
                photo = types.InputFile(product.image)
                await bot.send_photo(
                    callback_query.message.chat.id, 
                    photo=photo, 
                )
                await bot.send_message(
                    callback_query.message.chat.id,
                    text=text,
                    reply_markup=reply_markup
                )
                return
            except Exception as ex:
                print(ex)
                pass
        
        
        
        
    
    if code == 'menu/catalog/covering':
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
    
    # коллекции в рамках покрытия
    if re.fullmatch('menu/catalog/covering/\d*-\d*/', code):
        try:
            await callback_query.message.delete()
        except:
            pass
        covering = get_covering(id=int(code.split('/')[-2].split('-')[0]))
        if covering.name == 'Эмаль':
            await bot.send_message(
                callback_query.from_user.id,
                text=f'Видео покрытия: https://disk.yandex.ru/i/n0Lc5OD2-eeG0g\n\n Презентация покрытия: https://disk.yandex.ru/i/hnBdh_2Cc1cE_w',
            )
        text, reply_markup = inline_kb_collections_by_covering(covering_id=int(code.split('/')[-2].split('-')[0]), page=int(code.split('/')[-2].split('-')[1]))
        
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    """
    # модели/продукты по покрытиям
    if re.fullmatch('menu/catalog/covering/\d*-\d*/', code):
        text, reply_markup = inline_kb_models(covering_id=int(code.split('/')[-2].split('-')[0]), page=int(code.split('/')[-2].split('-')[1]))
        
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
    """
    if code == 'menu/catalog/search':
        text = 'Введите название коллекции/модели/покрытия для поиска'
        await Form.search.set()
        reply_markup = InlineConstructor.create_kb([['Отмена','deny']], [1])
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )


    # Раздел "Задать свой вопрос"
    if code == 'menu/askquestion':
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
    try:
        if code.split('/')[1] == 'interiers':
            if code.split('/')[2] == 'collection':
                print(f"database/Интерьеры/{code.split('/')[3]}/")
                images = []
                for root, dirs, files in os.walk(f"database/Интерьеры/{code.split('/')[3]}/"):
                    for filename in files:
                        images.append(f"database/Интерьеры/{code.split('/')[3]}/{filename}")
                for image in images:
                    try:
                        photo = types.InputFile(image)
                        await bot.send_photo(
                            callback_query.message.chat.id, 
                            photo=photo, 
                            #caption=text, 
                            #reply_markup=reply_markup
                        )
                    except:
                        print('wtf')
                        pass
                await bot.send_message(
                    callback_query.from_user.id,
                    text=callback_query.message.text,
                    reply_markup=callback_query.message.reply_markup
                )
            if code.split('/')[2] == 'model':
                
                images = []
                for root, dirs, files in os.walk(f"database/Интерьеры/{code.split('/')[3]}/{code.split('/')[4]}/"):
                    for filename in files:
                        images.append(f"database/Интерьеры/{code.split('/')[3]}/{code.split('/')[4]}/{filename}")
                print(images)
                for image in images:
                    try:
                        photo = types.InputFile(image)
                        await bot.send_photo(
                            callback_query.message.chat.id, 
                            photo=photo, 
                            #caption=text, 
                            #reply_markup=reply_markup
                        )
                    except:
                        print('wtf')
                        pass
                await bot.send_message(
                    callback_query.from_user.id,
                    text=callback_query.message.text,
                    reply_markup=callback_query.message.reply_markup
                )
    except:
        pass
    
    if code == 'menu/admin':
        text, reply_markup = inline_kb_admin()
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
    
    if code == 'menu/admin/users':
        users = get_user()
        with open(f'Подписчики.txt', 'w') as file:
            c = 1
            file.write('Usermane | Имя Фамилия | Время регистрации | Время посленего посещения')
            for user in users:
                file.write(f'\n{c}. {user.username} | {user.first_name} {user.last_name} | {user.was_registered} | {user.last_usage}')
                c += 1
        await bot.send_document(callback_query.from_user.id, open(f'Подписчики.txt', 'r'))
        os.remove(f'Подписчики.txt')

    if code == 'menu/admin/addadmin':
        await Form.add_admin.set()
        reply_markup = InlineConstructor.create_kb([['Отмена','deny']], [1])
        await bot.send_message(
            callback_query.from_user.id, 
            text='Введите username пользователя (без @), которого вы хотите назначить администратором бота:',
            reply_markup=reply_markup
            )
    
    if re.fullmatch('menu/admin/deladmin/\d*', code) or code == 'menu/admin/deladmin':
        if code.split('/')[-1] != 'deladmin':
            update_user(id=code.split('/')[-1], is_admin=False)
            text, reply_markup = inline_kb_deladmin()
            await callback_query.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        text, reply_markup = inline_kb_deladmin()
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )
        



@dp.callback_query_handler(lambda c: c.data == 'close')
async def btn_callback(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

@dp.callback_query_handler(lambda c: 'modelbtn' in c.data)
async def btn_callback(callback_query: types.CallbackQuery):
    print(callback_query.data)
    num = callback_query.data.split('_')[-1]
    
    if num == '1' or num == '2':
        text, reply_markup = inline_kb_develop()
        
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )
    if num == '3':
        text, reply_markup = inline_kb_develop()
        text = markdown.text(
            'Видео:',
            'https://www.youtube.com/watch?v=HOX4yykWlm0',
            'https://www.youtube.com/watch?v=cVu-u7X8yrw',
            'https://www.youtube.com/watch?v=e0zP_ckQh7E',
            '',
            'Памятка:',
            'https://disk.yandex.ru/d/ZNW-nVVwjcB0XA',
            sep='\n'
        )
        
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )


@dp.callback_query_handler(lambda c: 'sendmessage' in c.data)
async def btn_callback(callback_query: types.CallbackQuery):
    print(callback_query.data)
    text = 'Введите текст сообщения'
    await Form.new_message.set()
    reply_markup = InlineConstructor.create_kb([['Отмена','deny']], [1])
    Form.prev_message = await bot.send_message(
        callback_query.from_user.id,
        text=text,
        reply_markup=reply_markup
    )


# Рассылка сообщения
@dp.callback_query_handler(lambda c: c.data == 'aceptsending', state=Form.new_message)
async def acceptsending(callback_query: types.CallbackQuery, state: FSMContext):
    print(f'User {callback_query.from_user.id} open {callback_query.data}')

    
    async with state.proxy() as data:
        data['new_message'] = callback_query.message.text

    text = data['new_message']

    for user_id in [u for u in get_users()]:
        try:
            await bot.send_message(
                user_id,
                text=text
            )
        except Exception as ex:
            print(ex)
    
    await state.finish()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=Form.prev_message.message_id)

    text, reply_markup = inline_kb_menu()
    await bot.send_message(
        callback_query.from_user.id,
        text=text + '\n\nСообщение отправлено пользователям.',
        reply_markup=reply_markup
    )

# Отмена рассылки сообщения
@dp.callback_query_handler(lambda c: c.data == 'denysending', state=Form.new_message)
async def denysending(callback_query: types.CallbackQuery, state: FSMContext):
    print(f'User {callback_query.from_user.id} open {callback_query.data}')

    await state.finish()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=Form.prev_message.message_id)

    text, reply_markup = inline_kb_menu()
    await bot.send_message(
            callback_query.from_user.id,
            text=text + '\n\nСообщение не разослано.', 
            reply_markup=reply_markup
            )
    

# Отмена для State
@dp.callback_query_handler(lambda c: c.data == 'deny', state=Form.add_admin)
@dp.callback_query_handler(lambda c: c.data == 'deny', state=Form.search)
@dp.callback_query_handler(lambda c: c.data == 'deny', state=Form.city)
@dp.callback_query_handler(lambda c: c.data == 'deny', state=Form.new_message)
async def denysending(callback_query: types.CallbackQuery, state: FSMContext):
    print(f'User {callback_query.from_user.id} open {callback_query.data}')

    await state.finish()
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: 'search' in c.data)
async def search(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data.split('_')
    print(f'User {callback_query.from_user.id} open {code}')
    if len(code) == 3:
        model_collections = list(set([prod.collection.id for prod in get_product(model=code[1]) if prod.covering.id == int(code[2])]))
        print(model_collections)
        if len(model_collections) > 1:
            text, reply_markup = inline_kb_choose_collection(model_id=code[1], covering=code[2], collections=model_collections)
        else:
            text, reply_markup = inline_kb_colors(page=1, collection_id=model_collections[0], covering_id=code[2], model_id=code[1])
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )
    else:
        text, reply_markup = inline_kb_colors(page=1, collection_id=code[3], covering_id=code[2], model_id=code[1])
        await bot.send_message(
            callback_query.from_user.id,
            text=text,
            reply_markup=reply_markup
        )


# Отмена (закрытие State)

@dp.callback_query_handler(lambda c: 'deny' in c.data, state=Form.add_news)
@dp.callback_query_handler(lambda c: 'deny' in c.data, state='next_photo')
async def denysending(callback_query: types.CallbackQuery, state: FSMContext):
    print(f'User {callback_query.from_user.id} open {callback_query.data}')
    code = callback_query.data.split('_')[-1]
    if code == 'nextphoto':
        
        with open('photo.txt', 'r') as file:
            files = file.read().split('//')

        _, reply_markup = inline_kb_sales(tg_id=callback_query.from_user.id)

        if len(files) == 1:    
            await bot.send_photo(
                callback_query.from_user.id, 
                photo=files[0], 
                reply_markup=reply_markup
            )
        else:
            media = types.MediaGroup()
            for id in files:
                media.attach_photo(id)
            await bot.send_media_group(
                callback_query.from_user.id, 
                media=media,
            )
            
            await bot.send_message(
                callback_query.from_user.id,
                text='Вернуться в предыдущее меню',
                reply_markup=reply_markup
            )
    elif code == 'addnews':
        text, reply_markup = inline_kb_news(callback_query.from_user.id)
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

    

    await state.finish()