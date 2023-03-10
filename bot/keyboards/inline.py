from aiogram.utils import markdown
from emoji import emojize

from .constructor import InlineConstructor
from .buttons import *

# главное меню
def inline_kb_menu():
    text = markdown.text(
        'ГЛАВНОЕ МЕНЮ',
        'Добро пожаловать в главное меню телеграм-бота фабрики межкомнатных дверей ALBERO!',
        'Выберите интересующий вас раздел:',
        sep='\n\n'
    )

    text_and_data = [
        ['Что нового?', 'menu/whatnew'],
        ['О фабрике', 'menu/about'],
        ['Каталог', 'menu/catalog'],
        ['Задать свой вопрос', 't.me/Alberodoor'],
    ]
    schema = [1,1,1,1]
    btn_type = ['callback_data', 'callback_data', 'callback_data', 'url']
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

# Раздел "Что нового?"
def inline_kb_whatnew():
    text = markdown.text(
        'ЧТО НОВОГО?',
        'Добро пожаловать в главное меню телеграм-бота фабрики межкомнатных дверей ALBERO!',
        'Выберите интересующий вас раздел:',
        sep='\n\n'
    )

    text_and_data = [
        ['Акции', 'menu/whatnew/sales'],
        ['Новости', 'menu/whatnew/news'],
        ['Вебинары', 'menu/whatnew/webinars'],
        ['Задать свой вопрос', 't.me/Alberodoor'],
        btn_back('menu')
    ]
    schema = [1,1,1,1,1]
    btn_type = ['callback_data', 'callback_data', 'callback_data', 'url', 'callback_data']
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

def inline_kb_sales():
    text = markdown.text(
        'Раздел "АКЦИИ" находится в разработке'
    )
    text_and_data = [
        ['Где купить', 'menu/whatnew/sales/wheretobuy'],
        btn_back('menu/whatnew')
    ]
    schema = [1,1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_wheretobuy():
    text = markdown.text(
        'Раздел "ГДЕ КУПИТЬ" находится в разработке'
    )
    text_and_data = [
        btn_back('menu/whatnew/sales')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_news():
    text = markdown.text(
        'Раздел "НОВОСТИ" находится в разработке\n',
        'Подпишитесь на наши социальные сети:',
        markdown.text(markdown.link('Телеграм', 'https://t.me/alberofabrica'), markdown.link('Вконтакте', 'https://vk.com/albero_doors'), sep='     '),
        markdown.text(markdown.link('Телеграм', 'https://t.me/alberofabrica'), markdown.link('Вконтакте', 'https://vk.com/albero_doors'), sep='     '),
        markdown.text(markdown.link('Телеграм', 'https://t.me/alberofabrica'), markdown.link('Вконтакте', 'https://vk.com/albero_doors'), sep='     '),
        '',
        markdown.text(markdown.link('YouTube', 'https://www.youtube.com/channel/UCyxrLbTK1jQLBUSllWZovYw'), markdown.link('Дзен', 'https://zen.yandex.ru/id/624ea43b2970e30bb156d947'), sep='        '),
        markdown.text(markdown.link('YouTube', 'https://www.youtube.com/channel/UCyxrLbTK1jQLBUSllWZovYw'), markdown.link('Дзен', 'https://zen.yandex.ru/id/624ea43b2970e30bb156d947'), sep='        '),
        markdown.text(markdown.link('YouTube', 'https://www.youtube.com/channel/UCyxrLbTK1jQLBUSllWZovYw'), markdown.link('Дзен', 'https://zen.yandex.ru/id/624ea43b2970e30bb156d947'), sep='        '),
        sep='\n'
    )
    text_and_data = [
        btn_back('menu/whatnew')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

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
        ['Производство', 'menu/about/production'],
        ['Наш сайт', 'https://alberodoors.com'],
        ['Позвонить', 'https://alberodoors.com/contacts/'],
        ['Написать нам', 't.me/Alberodoor'],
        btn_back('menu')
    ]
    schema = [1,1,1,1,1]
    btn_type = ['callback_data', 'url', 'url', 'url', 'callback_data']
    inline_kb = InlineConstructor.create_kb(text_and_data, schema, btn_type)
    return text, inline_kb

def inline_kb_production():
    text = markdown.text(
        'Фабрика межкомнатных дверей ALBERO',
        '2 производственных площадки:',
        '',
        'Производство в г. Балаково',
        '413859б г. Балаково, ул. Транспортная, 12',
        '',
        'Главный офис и производство г. Новосибирск',
        '630088, г.Новосибирск, ул. Сибиряков-Гвардейцев, 49/3',
        
        sep='\n'
    )
    text_and_data = [
        ['Где купить', 'menu/about/production/wheretobuy'],
        btn_back('menu/about')
    ]
    schema = [1, 1]
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
        ['Новинки', 'menu/catalog/novelty'],
        ['Коллекции', 'menu/catalog/collections'],
        ['Покрытия', 'menu/catalog/covering'],
        ['Поиск', 'menu/catalog/search'],
        btn_back('menu')
    ]
    schema = [1,1,1,1, 1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_novelty():
    text = markdown.text(
        'Раздел "НОВИНКИ" находится в разработке'
    )
    text_and_data = [
        ['Где купить', 'menu/catalog/novelty/wheretobuy'],
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_collections():
    text = markdown.text(
        'Раздел "КОЛЛЕКЦИИ" находится в разработке'
    )
    text_and_data = [
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_covering():
    text = markdown.text(
        'Раздел "ПОКРЫТИЯ" находится в разработке'
    )
    text_and_data = [
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb

def inline_kb_search():
    text = markdown.text(
        'Раздел "ПОИСК" находится в разработке'
    )
    text_and_data = [
        btn_back('menu/about')
    ]
    schema = [1]
    inline_kb = InlineConstructor.create_kb(text_and_data, schema)
    return text, inline_kb