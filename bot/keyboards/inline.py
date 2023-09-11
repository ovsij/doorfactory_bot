from aiogram.utils import markdown
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from emoji import emojize

from database.crud import *
from .constructor import InlineConstructor
from .buttons import *

# главное меню
def inline_kb_menu(tg_id : str):
    text = markdown.text(
        'ГЛАВНОЕ МЕНЮ',
        'Добро пожаловать в главное меню телеграм-бота фабрики межкомнатных дверей ALBERO!',
        'Выберите интересующий вас раздел:',
        sep='\n\n'
    )

    text_and_data = [
        [emojize(':door: Межкомнатные двери', language='alias'), 'menu/doors'],
        [emojize(':pushpin: Что нового?', language='alias'), 'menu/whatnew'],
        [emojize(':information: О фабрике', language='alias'), 'menu/about'],
        [emojize(':file_cabinet: Навигация по каталогу', language='alias'), 'menu/catalog'],
        [emojize(':raised_hand: Задать свой вопрос', language='alias'), 't.me/albero_callcenter'],
        
    ]
    schema = [1,1,1,1,1]
    btn_type = ['callback_data', 'callback_data', 'callback_data', 'callback_data', 'url']

    if get_user(tg_id=tg_id).is_admin:
        text_and_data.append(['Админка', 'menu/admin'])
        schema.append(1)
        btn_type.append('callback_data')
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

def inline_kb_doors():
    text = 'Выберите коллекцию:'
    collections = get_collection()
    text_and_data = []
    schema = []
    for collection in collections:
        if collection.name != 'Геометрия':
            text_and_data.append([collection.name, f'menu/doors/{collection.id}'])
        else:
            text_and_data.append(['Геометрия Эмаль', f'menu/doors/{collection.id}'])
        schema.append(1)

    text_and_data.append(btn_back('menu'))
    schema.append(1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_doorscollections(collection_id):
    text = 'Выберите модель:'
    collection = get_collection(id=collection_id)
    text_and_data = []
    schema = []
    if collection.name == 'Классика':
        model_names = ['Классика-1', 'Классика-2', 'Классика-3', 'Классика-4', 'Классика-5']
    if collection.name == 'НеоКлассика':
        model_names = ['НеоКлассика-1', 'НеоКлассика-2']
    if collection.name == 'Стиль':
        model_names = ['Стиль-1', 'Стиль-2']
    if collection.name == 'Геометрия':
        model_names = ['Геометрия-1', 'Геометрия-2', 'Геометрия-3', 'Геометрия-4', 'Геометрия-5', 'Геометрия-6', 'Геометрия-7', 'Геометрия-8']
    if collection.name == 'Status':
        model_names = ['STATUS А', 'STATUS G', 'STATUS M', 'STATUS S']
    if collection.name == 'Скрытые двери':
        model_names = ['ПС Отделка Тип 1-2', 'ПС Тип 1- 2']
    if collection.name == 'Галерея':
        model_names = ['Эрмитаж 1', 'Эрмитаж 2', 'Эрмитаж 3', 'Эрмитаж 4', 'Эрмитаж 6', 'Эрмитаж 7', 'Версаль 1', 'Лувр 1']
    if collection.name == 'Империя':
        model_names = ['Рим', 'Прадо', 'Византия', 'Спарта-2', 'Спарта-2 с молдингом', 'Олимпия', 'Киото', 'Афина-1', 'Афина-2']
    if collection.name == 'Альянс':
        model_names = ['Мехико', 'Гавана', 'Бостон', 'Мальта']
    if collection.name == 'Мегаполис':
        model_names = ['Вена', 'Прага', 'Мюнхен', 'Мадрид', 'Дублин', 'Дрезден', 'Валенсия', 'Сеул', 'Пекин', 'Рига', 'Сингапур-5', 'Кельн', 'Барселона', 'Сидней', 'Марсель']
    if collection.name == 'Мегаполис Лофт':
        model_names = ['Вена', 'Сеул', 'Дрезден', 'Дублин', 'Мюнхен', 'Валенсия']
    if collection.name == 'Мегаполис GL':
        model_names = ['Вена', 'Прага', 'Сидней', 'Сеул']
    if collection.name == 'WEST':
        model_names = ['Невада', 'Техас', 'Миссури', 'Каролина', 'Монтана']
    if collection.name == 'Тренд':
        model_names = ['Тренд Т - 1', 'Тренд Т - 2', 'Тренд Т - 3', 'Тренд Т - 4', 'Тренд Т - 5', 'Тренд Т - 7', 'Тренд Т- 10', 'Тренд Т- 12', 'Тренд Т- 14']

    models = [get_model(name=name) for name in model_names]
    
    for model in models:
        if collection.name != 'Скрытые двери':
            text_and_data.append([model.name, f'menu/doors/{collection.id}/{model.id}'])
            schema.append(1)
        else:
            text_and_data.append(['Скрытая дверь (под отделку)', f'menu/doors/{collection.id}/{model.id}']) if models.index(model) == 0 else None
            text_and_data.append(['Скрытая дверь (в покрытии)', f'menu/doors/{collection.id}/{model.id}']) if models.index(model) == 1 else None
            schema.append(1) if models.index(model) == 0 else None
            schema.append(1) if models.index(model) == 1 else None

    text_and_data.append(btn_back(f'menu/doors'))
    schema.append(1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_doorsmodel(collection_id, model_id):
    model = get_model(id=model_id)
    collection = get_collection(id=collection_id)
    model_ids_1 = [get_model(name='ПС Отделка Тип 1-2').id, get_model(name='ПС Отделка Тип 1-2 порог').id, get_model(name='ПС Отделка Тип 3-4').id, get_model(name='ПС Отделка Тип 3-4 порог').id]
    model_ids_2 = [get_model(name=mod_name).id for mod_name in ['ПС Тип 1- 2', 'ПС Тип 1- 2 порог', 'ПС Тип 3-4', 'ПС Тип 3-4 порог']]
    model_ids = {'ПС Отделка Тип 1-2': model_ids_1, 'ПС Тип 1- 2': model_ids_2}
    coverings = ''
    if 'ПС Отделка' in model.name or 'ПС Тип' in model.name:
        for model_id in model_ids[model.name]:
            for p in get_product(model=model_id):
                covering = get_covering(id=p.covering.id)
                if covering.name not in coverings:
                    coverings += covering.name + ', '
    else:
        for p in get_product(model=model_id, collection=collection_id):
            covering = get_covering(id=p.covering.id)
            if covering.name not in coverings:
                coverings += covering.name + ', '
    coverings = coverings.strip(', ')
    
    colors = ''
    if 'ПС Отделка' in model.name or 'ПС Тип' in model.name:
        covering_colors = {}
        for covering in coverings.split(', '):
            covering_colors[covering] = []
        for model_id in model_ids[model.name]:
            for covering in coverings.split(', '):
                covering = get_covering(name=covering)
                
                for color in get_color(model_id=model_id, covering_id=covering.id):
                    color = get_color(id=color.id)
                    covering_colors[covering.name].append(color.name)

        for covering, color in covering_colors.items():
            colors += f'\n<b>Доступные цвета в покрытии "{covering}":</b> \n'
            colors += str(set(color)).strip(', ').replace("'", '').replace("{", '').replace("}", '')
                
    else:
        for covering in coverings.split(', '):
            colors += f'\n<b>Доступные цвета в покрытии "{covering}":</b> \n'
            for color in get_color(model_id=model_id, covering_id=get_covering(name=covering).id):
                color = get_color(id=color.id)
                colors += color.name + ', '
            colors = colors.strip(', ')

    width = ''
    product_type = '' # тип полотна
    if 'ПС Отделка' in model.name or 'ПС Тип' in model.name:
        for model_id in model_ids[model.name]:
            for p in get_product(model=model_id):
                if p.product_type not in product_type:
                    product_type += p.product_type + ', '
                if p.width.replace('.0', '') not in width:
                    width += p.width.replace('.0', '') + ', '
    else:
        for p in get_product(model=model_id):
            if p.product_type not in product_type:
                product_type += p.product_type + ', '
            if p.width.replace('.0', '') not in width:
                width += p.width.replace('.0', '') + ', '
    width = width.strip(', ')
    product_type = product_type.strip(', ')

    glasstype = ''
    if 'ПС Отделка' in model.name or 'ПС Тип' in model.name:
        for model_id in model_ids[model.name]:
            for gt in get_glasstype(model_id=model_id, collection_id=collection_id):
                gt = get_glasstype(id=gt.id)
                if gt.name not in glasstype:
                    glasstype += gt.name + ', '
    else:
        for gt in get_glasstype(model_id=model_id, collection_id=collection_id):
            gt = get_glasstype(id=gt.id)
            if gt.name not in glasstype:
                glasstype += gt.name + ', '
    glasstype = glasstype.strip(', ')

    # вид полотна
    type_product = ''
    type_product += 'Полотно глухое, ' if 'ПГ' in glasstype else ''
    type_product += 'Полотно остекленное' if 'Стекло' in glasstype else ''
    type_product = type_product.strip(', ')
    glasstype = 'ПГ, ' + glasstype.replace('ПГ', '').replace('ПГ, ', '') if 'ПГ' in glasstype and not 'Полотно глухое' in glasstype else glasstype
    glasstype = glasstype.strip(', ')
    
    model_name = 'Скрытая дверь (под отделку)' if model.name == 'ПС Отделка Тип 1-2' else 'Скрытая дверь (в покрытии)' if model.name == 'ПС Тип 1- 2' else model.name
    text = markdown.text(
        f'<b>Модель:</b> {model_name}',
        f'<b>Коллекция:</b> {collection.name}',
        f'<b>Доступные покрытия:</b> {coverings}{colors}',
        f'<b>Тип полотна:</b> {product_type}',
        f'<b>Вид полотна:</b> {type_product}',
        f'<b>Остекление:</b> {glasstype}',
        '<b>Стандартные размеры:</b>',
        'Высота полотна: 2000 мм',
        f'Ширина полотна: {width} мм',
        sep='\n'
    )
    text_and_data = [['Показать фото моделей', f'menu/doors/{collection.id}/{model.id}/photos']]
    schema = [1]
    text_and_data.append(btn_back(f'menu/doors/{collection_id}'))
    schema.append(1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb
        

# Раздел "Что нового?"
def inline_kb_whatnew():
    text = markdown.text(
        'ЧТО НОВОГО?',
        'Добро пожаловать в главное меню телеграм-бота фабрики межкомнатных дверей ALBERO!',
        'Выберите интересующий вас раздел:',
        sep='\n\n'
    )
    try:
        last_news_index = get_news()[0].id
    except:
        last_news_index = None

    text_and_data = [
        [emojize(':gift: Акции', language='alias'), 'menu/whatnew/sales'],
        [emojize(':newspaper: Новости', language='alias'), f'menu/whatnew/news/{last_news_index}'],
        [emojize(':movie_camera: Вебинары', language='alias'), 'menu/whatnew/webinars'],
        [emojize(':raised_hand: Задать свой вопрос', language='alias'), 't.me/albero_callcenter'],
        btn_back('menu')
    ]
    schema = [1,1,1,1,1]
    btn_type = ['callback_data', 'callback_data', 'callback_data', 'url', 'callback_data']
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

def inline_kb_sales(tg_id : str):
    text = markdown.text(
        'Раздел "АКЦИИ" находится в разработке'
    )
    text_and_data = [
        btn_back('menu/whatnew')
    ]
    
    if get_user(tg_id=tg_id).is_admin:
        text_and_data.insert(0, ['Изменить картинку', 'menu/sales/changepicture'])
    schema = [1 for _ in range(len(text_and_data))]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb


def inline_kb_news(tg_id, news_index):
    if news_index == None:
        text = 'Новостей пока нет...'
        text_and_data = [
            btn_back('menu/whatnew')
        ]
        schema = [1]
        if get_user(tg_id=tg_id).is_admin:
            text_and_data.insert(0, ['Добавить новость', 'menu/whatnew/news/add'])
            schema.insert(0, 1)
        image = None
    else:

        bottom_text = markdown.text(
            '',
            '',
            '\-\-\-\-\-',
            '',
            'Подпишитесь на наши социальные сети:',
            markdown.text(markdown.link('Телеграм', 'https://t.me/alberofabrica'), markdown.link('Вконтакте', 'https://vk.com/albero_doors'), sep='     '),
            '',
            markdown.text(markdown.link('YouTube', 'https://www.youtube.com/channel/UCyxrLbTK1jQLBUSllWZovYw'), markdown.link('Дзен', 'https://zen.yandex.ru/id/624ea43b2970e30bb156d947'), sep='        '),
            sep='\n'
        )
        all_news = [n.id for n in get_news()]
        
        news = get_news(id=news_index)
        prev_news = all_news[all_news.index(news.id)-1]
        try:
            next_news = all_news[all_news.index(news.id)+1]
        except:
            pass

        text = news.text
        image = news.image

        text_and_data = [
            btn_back('menu/whatnew')
        ]
        schema = [1]

        

        if all_news.index(news.id) == 0 and len(all_news) > 1:
            text_and_data.insert(0, [emojize(':arrow_right: Следующая', language='alias'), f'menu/whatnew/news/{next_news}'])
            schema.append(1)

        
        elif all_news.index(news.id) == len(all_news) - 1 and len(all_news) > 1:
            text_and_data.insert(0, [emojize(':arrow_left: Предыдущая', language='alias'), f'menu/whatnew/news/{prev_news}'])
            schema.append(1)

        elif len(all_news) > 1:
            text_and_data.insert(0, [emojize(':arrow_right: Следующая', language='alias'), f'menu/whatnew/news/{next_news}'])
            text_and_data.insert(0, [emojize(':arrow_left: Предыдущая', language='alias'), f'menu/whatnew/news/{prev_news}'])
            schema.insert(0, 2)


        if get_user(tg_id=tg_id).is_admin:
            text_and_data.insert(0, ['Удалить новость', f'menu/whatnew/news/delete/{news_index}'])
            text_and_data.insert(0, ['Добавить новость', 'menu/whatnew/news/add'])
            schema.insert(0, 1)
            schema.insert(0, 1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb, image

def inline_kb_webinars():
    text = markdown.text(
        'В ближайшее время мероприятия не запланированы. Смотрите наши видео на YouTube.'
    )
    text_and_data = [
        ['Перейти на YouTube', 'https://www.youtube.com/channel/UCyxrLbTK1jQLBUSllWZovYw'],
        btn_back('menu/whatnew')
    ]
    schema = [1, 1]
    btn_type = ['url', 'callback_data']
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

# Раздел "О фабрике"
def inline_kb_about():
    text = markdown.text(
        'О ФАБРИКЕ',
        'Добро пожаловать в главное меню телеграм-бота фабрики межкомнатных дверей ALBERO!',
        'Выберите интересующий вас раздел:',
        sep='\n\n'
    )
    text_and_data = [
        [emojize(':factory: О нас', language='alias'), 'menu/about/production'],
        [emojize(':movie_camera: Видео', language='alias'), 'menu/about/video'],
        [emojize(':globe_with_meridians: Наш сайт', language='alias'), 'https://alberodoors.com'],
        [emojize(':telephone: Позвонить', language='alias'), 'http://onmap.uz/tel/78005507954'],
        [emojize(':pencil2: Написать нам', language='alias'), 't.me/albero_callcenter'],
        btn_back('menu')
    ]
    schema = [1,1,1,1,1,1]
    btn_type = ['callback_data', 'callback_data', 'url', 'url', 'url', 'callback_data']
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

def inline_kb_production():
    text = markdown.text(
        'ALBERO — крупная фабрика по производству межкомнатных дверей, входящая в ТОП-3 ведущих дверных фабрик России по объёму выпускаемой продукции.',
        'Год основания фабрики — 2002 год.',
        '',
        'За 20 лет работы фабрика выросла до масштабов с производительностью 80 000 комплектов дверей в месяц, с развитой дилерской и собственной сетью розничных салонов.',
        '',
        'Производственный процесс включает в себя полный цикл изготовления продукции: от разработки новых моделей, входящего контроля качества материалов до изготовления готовой двери и конечного контроля качества на этапе упаковки.',
        'В структуре компании 6  региональных представительств на территории России: Москва, Новосибирск, Красноярск, Краснодар, Самара, Екатеринбург.',
        '',
        '<b>Главный офис и производство в Новосибирске:',
        '630088, г. Новосибирск, ул. Сибиряков-Гвардейцев, 49/3</b>',
        '',
        '<b>Производство в Балаково:</b>',
        '413859, г. Балаково, ул.Транспортная, 12',
        sep='\n'
    )
    text_and_data = [
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_video():
    text = markdown.text(
        '<b>Межкомнатные двери от фабрики-производителя ALBERO:</b>',
        'https://www.youtube.com/watch?v=fBpm5DExr8U',
        '',
        sep='\n'
    )
    text_and_data = [
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb


def inline_kb_call():
    text = markdown.text(
        'Раздел "ПОЗВОНИТЬ" находится в разработке'
    )
    text_and_data = [
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# Раздел "Каталог"
def inline_kb_catalog():
    text = markdown.text(
        'КАТАЛОГ',
        'Добро пожаловать в главное меню телеграм-бота фабрики межкомнатных дверей ALBERO!',
        'Выберите интересующий вас раздел:',
        sep='\n\n'
    )
    text_and_data = [
        [emojize(':new: Новинки', language='alias'), 'menu/catalog/novelty'],
        #[emojize(':door: Коллекции', language='alias'), 'menu/catalog/collections'],
        [emojize(':orange_circle: Покрытия', language='alias'), 'menu/catalog/covering'],
        [emojize(':mag: Поиск', language='alias'), 'menu/catalog/search'],
        btn_back('menu')
    ]
    schema = [1,1,1,1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_novelty():
    text = markdown.text(
        'Раздел "НОВИНКИ" находится в разработке'
    )
    text_and_data = [
        ['Где купить', 'menu/catalog/novelty/wheretobuy'],
        btn_back('menu/catalog')
    ]
    schema = [1, 1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_collections():
    text = "КОЛЛЕКЦИИ"
    text_and_data = []
    schema = [1]
    for collection in get_collection():
        text_and_data.append([collection.name, f'menu/catalog/collections/{collection.id}-1/'])
        schema.append(1)
    
    text_and_data.append(btn_back('menu/catalog'))
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_models(page : int, collection_id : int = None, covering_id : int = None):
    text_and_data = []
    schema = []
    if collection_id:
        text = f'Коллекция {get_collection(id=collection_id).name}'
        for model in get_model(collection=collection_id):
            text_and_data.append([model.name, f'menu/catalog/collections/{collection_id}/{model.id}/'])
            schema.append(1)
        if len(text_and_data) > 10:
            btn_prevnext_name = f'menu/catalog/collections/{collection_id}'
            text_and_data, schema = btn_prevnext(len(text_and_data), text_and_data, schema, page, name=btn_prevnext_name)
        schema.append(1)
        text_and_data.append(btn_back('menu/catalog/collections'))
    if covering_id:
        text = f'Покрытие {get_covering(id=covering_id).name}'
        for model in get_model(covering=covering_id):
            text_and_data.append([model.name, f'menu/catalog/covering/{covering_id}/{model.id}/'])
            schema.append(1)
        if len(text_and_data) > 10:
            btn_prevnext_name = f'menu/catalog/covering/{covering_id}'
            text_and_data, schema = btn_prevnext(len(text_and_data), text_and_data, schema, page, name=btn_prevnext_name)
        schema.append(1)
        text_and_data.append(btn_back('menu/catalog/covering'))
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb


def inline_kb_glass_by_covering_collection_model(page : int, collection_id : int = None, covering_id : int = None,  model_id : int = None):
    text_and_data = []
    schema = []
    collection = get_collection(id=collection_id)
    covering = get_covering(id=covering_id)
    text = f'Покрытие {covering.name}\nКоллекция {collection.name}\nМодели в данной конфиругации:'
    for model in get_model():
        if model.covering.id == covering.id and model.collection.id == collection.id:
            text_and_data.append([model.name, f'menu/catalog/covering/{covering_id}/{collection_id}/{model.id}/'])
            schema.append(1)
    schema.append(1)
    text_and_data.append(btn_back('menu/catalog/covering'))
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# продукты внутри категории
def inline_kb_model_by_collection(model_id : int, collection_id : int):
    model = get_model(id=model_id)
    covering = get_covering(id=model.covering.id).name
    text = markdown.text(
        f'МОДЕЛЬ: {model.name}',
        f'ТИП ПОКРЫТИЯ: {covering}',
        f'ВАРИАНТЫ ОСТЕКЛЕНИЯ: {model.glass_type}',
        f'СТАНДАРТНАЯ ВЫСОТА ПОЛОТНА: {model.height}',
        f'ШИРИНА ПОЛОТНА: {model.width}',
        f'ТИП: {model.product_type}',
        f'ТОЛЩИНА ПОЛОТНА: {model.depth}',
        sep='\n'
    )
    text_and_data = [
        ['Конструкция полотна', 'q'],
        ['Особенности ухода и монтажа', 'q'],
        ['Погонажные изделия', 'q'],
        ['Варианты комплектации', 'q'],
        ['Где купить', 'menu/wheretobuy'],
    ]
    schema = [1, 1, 1, 1, 1]

    models_id = [m.id for m in get_model(collection=collection_id)]
    back = models_id[models_id.index(model_id) - 1]
    if models_id.index(model_id) == len(models_id) - 1:
        next = models_id[0]
    else:
        next = models_id[models_id.index(model_id) + 1]
    text_and_data += [
        [emojize(':arrow_backward:', language='alias'), f'menu/catalog/collections/{collection_id}/{back}/'],
        [f'[{models_id.index(model_id) + 1} из {len(models_id)}]', f'btn_pass'],
        [emojize(':arrow_forward:', language='alias'), f'menu/catalog/collections/{collection_id}/{next}/'],
    ]
    schema.append(3)

    text_and_data.append(btn_back(f'menu/catalog/collections/{collection_id}-1/'))
    schema.append(1)

    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb


#
#
#
#
#
#
#


def inline_kb_covering():
    text = "ПОКРЫТИЯ"
    text_and_data = []
    schema = [1]
    for covering in get_covering():
        text_and_data.append([covering.name, f'menu/catalog/covering/{covering.id}-1/'])
        schema.append(1)
    
    text_and_data.append(btn_back('menu/catalog'))
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_collections_by_covering(covering_id : int, page : int):
    covering = get_covering(id=covering_id)
    text = f'<b>Покрытие:</b> {covering.name}\n\nКоллекции в выбранном покрытии:'
    text_and_data = []
    schema = []
    collections = []
    #for model in get_model():
    #    if model.covering.id == covering_id and model.collection.id not in collections:
    #        collections.append(model.collection.id)

    for collection in get_collection(covering=covering_id):
        text_and_data.append([collection.name, f'menu/catalog/covering/{covering_id}/{collection.id}-1/'])
        schema.append(1)
    if covering.name == 'Эмаль':
        button_type = ['callback_data' for _ in range(len(text_and_data))]
        text_and_data.append(['Видео', 'https://youtu.be/JU4NdS6OlUI?si=KEAYo4gSaVZgLaPT'])
        text_and_data.append(['Презентация', 'https://disk.yandex.ru/d/MyKDLj4RAMyllg'])
        schema.append(1)
        schema.append(1)
        button_type.append('url')
        button_type.append('url')
        text_and_data.append(btn_back(f'menu/catalog/covering'))
        schema.append(1)
        button_type.append('callback_data')
        inline_kb = InlineConstructor.create_kb(text_and_data, schema, button_type=button_type)
        return text, inline_kb
    else:
        text_and_data.append(btn_back(f'menu/catalog/covering'))
        schema.append(1)
        inline_kb = InlineConstructor.create_kb(text_and_data, schema)
        return text, inline_kb

def inline_kb_models_by_covering_collection(page : int, collection_id : int = None, covering_id : int = None):
    text_and_data = []
    schema = []
    collection = get_collection(id=collection_id)
    covering = get_covering(id=covering_id)
    text = f'<b>Покрытие:</b> {covering.name}\n<b>Коллекция:</b> {collection.name}\nМодели в данной конфиругации:'
    for model in get_model(covering=covering_id, collection=collection_id):
        text_and_data.append([model.name, f'menu/catalog/covering/{covering_id}/{collection_id}/{model.id}/'])
        schema.append(1)
    
    if len(text_and_data) > 10:
        btn_prevnext_name = f'menu/catalog/covering/{covering_id}/{collection_id}'
        text_and_data, schema = btn_prevnext(len(text_and_data), text_and_data, schema, page, name=btn_prevnext_name)
    
        buttons_1 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data[:-3])
        inline_kb = InlineKeyboardMarkup()
        for button in buttons_1:
            inline_kb.add(button)
        buttons_2 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data[-3:])
        inline_kb.row(*buttons_2)
    else:
        buttons_1 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        inline_kb = InlineKeyboardMarkup()
        for button in buttons_1:
            inline_kb.add(button)
    
    button_type = ['callback_data' for _ in text_and_data]
    if collection.name == 'Status':
        text_and_data_3 = [
            ['Видео', 'https://youtu.be/g7kMSefuJRk?si=is__sIQP-rJ7Fy0w'],
            ['Презентация', 'https://disk.yandex.ru/d/CuSYCDrjVIa4xQ']
        ]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Status']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'НеоКлассика':
        text_and_data_3 = [
            ['Видео', 'https://youtu.be/hl5xnnT1Eqk?si=4kbjsd9ctYhYoQhG']
        ]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/НеоКлассика']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Геометрия':
        text_and_data_3=[
            ['Видео', 'https://youtu.be/ZbZRnUDHDqU?si=906sCWpQ8Gygrq5h'],
            ['Презентация', 'https://disk.yandex.ru/d/J9BRnGO36jBWTg']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Геометрия']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Альянс':
        text_and_data_3 = [
            ['Видео', 'https://youtu.be/1hp5ijrdLLc?si=sBIcvHLWH3FKdJga'],
            ['Презентация', 'https://disk.yandex.ru/d/8Psy0ZA_ugH32A']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Альянс']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Классика':
        text_and_data_3 = [
            ['Видео', 'https://youtu.be/S980dRQxUr8?si=-SXDQa7CBJiuRDCz'],
            ['Презентация', 'https://disk.yandex.ru/d/bPmUoch_JiMr7Q']
            ]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Классика']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Стиль':
        text_and_data_3 = [['Презентация', 'https://disk.yandex.ru/d/xFFl71wcA-4kng']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Мегаполис GL':
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Мегаполис GL']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Неоклассика':
        text_and_data_3 = [
            ['Видео', 'https://youtu.be/hl5xnnT1Eqk?si=bW0sE39UOxXswIty'],
            ]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Неоклассика']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Скрытые двери':
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Скрытые двери']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Тренд':
        text_and_data_3 = [['Презентация', 'https://disk.yandex.ru/d/wTPHd9iWgpXWtQ']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/Тренд']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'WEST':
        text_and_data_3 = [['Презентация', 'https://disk.yandex.ru/d/ZAFYQw6i1spg0Q']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
        text_and_data_3 = [['Интерьеры', 'menu/interiers/collection/West']]
        buttons_3 = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Галерея':
        text_and_data_3 = [['Видео', 'https://youtu.be/IOVG-8FnZMo?si=xoFRuPaEE8VTNjM7']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Империя':
        text_and_data_3 = [['Презентация', 'https://disk.yandex.ru/d/1iD5H_ysZpP8Xg']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Мегаполис':
        text_and_data_3 = [['Видео', 'https://youtu.be/ih5ZiI_MFhE?si=XquF3tOKigvV2Y4Q']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    if collection.name == 'Мегаполис Лофт':
        text_and_data_3 = [['Презентация', 'https://disk.yandex.ru/d/x8T7uY1v0McxTA']]
        buttons_3 = (InlineKeyboardButton(text, url=data) for text, data in text_and_data_3)
        inline_kb.row(*buttons_3)
    text_and_data.append(btn_back(f'menu/catalog/covering/{covering_id}-1/'))
    inline_kb.row(InlineKeyboardButton(emojize(':arrow_left: Назад', language='alias'), callback_data=f'menu/catalog/covering/{covering_id}-1/'))
    
    #InlineConstructor.create_kb(text_and_data, schema, button_type=button_type)
    return text, inline_kb

# цвета покрытия для модели
def inline_kb_colors(covering_id : int, collection_id : int, model_id : int, page : int = None):
    covering = get_covering(id=covering_id)
    collection = get_collection(id=collection_id)
    model = get_model(id=model_id)
    text = f'<b>Покрытие:</b> {covering.name}\n\n<b>Коллекция:</b> {collection.name}\n\n<b>Модель:</b> {model.name}\n\nЦвета покрытия:'
    colors = get_color(model_id=model_id, covering_id=covering_id)
    text_and_data = []
    schema = []
    for color in colors:
        text_and_data.append([get_color(id=int(color.id)).name, f'menu/catalog/covering/{covering_id}/{collection_id}/{model_id}/{color.id}/'])
        schema.append(1)

    if 'Версаль' in model.name:
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Версаль'])
        schema.append(1)
    if model.name == 'Лувр 1':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Лувр 1'])
        schema.append(1)
    if model.name == 'Эрмитаж 1':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 1'])
        schema.append(1)
    if model.name == 'Эрмитаж 2':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 2'])
        schema.append(1)
    if model.name == 'Эрмитаж 3':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 3'])
        schema.append(1)
    if model.name == 'Эрмитаж 4':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 4'])
        schema.append(1)
    if model.name == 'Эрмитаж 5':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 5'])
        schema.append(1)
    if model.name == 'Эрмитаж 6':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 6'])
        schema.append(1)
    if model.name == 'Эрмитаж 7':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Галерея/Эрмитаж 7'])
        schema.append(1)
    
    if model.name == 'Афина-1':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Афина-1'])
        schema.append(1)
    if model.name == 'Афина-2':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Афина-2'])
        schema.append(1)
    if model.name == 'Византия':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Византия'])
        schema.append(1)
    if model.name == 'Киото':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Киото'])
        schema.append(1)
    if model.name == 'Олимпия':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Олимпия'])
        schema.append(1)
    if model.name == 'Прадо':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Прадо'])
        schema.append(1)
    if model.name == 'Рим':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Рим'])
        schema.append(1)
    if model.name == 'Спарта':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Империя/Спарта'])
        schema.append(1)
    
    if model.name == 'Барселона':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Барселона'])
        schema.append(1)
    if model.name == 'Вена':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Вена'])
        schema.append(1)
    if model.name == 'Дрезден':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Дрезден'])
        schema.append(1)
    if model.name == 'Дублин':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Дублин'])
        schema.append(1)
    if model.name == 'Кельн':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Кельн'])
        schema.append(1)
    if model.name == 'Мадрид':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Мадрид'])
        schema.append(1)
    if model.name == 'Марсель':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Марсель'])
        schema.append(1)
    if model.name == 'Мюнхен':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Мюнхен'])
        schema.append(1)
    if model.name == 'Прага':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Прага'])
        schema.append(1)
    if model.name == 'Рига':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Рига'])
        schema.append(1)
    if model.name == 'Сеул':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Сеул'])
        schema.append(1)
    if model.name == 'Сидней':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Сидней'])
        schema.append(1)
    if model.name == 'Сингапур':
        text_and_data.append(['Интерьеры', 'menu/interiers/model/Мегаполис/Сингапур'])
        schema.append(1)
    

        

    text_and_data.append(btn_back(f'menu/catalog/covering/{covering_id}/{collection_id}-1/'))
    schema.append(1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# типы стекла
def inline_kb_glases(covering_id : int, collection_id : int, model_id : int, color_id : int):
    covering = get_covering(id=covering_id)
    collection = get_collection(id=collection_id)
    model = get_model(id=model_id)
    color = get_color(id=color_id)
    text = f'<b>Покрытие:</b> {covering.name}\n\n<b>Коллекция:</b> {collection.name}\n\n<b>Модель:</b> {model.name}\n\n<b>Цвет покрытия:</b> {color.name}\n\nТипы остекления:'
    glases = get_glasstype(model_id=model_id, covering_id=covering_id, color_id=color_id)
    text_and_data = []
    schema = []
    for glass in glases:
        text_and_data.append([get_glasstype(id=int(glass.id)).name, f'menu/catalog/covering/{covering_id}/{collection_id}/{model_id}/{color_id}/{glass.id}/'])
        schema.append(1)
    
    text_and_data.append(btn_back(f'menu/catalog/covering/{covering_id}/{collection_id}/{model_id}/'))
    schema.append(1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# продукты внутри покрытия
def inline_kb_model(covering_id : int, collection_id : int, model_id : int, color_id : int, glasstype_id : int):
    
    covering = get_covering(id=covering_id)
    collection = get_collection(id=collection_id)
    model = get_model(id=model_id)
    color = get_color(id=color_id)
    glasstype = get_glasstype(id=glasstype_id)
    product = [p for p in get_product(model=model_id, color=color_id, glass_type=glasstype_id)]
    colors = ''
    for col in get_color(model_id=model_id, covering_id=covering_id):
        color_ = get_color(id=col.id)
        colors += color_.name + ', '
    colors = colors.strip(', ')
    gtypes = ''
    for gt in get_glasstype(model_id=model_id, color_id=color_id):
        gtype_ = get_glasstype(id=gt.id)
        gtypes += gtype_.name + ', '
    gtypes = gtypes.strip(', ')
    widths = ''
    for prod in product:
        widths += prod.width.replace('.0', '') + ', ' if prod.width.replace('.0', '') not in widths else ''
    widths = widths.strip(', ')
    print(product)
    text = markdown.text(
        f'МОДЕЛЬ: {model.name}',
        '',
        f'ТИП ПОКРЫТИЯ: {covering.name}',
        '',
        f'ЦВЕТ: {color.name}',
        f'ДОСТУПНЫЕ ЦВЕТА: {colors}',
        '',
        f'ТИП ОСТЕКЛЕНИЯ: {glasstype.name}',
        f'ДОСТУПНЫЕ ТИПЫ ОСТЕКЛЕНИЯ: {gtypes}',
        '',
        f'СТАНДАРТНАЯ ВЫСОТА ПОЛОТНА: {product[0].height}',
        f'ШИРИНА ПОЛОТНА: {widths}',
        f'ТИП: {product[0].product_type}',
        f'ТОЛЩИНА ПОЛОТНА: {product[0].depth}',
        sep='\n'
    )
    text_and_data = [
        ['Конструкция полотна', f'modelbtn_1'],
        ['Погонажные изделия', 'modelbtn_2'],
        ['Особенности ухода и монтажа', 'modelbtn_3'],
        ['Где купить', 'menu/wheretobuy'],
    ]
    schema = [1, 1, 1, 1]

    models_id = [m.id for m in get_model(covering=covering_id)]
    back = models_id[models_id.index(model_id) - 1]
    if models_id.index(model_id) == len(models_id) - 1:
        next = models_id[0]
    else:
        next = models_id[models_id.index(model_id) + 1]
    #text_and_data += [
    #    [emojize(':arrow_backward:', language='alias'), f'menu/catalog/corering/{covering_id}/{back}/'],
    #    [f'[{models_id.index(model_id) + 1} из {len(models_id)}]', f'btn_pass'],
    #    [emojize(':arrow_forward:', language='alias'), f'menu/catalog/corering/{covering_id}/{next}/'],
    #]
    #schema.append(3)

    text_and_data.append(btn_back(f'menu/catalog/covering/{covering_id}/{collection_id}/{model_id}/{color_id}/'))
    schema.append(1)
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_develop():
    text = markdown.text(
        'Данный раздел находится в стадии разработки'
    )
    text_and_data = [
        ['Скрыть', 'close']
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_nosearch(request : str):
    text = markdown.text(
        f'К сожалению, по вашему запросу "{request}" ничего не найдено'
    )
    text_and_data = [
        btn_back('menu/catalog')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# админка
def inline_kb_admin():
    text = 'Меню администратора'
    text_and_data = [
        ['Рассылка', 'btn_sendmessage'],
        ['Подписчики', 'menu/admin/users'],
        ['Добавить администратора', 'menu/admin/addadmin'],
        ['Удалить администратора', 'menu/admin/deladmin'],
        btn_back('menu')
    ]
    schema = [1, 1, 1, 1, 1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# удалить админа
def inline_kb_deladmin():
    text = 'Выберите пользователя, которого вы хотите исключить из администраторов бота'
    text_and_data = []
    admins = [u for u in get_user() if u.is_admin]
    for admin in admins:
        print(int(admin.tg_id))
        if str(int(admin.tg_id)) == '733733168' or str(int(admin.tg_id)) == '227184505':
            continue
        text_and_data.append([admin.username, f'menu/admin/deladmin/{admin.id}'])
    text_and_data.append(btn_back('menu/admin'))
    schema = [1 for _ in range(len(text_and_data))]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

# проверка сообщения перед отправкой
def inline_sendmessage():
    text_and_data = [
        [emojize(':white_check_mark: Отправить :white_check_mark:', language='alias'), 'aceptsending'],
        [emojize(':x: Отменить :x:', language='alias'), 'denysending']
    ]
    schema = [1, 1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return inline_kb

# выбор покрытия если модель представленна в нескольких (при поиске)
def inline_kb_choose_covering(coverings : list, model : Model = None, collection: Collection = None):
    if model:
        text = f'Выберите покрытие для модели {model.name}'
        text_and_data = [[get_covering(id=c).name, f'search_{model.id}_{c}'] for c in coverings]
        
    if collection:
        text = f'Выберите покрытие для коллекции {collection.name}'
        text_and_data = [[get_covering(id=c).name, f'menu/catalog/covering/{c}/{collection.id}-1/'] for c in coverings]

    text_and_data.append(btn_back('menu/catalog'))
    schema = [1 for _ in range(len(text_and_data))]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_choose_collection(model_id : int, covering : int, collections : list):

    text = f'Покрытие: {get_covering(id=covering).name}\n\nВыберите коллекцию для модели {get_model(id=model_id).name}'
    text_and_data = [[get_collection(id=c).name, f'search_{model_id}_{covering}_{c}'] for c in collections]
    text_and_data.append(btn_back('menu/catalog'))
    schema = [1 for _ in range(len(text_and_data))]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb